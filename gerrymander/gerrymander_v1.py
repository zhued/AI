# Edward Zhu
# gerrymander.py
# Worked with Sheefali and Noah

import sys, itertools, time


#parse file and place each letter into a a 2 dimensional array
def fileparser(f):
	i = 0
	array = []
	for line in f:
		line = line.rstrip('\n')
		line = line.split('  ')
		j = 0
		for c in line:
			array.append((i, j, c))
			j += 1
		i += 1
	return array, min([i, j])

def adjacent(b1, b2):
	if ((abs(b1[0] - b2[0])*abs(b1[0]-b2[1])) <= 1):
		return True
	else:
		return False

def valid(district): 
	size = len(district)
	temp1 = []
	temp2 = []
	for a in district:
		temp1.append(a)
	temp2.append(temp1.pop())
	i = 0
	while(len(temp2) < size):
		good = False
		j = 0
		while(j < len(temp1)):
			if(adjacent(temp1[j], temp2[i])):
				good = True
				break
			j += 1
		if(good):
			temp2.append(temp1.pop(j))
		else:
			i += 1
		if(i >= len(temp2)):
			return False
	return True

#from intertools:
def ifilter(predicate, iterable):
	#ifilter(lambda x: x%2, range(10)) --> 1 3 5 7 9
	if predicate is None:
		predicate = bool
	for x in iterable:
		if predicate(x):
			yield x

def ifilterfalse(predicate, iterable):
	#ifilter(lambda x: x%2, range(10)) --> 2 4 6 8
	if predicate is None:
		predicate = bool
	for x in iterable:
		if not predicate(x):
			yield x

def movesGenerator(positions, size):
	a = 1
	b = size
	moves = []
	while(a <= size):
		for pos in positions:
			temp = []
			if((pos[0]*a) <= size and (pos[1]*b) <= size):
				for i in range(a):
					for j in range (b):
						temp.append(positions[size*(pos[0]+i) + (pos[1] + j)])
				moves.append(set(temp))
		a = int(a*2)
		b = int(b/2)
	return moves

def util(currentMoves):
	score = 0
	for district in currentMoves:
		count = 0
		for vote in district:
			if(vote[2] == "R"):
				count += 1
			else:
				count -= 1
		if(count > 0):
			score += 1
		elif(count < 0):
			score -= 1
	return score

def minMax(currentM, availableM, numM, goalNum):
	if(len(availableM) == 0):
		if(numM == goalNum):
			score = util(currentM)
			return score, currentM
		else:
			return 0, []
	if(numM % 2): #min turn
		minScore = 100
		minMove = []
		for move in availableM:
			nextM = []
			for nex in availableM:
				if(not move.intersection(nex)):
					nextM.append(nex)
			#nextM = ifilterfalse(lambda x: move.intersection(x), availableM)
			temp = List(currentM)
			temp.append(move)
			score, move = minMax(temp, nextM, numM + 1, goalNum)
			if(score <= minScore and len(move)!= 0):
				minScore = score
				minMove = move
		return minScore, minMove
	else: #max turn
		maxScore =- 100
		maxMove = []
		for move in availableM:
			nextM = []
			for nex in availableM:
				if(not move.intersection(nex)):
					nextM.append(nex)
			#nextM = ifilterfalse(lambda x: move.intersection(x), availableM)
			temp = list(currentM)
			temp.append(move)
			score, move = minMax(temp, nextM, numM + 1, goalNum)
			if(score >= maxScore and len(move)!= 0):
				maxScore = score
				maxMove = move
		return maxScore, maxMove

def main():
	start = time.time()
	fin = open(sys.argv[1])
	
	fout = open("output" + sys.argv[1], 'w')
	area, s = fileparser(fin)

	moves = movesGenerator(area, s)

	finalScore, movesTaken = minMax(List(), moves, 0, s)
	print(finalScore, len(movesTaken), movesTaken)
	fout.write(str(movesTaken))
	stop = time.time() - start 
	print(stop)

if __name__ == "__main__":
	main()
