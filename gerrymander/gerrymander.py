# Edward Zhu
# Artificial Intellengence - CSCI 3202
# Collaborated with:
#	Sheefali Tewari, Andrew Arnoupolis, Steven Tang, and Andrew (he is blonde)
#
# Instead of using a tree (which would take ages to load everything into)
#	we used lists and dictionaries that store various information about the graph and we
# 	will be manipulating with the MinMax utility function to correctly
#	gerrymander regions on a graph
#	
#	We first loaded the file into a graph and set everything up accordingly.
#
#	For each turn we go through all valid areas on the graph and pick the best
#	shape and area for either D and R. Then the end will calculate who won.
#
#	There are a lot of comments for further explaination.

import sys, argparse, itertools, time 

#Globals
availablemoves={}
finishedmoves={}
originalgraph = {}

# areas that D or R owns
D_area = []
R_area = []

# depth of each move
depth = 3

player1 = 'R'
player2 = 'D'

# minmax function, finds the best moves
def minmax(player, depth, currentMoveList):
	if depth == 0:
		#depth can't go lower, so return the move
		return currentMoveList 
	else:	
		bestScore = 0

		# iterate all the legal moves
		for x in availablemoves:
			# get utility of given move
			currentMoveList, score = utility(player, x, currentMoveList)
			# record whether a move is better than previous
			if score >= bestScore:	
				bestScore = score
				bestMove = currentMoveList

		#continue recursion until depth is 0
		return minmax(player, depth-1, bestMove)

# U(a|e) = sum P(result(a)=s'|a,e)*U(s')
# emulated equation above; found best score for each shape 
def utility(player,move,currentMoveList):
	# score 0 if can't find anything
	score = 0 

	# all possibleMoves (square, horizontal, and vertical line)
	possibleMoves = [] 
	x,y = move

	counter = 0
	temp = []
	# vertical line check
	for j in range(0, 4):
		move = x,y+j
		if checklegal(move,currentMoveList):
			temp.append(move)
			counter+=1
			if counter == 4:
				possibleMoves.append(temp)

	counter = 0
	temp = []
	# horizontal line check
	for i in range(0, 4):
		move = x+i,y
		if checklegal(move,currentMoveList):
			temp.append(move)
			counter+=1
			if counter == 4:
				possibleMoves.append(temp)

	counter = 0
	temp = []
	# square check
	for i in range(0,2):
		for j in range(0,2):
			move=x+i,y+j
			if checklegal(move,currentMoveList):
				temp.append(move)
				counter += 1
				if counter == 4:
					possibleMoves.append(temp)

	# evaluate all possible moves and find best one. if empty than disregard
	newMove, score = findbestMove(possibleMoves, player)
	if newMove != [] and len(currentMoveList) <= depth:
		currentMoveList.append(newMove)

	#If nothing, return an empty list and 0 for this move (we iterate over all moves in minmax and find the best possible move there)
	return currentMoveList, score

# Append the optimal move done by player to the right ownership
def makeMove(listofMoves, player):
	if listofMoves == []:
		return 
	if player == 'R':
		R_area.append(listofMoves)
	else:
		D_area.append(listofMoves)
	
	#remove moves from right lists
	for moves in listofMoves:
		for x in moves:
			#put player into finishedmoves list to mark district
			finishedmoves[x] = player
			#pop off the current legal move as it isn't legal anymore
			availablemoves.pop(x, None)

# check if shape is legal, return bool accordingly
def checklegal(move, currentMoveList):
	if move not in availablemoves:
		return False
	if move in finishedmoves:
		return False
	for a in currentMoveList:
		if move in a:
			return False 
	return True

#evaluate a given move and find best district to choose
def findbestMove(possibleMoves, player):	
	optMove = []
	score = 0
	prevScore = 10

	for eachmove in possibleMoves:
		dScore = 0
		rScore = 0
		for i in eachmove:		#get a score for this move
			if originalgraph[i] =='D':
				dScore+=1
			if originalgraph[i] =='R':
				rScore+=1

		# avoid dividing by zero		
		if dScore==0: dScore+=1
		if rScore==0: rScore+=1 
		
		# find best move for each player
		if player == 'D':
			# try to find the 3-1 wins, and not a 4-0 win
			if (dScore/rScore) > 1 and (dScore/rScore) <= prevScore:
				optMove = eachmove
				score = float(dScore/rScore)
				prevScore = score
		if player == 'R':
			if (rScore/dScore) > 1 and (rScore/dScore) <= prevScore:
				optMove = eachmove
				score = float(rScore/dScore)
				prevScore = score

	return optMove, score

# read in neighborhood and make it into a graph, availablemoves an neighborhood
def makeGraph(neighborhood,length):
	for x in range(0,len(neighborhood)):
		owner = neighborhood[x]
		row = x/length
		col = x%length
		availablemoves[row,col]=owner
		originalgraph[row,col] = owner

	print "\nInitial Graph of neighborhood given:"
	for x in range(0,len(neighborhood)):
		if x%length==0:
			print '\n',neighborhood[x],
		else:
			print neighborhood[x],
	print '\n'

# For every slot in the original graph, if the slot is D add 1 to count and it was
# R then subtract 1 from count. depending on negative or positive will explain
# the winner
def whoWon():
	count = 0
	for x in originalgraph:
		if x in finishedmoves:
			if finishedmoves[x] =='D':
				count += 1
			else:
				count -= 1
	if count < 0:
		print "Election outcome: RABBITS WIN!"
	elif count > 0:
		print "Election outcome: DUCKS WIN!"
	elif count==0:
		print "Election outcome: TIE!"

#reads file into matrix
def fileparser(f):
	try:
	    inputfile = open(f, "r")
	except:
	    sys.exit("ERROR. Can't read filename given.")
	text = inputfile.read()

	neighborhood = []
	for x in text:
		if x == 'D':
			neighborhood.append(x)
		elif x=='R':
			neighborhood.append(x)

	inputfile.close()

	return neighborhood

def playGame(length):
	print 'Printing results...'
	print
	print "*************************************"
	print "MAX = R"
	print "MIN = D"
	print "*************************************\n"

	# have duck and rabbit move accordingly
	i = 0
	while (i<length/2):
		duckMove = minmax(player1,depth,[])
		makeMove(duckMove, player1)
		rabbitMove = minmax(player2,depth,[])
		makeMove(rabbitMove, player2)
		i += 1 

	#print out game state, and which regions would go towards R or D
	print "Final game state: "
	print 'Symbol _ defines a TIE between R and D in district'
	for i in range(0,length):
		for j in range(0,length):
			move=i,j
			if move in finishedmoves:
				if j%length==0:
					print '\n', '[',move, '=',finishedmoves[move],']',
				else:
					print '[',move, '=',finishedmoves[move],']',
			else:
				if j%length==0:
					print '\n[', move, '= _ ]',
				else:
					print '[', move, '= _ ]',
	
	#print valid districts
	district = 1
	print "\n\nNotice that not all districts are shown"
	print "Districts that will are invalid shape, or will result in a tie will be disregarded"
	print "*************************************"
	for moves in D_area:
		for x in moves:
			print "District",district,':',x, "is owned by Ducks"
			district+=1
	for moves in R_area:
		for y in moves:
			print "District",district,':',y, "is owned by Rabbits"
			district+=1
	print "*************************************\n"

def main():
	# start time and open file and parse it
	start = time.time()
	fin = sys.argv[1]
	neighborhood = fileparser(fin)

	# nxn assumed; find length of a side
	if len(neighborhood) == 16:
		length = 4
	if len(neighborhood) == 64:
		length =  8

	# make graph and print it 
	makeGraph(neighborhood, length)
	# play!
	playGame(length)
	# find out who won!
	whoWon()

	# stop time and print it
	stop = time.time() - start 
	print 'Total Time Taken:'
	print stop
	print


if __name__ == "__main__":
	main()
