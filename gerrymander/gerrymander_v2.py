# Edward Zhu
# Artificial Intellengence
# 

#argparse: grab min and max tree grids from large/small neighborhood


import argparse
import sys

try:
    in_file = open(sys.argv[1], "r")
except:
    sys.exit("ERROR. Can't read supplied filename.")
text = in_file.read()

neighborhood = []
for x in text:
	if x == 'D':
		neighborhood.append(x)
	elif x=='R':
		neighborhood.append(x)

in_file.close()
#end command line argument parsing


#globals 
#figure out neighborhood size(we could generalize this to nxn neighborhoods of any size)
if len(neighborhood) == 16:
	length = 4 #1 square, 1 row/col
	movesPerTurn = 4
if len(neighborhood) == 64:
	length =  8 #2 squares, 1 row/col
	movesPerTurn = 8

legalmoves={}
illegalmoves={}
neighborhoodKey = {}
demOwns = []
rabOwns = []

depth = 3
player1 = 'R'
player2 = 'D'

# Begin game definitions
def minmax(player, depth, previousMoves):
	if depth == 0:
		return previousMoves #we have fulfilled our amount of moves here; break
	else:
	
		bestMoveScore = 0
		

		for x in legalmoves:
			#get utility of given move
			previousMoves, score = utility(player, x, previousMoves)
			#record whether a move is better or worse than previous
			if score >= bestMoveScore:	#get max and subsequent move
				bestMoveScore = score
				bestMove = previousMoves

		#continue until we have used all of our moves (depth ==0) while disregarding empty moves (inadmissible states)
		return minmax(player, depth-1, bestMove)





#need: reward/utility function: U(a|e) = sum P(result(a)=s'|a,e)*U(s')
def utility(player,move,previousMoves):

	score = 0 #set score to be equal to 0 if we can't grab anything; 
			  #otherwise see score-setting at the end
	possibleMoves = [] #we will check this at end to find the best of 3 moves
	x,y=move

	
	counter = 0
	temp=[]
	#check for an up-down column in the spot
	for j in range(0, 4):
		move = x,y+j
		if checklegal(move,previousMoves):
			temp.append(move)
			counter+=1
			if counter == 4:
				possibleMoves.append(temp)

	counter = 0
	temp = []
	#check for a left-right row in this spot
	for i in range(0, 4):
		move = x+i,y
		if checklegal(move,previousMoves):
			temp.append(move)
			counter+=1
			if counter == 4:
				possibleMoves.append(temp)

	counter = 0
	temp = []
	#check for a square in this spot
	for i in range(0,2):
		for j in range(0,2):
			move=x+i,y+j
			if checklegal(move,previousMoves):
				temp.append(move)
				counter += 1
				if counter == 4:
					possibleMoves.append(temp)


	newMove, score = evaluateMove(possibleMoves, player)
	if newMove != [] and len(previousMoves) <= depth:
		previousMoves.append(newMove)

	#If nothing, return an empty list and 0 for this move (we iterate over all moves in minmax and find the best possible move there)
	return previousMoves, score

def evaluateMove(possibleMoves, player):
	
	bestScore=10 
	
	bestMove = []
	score = 0

	for possible in possibleMoves:
		dScore = 0
		rScore = 0
		for i in possible:		#get a score for this move
			if neighborhoodKey[i] =='D':
				dScore+=1
			if neighborhoodKey[i] =='R':
				rScore+=1
		
		if dScore==0:	 #avoid divide by 0 errors
			dScore+=1 	 #this will give a high score because instead of a ratio close to 0
		if rScore==0:	 #so, we probably won't pick this, but at the end of the game we will take
			rScore+=1 	 #districts that aren't highly contested
		#we want a ratio greater than 1 but close to 1 as possible
		if player == 'D':
			if (dScore/rScore) > 1 and (dScore/rScore) < bestScore:
				bestMove = possible
				score = float(dScore/rScore)
		if player == 'R':
			if (rScore/dScore) > 1 and (rScore/dScore) < bestScore:
				bestMove = possible
				score = float(rScore/dScore)


	return bestMove, score

def checklegal(move, previousMoves):
	if move not in legalmoves: #boundary catch; say we are on the far right and y+j goes off the board
		return False
	if move in illegalmoves:
		return False #this spot is already taken by the other party

	for x in previousMoves:
		if move in x:
			return False # this is already a potential move we are about to make
	return True


def executeMove(moveList, player):
	if moveList == []:
		return 
	if player == 'D':
		demOwns.append(moveList)
	else:
		rabOwns.append(moveList)
	for moves in moveList:
		for x in moves:
			illegalmoves[x] = player
			legalmoves.pop(x, None)

#output a dictionary of (x,y) tuple keys that return a D or R for a given move
#originally legalmoves will consist of all neighborhood
def coordAssign(neighborhood):
	for x in range(0,len(neighborhood)):
		owner = neighborhood[x]
		row = x/length
		col = x%length
		legalmoves[row,col]=owner
		neighborhoodKey[row,col] = owner

def printneighborhood(neighborhood):
	for x in range(0,len(neighborhood)):
		if x%length==0:
			print '\n',neighborhood[x],
		else:
			print neighborhood[x],
	print '\n'

def printDictionaryNice(dictionary):
	for i in range(0,length):
		for j in range(0,length):
			move=i,j
			if move in dictionary:
				if j%length==0:
					print '\n', '[',move, '=',dictionary[move],']',
				else:
					print '[',move, '=',dictionary[move],']',
			else:
				if j%length==0:
					print '\n[', move, '= _ ]',
				else:
					print '[', move, '= _ ]',

def game():

	print "*************************************"
	print "MAX =", player1
	print "MIN =", player2
	print "*************************************\n"

	maxMoves = length
	it = 0
	while (it<length/2):
		dogMove = minmax(player1,depth,[])
		executeMove(dogMove, player1)	#wait till we have the best move to execute it
		rabbitMove = minmax(player2,depth,[])
		executeMove(rabbitMove, player2)
		it += 1 

	print "Final game state: "
	printDictionaryNice(illegalmoves)
	
	district = 1
	print "\n\n*************************************"
	for moves in demOwns:
		for x in moves:
			print "District",district,':',x, "is owned by Dogs"
			district+=1
	for moves in rabOwns:
		for y in moves:
			print "District",district,':',y, "is owned by Rabbits"
			district+=1
	print "*************************************\n"

	getWinner()
	


def getWinner():
	d = 0
	r = 0
	for x in neighborhoodKey:
		if x in illegalmoves:
			if illegalmoves[x] =='D':
				d+=1
			else:
				r+=1
	if r>d:
		print "Election outcome: RABBITS WIN!"
	elif d>r:
		print "Election outcome: DOGS WIN!"
	elif d==r:
		print "Election outcome: TIE!"



def main():
	printneighborhood(neighborhood)
	coordAssign(neighborhood)
	game()


if __name__ == "__main__":
	main()