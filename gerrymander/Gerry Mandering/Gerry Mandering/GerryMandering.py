import copy, sys, os
from Gerrymanderer import Gerrymanderer

class Neighborhood:
	#Matrix of residents (Rabbits or Ducks)
	residents = [[]];
	#True or False depending on whether or not an area is part of a district
	incorperatedAreas = [[]];
	#Array of Districts
	districts = [];
	#Residents with particular political affiliations without a district
	partiesRemaining = {}

	neighborhoodSize = 0;

	def __init__(self,rOrN):
		if isinstance(rOrN,Neighborhood):
			neighborhood = rOrN
			self.residents = copy.deepcopy(neighborhood.residents)
			self.incorperatedAreas = copy.deepcopy(neighborhood.incorperatedAreas)
			self.districts = copy.deepcopy(neighborhood.districts)
			self.partiesRemaining = copy.deepcopy(neighborhood.partiesRemaining)
			self.neighborhoodSize = neighborhood.neighborhoodSize;
		else:
			residents = rOrN
			self.residents = residents;
			self.incorperatedAreas = [];
			for y in range(len(self.residents)):
				row = [];
				for x in range(len(self.residents[y])):
					if (self.residents[y][x] not in self.partiesRemaining.keys()): self.partiesRemaining[self.residents[y][x]] = 0
					self.partiesRemaining[self.residents[y][x]] += 1

					self.neighborhoodSize += 1

					row.append(False)
				self.incorperatedAreas.append(row);

	def __str__(self):
		s = ""
		for y in range(len(self.residents)):
			row = self.residents[y]
			for x in range(len(row)):
				if (self.incorperatedAreas[y][x]): s += str(row[x]) + "* "
				else: s += str(row[x]) + "  "
			s += "\n"
		return s

	#Checks whether or not the district is valid within the neighborhood
	def isValidDistrict(self,district):
		if District.districtSize != len(district.residents): return False;
		for x,y in district.residents:
			if (self.incorperatedAreas[y][x] == True):
				return False;
		return True;

	#Checks whether or not the additional district will create a future invalid state
	def willCreateInvalidState(self,district):
		#All positions that have not been incorperated
		stack = []
		#All positions that have been visited by the function traverseForUnincorperatedAreas
		visited = []

		#Returns True if area is incorperated or invalid
		def isPositionIncorperated(position,incorperatedAreas=self.incorperatedAreas):
			x,y = position
			if (y >= 0 and y < len(self.residents) and x >= 0 and x < len(self.residents[y])): return incorperatedAreas[y][x];
			return True;
		#Gives cluster that has not been incorperated from the given position
		#If position is incorperated or has been visited it returns empty list
		def traverseForUnincorperatedAreas(position,incorperatedAreas=self.incorperatedAreas):
			cluster = []
			x,y = position;
			if (not incorperatedAreas[y][x] and position not in visited):
				visited.append(position);
				cluster.append(visited);
				x,y = position;
				if (not isPositionIncorperated((x - 1,y),incorperatedAreas)): cluster += traverseForUnincorperatedAreas((x - 1,y));
				if (not isPositionIncorperated((x + 1,y),incorperatedAreas)): cluster += traverseForUnincorperatedAreas((x + 1,y));
				if (not isPositionIncorperated((x,y - 1),incorperatedAreas)): cluster += traverseForUnincorperatedAreas((x,y - 1));
				if (not isPositionIncorperated((x,y + 1),incorperatedAreas)): cluster += traverseForUnincorperatedAreas((x,y + 1));

			return cluster;

		newIncorperatedArea = copy.deepcopy(self.incorperatedAreas)
		for x,y in district.residents:
			newIncorperatedArea[y][x] = True;
		
		for y in range(len(newIncorperatedArea)):
			for x in range(len(newIncorperatedArea[y])):
				if (not isPositionIncorperated((x,y),newIncorperatedArea)):
					stack.append((x,y))
		
		for position in stack:
			uAreaLength = len(traverseForUnincorperatedAreas(position,newIncorperatedArea))
			if ((uAreaLength % District.districtSize) != 0): return True;
		return False;


	#Adds district to neighborhood
	#Returns True or False based on whether or not the district can be added
	def addDistrict(self,district):
		if (self.isValidDistrict(district) and not self.willCreateInvalidState(district)):
			for x,y in district.residents:
				self.incorperatedAreas[y][x] = True;
				self.partiesRemaining[self.residents[y][x]] -= 1
			self.districts.append(district)
			return True
		return False

	#Gets party affiliation for specified position
	#Returns political party or None if the position is not valid
	def getPartyWithPosition(self,position):
		x,y = position
		if (y >= 0 and y < len(self.residents) and x >= 0 and x < len(self.residents[y])): return self.residents[y][x]
		return None

	def unincorperatedAreaCount(self):
		acc = 0
		for row in self.incorperatedAreas:
			for i in row:
				if (i == False): acc += 1
		return acc

	def getPartyMajorityForDistricts(self):
		m = []
		for d in self.districts:
			acc = {}
			partyCount = {}
			for p in d.residents:
				party = self.getPartyWithPosition(p)
				if (party not in partyCount): partyCount[party] = 0
				partyCount[party] += 1

			for party in partyCount.keys():
				count = partyCount[party]
				if (count not in acc): acc[count] = [party]
				else:
					acc[count].append(party)

			maxCount = None
			for count in acc.keys():
				if (maxCount == None or acc[maxCount] < acc[count]): maxCount = count


			if (maxCount != None): m.append(acc[maxCount])
			else: m.append(None)
		return m


class District:
	#Array of coordinate tuples
	residents = set();
	#Size that the district has to be
	districtSize = 0;

	def __init__(self,residents):
		self.residents = residents;

if __name__ == "__main__":
	g = None

	if (len(sys.argv) > 1):
		neighborhoodFileName = sys.argv[1]
		neighborhoodFile = open(neighborhoodFileName)
		residents = []
		for line in neighborhoodFile.readlines():
			line = line.replace('\n','')
			residents.append(line.split(' '))
		n = Neighborhood(residents)
		test = Neighborhood(n)
		g = Gerrymanderer(n)

	#If the Gerrymanderer is not initialized exit program
	if (not g):
		print "Please provide a neighborhood file."
		exit()

	#Sets required district size (based on number of rows)
	District.districtSize = len(n.residents)

	'''
	Daffy: Rabbit season!
	Bugs: Duck Season!
	Daffy: Rabbit Season!
	Bugs: Rabbit Season!
	Daffy: Duck Season! FIRE!
	'''
	maxParty = 'R'
	minParty = 'D'
	g.neighborhood.addDistrict(District([(0,0),(0,1),(1,0),(0,1)]))
	g.setDistrictsForParty(maxParty,minParty)

	print "*************************************"
	print "MAX=" + str(maxParty)
	print "MIN=" + str(minParty)
	print "*************************************"

	print

	print "*************************************"

	for i in range(len(g.neighborhood.districts)):
		residents = g.neighborhood.districts[i].residents
		print "District " + str(i + 1) + ": ",
		for j in range(len(residents)-1):
			position = residents[j]
			print str(position) + ", ",
		if (len(residents) > 0): print str(residents[len(residents)-1])

	print "*************************************"

	print

	print "*************************************"

	partyMajorities = g.neighborhood.getPartyMajorityForDistricts()

	for i in range(len(partyMajorities)):
		if (partyMajorities[i] != None and len(partyMajorities[i]) == 1):
			print "District " + str(i + 1) + ": " + str(partyMajorities[i][0])
		elif (partyMajorities[i] == None):
			print "District " + str(i + 1) + ": No residents have a party affiliation (Error)"
		elif (partyMajorities[i] > 1):
			print "District " + str(i + 1) + ": ",
			districtParties = partyMajorities[i]
			for j in range(len(districtParties) - 1):
				party = districtParties[j]
				print str(party) + ",",
			if (len(districtParties) > 0): print str(districtParties[len(districtParties) - 1])

	print "*************************************"

	print

	print "*************************************"
	#Election outcome
	print "*************************************"










