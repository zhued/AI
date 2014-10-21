# Edward Zhu
# Artificial Intellengence
# 
#
#argparse: grab min and max tree grids from large/small neighborhood
#

import argparse
import sys
try:
    in_file = open(sys.argv[1], "r")
except:
    sys.exit("ERROR. Can't read supplied filename.")
text = in_file.read()
#print text

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


player1 = 'D'
player2 = 'R'


# Begin game definitions
def minmax(player):
	bestMoveScore = 0
	worstMoveScore = 1000000
	previousMoves = []

	
	for i in range(0,length):
		for j in range(0, length):
			move=i,j
			#get utility of given move
			previousMoves, score = utility(player, move, previousMoves)
			#record whether a move is better or worse than previous
			if score >= bestMoveScore:	#get max and subsequent move
				bestMoveScore = score
				bestMove = previousMoves
			if score < worstMoveScore:    #get min and subsequent move
				worstMoveScore = score
				worstMove = previousMoves

			#continue until we have used all of our moves or there are no moves
			if len(previousMoves) >= movesPerTurn: 
				return bestMove, worstMove  #we have fulfilled our amount of moves here; break

	return bestMove, worstMove




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
		if move not in legalmoves:	#special catch; say we are on the far right and y+j goes off the board
			break
		if checklegal(move):
			temp.append(move)
			counter+=1
			if counter == 4:
				possibleMoves.append(temp)

	counter = 0
	temp = []
	#check for a left-right row in this spot
	for i in range(0, 4):
		move = x+i,y
		if move not in legalmoves:	#errcatch for going out of the county
			break
		if checklegal(move):
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
			if move not in legalmoves:	#errcatch for going out of the county
				break
			if checklegal(move):
				temp.append(move)
				counter += 1
				if counter == 4:
					possibleMoves.append(temp)

	bestScore=10
	bestMove = []
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

	#If nothing, return an empty list and 0 for this move (we iterate over all moves in minmax and find the best possible move there)
	return bestMove, score


def checklegal(move):

	if move in illegalmoves:
		return False #this spot is already taken by the other party
					 #majority ownership determined once we have found a complete move
	return True


def executeMove(move, player):
	if move == []:
		return 
	if player == 'D':
		demOwns.append(move)
	else:
		rabOwns.append(move)

	for x in move:
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
	print legalmoves
	maxMoves = length*2
	it = 0
	while (it < maxMoves):
		bestMove, worstMove = minmax(player1)
		executeMove(bestMove, player1)	#wait till we have the best move to execute it
		bestMove, worstMove = minmax(player2)
		executeMove(bestMove, player2)
		it += 1 

	printDictionaryNice(illegalmoves)
	
	print "\ndogs own"
	print demOwns
	print 'rabbits own:'
	print rabOwns

	if len(demOwns) > len(rabOwns):
		print "DAWGS WINNN"
	elif len(rabOwns) > len(demOwns):
		print "RABBITS win!!!"
	else:
		print "TIE?!"

def main():
	printneighborhood(neighborhood)
	coordAssign(neighborhood)
	game()



main()



































