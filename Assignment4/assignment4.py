import getopt, sys
from numpy import *
import CancerModel as Cancer
from pbnt.Graph import *
from pbnt.Distribution import *
from pbnt.Node import *
from pbnt.Inference import *

"""
Edward Zhu
Artificial Intellengence - CSCI 3202
Collaborated with: Josh Fermin, Louis, Sheefali Tewari
	

Issues:
	After calculating out the marginal probability by hand,
	the marginal values returned by the toolbox are incorrect
	for all variables except for Pollution and Smoker. Because
	of this, it will skew the answers for joint and conditional
	probability. 


How to Use:
    Flags
	    -g  conditional probablity
	    -j  joint probability
	    -m  marginal probability
	    -h  help
    Arguments (Distribution, true, false)
	    P,p,~p  pollution
	    S,s,~s  Smoker   
	    C,c,~c  Cancer   
	    D,d,~d  Dyspnoea 
	    X,x,~d  X-Ray 

"""


#--------------------------------------------------
# conditional probability that takes in a marginal
# value and gives evidence to the engine of the
# given conditions
#-------------------------------------------------
def conditional_prob(args, BayesNet, engine, show=True):
	conditionalTuples = []

	left, given = parseConditionalArgs(args)

	leftTuple = bruteforcetuple(BayesNet, left)

	#list of tuples for given conditions
	for letter in given:
		conditionalTuples.append(bruteforcetuple(BayesNet, letter))

	for condition, truth in conditionalTuples:
		engine.evidence[condition] = truth

	# left side of | 
	toCalculate, leftTruth = leftTuple

	Q = engine.marginal(toCalculate)[0]
	index = Q.generate_index([leftTruth], range(Q.nDims))
	conditionalProbablity = Q[index]

	if show: print "The conditional probability of", toCalculate.name, "=", leftTruth, ", given", given, "is: ", conditionalProbablity
	return conditionalProbablity

#--------------------------------------------------
# calls joint_prob to start off the recursive callings
#-------------------------------------------------
def joint_distribution(args, BayesNet, engine, argsarray):
	result = joint_prob(args, BayesNet, engine, argsarray)
	print "The joint probability of", args, "is:", result

#--------------------------------------------------
# recursively calls either conditional_prob*marginal+prob
# or conditional_prob*joint_prob and returns the ending
#-------------------------------------------------
def joint_prob(args, BayesNet, engine, argsarray):
	typeArgs = checkArgs(args)
	if typeArgs == "lower":
		if len(argsarray) <= 1:
			print "Joint Probability Distribution must take at least 2 arguments"
			sys.exit(2)
		elif len(argsarray) == 2:
			conditionalArgs = argsarray[0] + "|" + argsarray[1]
			marginalArgs = argsarray[1]
			return conditional_prob(conditionalArgs, BayesNet, engine, False) * marginal_prob(marginalArgs, BayesNet, engine, False)
		elif len(argsarray) > 2:
			conditionalArgs = argsarray[0] + "|" + argsarray[1]
			toCalculate = argsarray.pop(0)
			args = "".join(argsarray)
			argsarray = parseJointArgs(args)
			return conditional_prob(conditionalArgs, BayesNet, engine, False) * joint_prob(args, BayesNet, engine, argsarray)
	elif typeArgs == "upper":
		print "upper"
		if len(argsarray) <= 1:
			print "Joint Probability Distribution must take at least 2 arguments"
			sys.exit(2)
		elif len(argsarray) == 2:
			conditionalArgs = argsarray[0] + "|" + argsarray[1]
			marginalArgs = argsarray[1]
			return conditional_prob(conditionalArgs, BayesNet, engine, False) * marginal_prob(marginalArgs, BayesNet, engine, False)
		elif len(argsarray) > 2:
			conditionalArgs = argsarray[0] + "|" + argsarray[1]
			toCalculate = argsarray.pop(0)
			args = "".join(argsarray)
			argsarray = parseJointArgs(args)
			return conditional_prob(conditionalArgs, BayesNet, engine, False) * joint_prob(args, BayesNet, engine, argsarray)

#--------------------------------------------------
# marginal probability of a single given letter
#-------------------------------------------------
def marginal_prob(args, BayesNet, engine, show=True):
	arglookup = findArgValue(args)
	if len(args) > 1:
		print "Marginal Probability Distribution can only take one argument"
		sys.exit(2)
	for node in BayesNet.nodes:
		if node.id == 0 and arglookup == 'p':
			CalcNode = node
		if node.id == 1 and arglookup == 's':
			CalcNode = node
		if node.id == 2 and arglookup == 'c':
			CalcNode = node
		if node.id == 3 and arglookup == 'x':
			CalcNode = node
		if node.id == 4 and arglookup == 'd':
			CalcNode = node

	Q = engine.marginal(CalcNode)[0]
	argtype = checkArgs(args)
	if argtype == "lower":
		index = Q.generate_index([True], range(Q.nDims))
		if show: print "\nThe marginal probability of ", CalcNode.name, "=true: ", Q[index]
		return Q[index]
	elif argtype == "tilda":
		index = Q.generate_index([False], range(Q.nDims))
		if show: print "\nThe marginal probability of ", CalcNode.name, "=false: ", Q[index]
		return Q[index]
	elif argtype == "upper":
		index = Q.generate_index([True], range(Q.nDims))
		print "\nThe marginal probability of ", CalcNode.name, "=true: ", Q[index]
		if show: index = Q.generate_index([False], range(Q.nDims))
		print "The marginal probability of ", CalcNode.name, "=false: ", Q[index]

#--------------------------------------------------
# main functions that takes in options and executes
#--------------------------------------------------
def main():
	BayesNet = Cancer.cancer()
	engine = JunctionTreeEngine(BayesNet)

	options, remainder = getopt.getopt(sys.argv[1:], 'g:j:m:')
	for opt, arg in options:
		if opt in ('-g'):
			conditional_prob(arg, BayesNet, engine)

		elif opt in ('-j'):
			argsarray = parseJointArgs(arg)
			result = []
			joint_distribution(arg, BayesNet, engine, argsarray)

		elif opt in ('-m'):			
			marginal_prob(arg, BayesNet, engine)

		else:
			assert False, "unhandled option"

#--------------------------------------------------
# puts in tuple of the node name with the value of
# either true or false
#--------------------------------------------------
def bruteforcetuple(BayesNet, letter, joint_distrib=False):
	for node in BayesNet.nodes:
		if node.id == 0:
			pollution = node
		if node.id == 1:
			smoker = node
		if node.id == 2:
			cancer = node
		if node.id == 3:
			xray = node
		if node.id == 4:
			dyspnoea = node

	if letter == 'p':
		returntuple = (pollution, True)
	elif letter == 's':
		returntuple = (smoker, True)
	elif letter == 'c':
		returntuple = (cancer, True)
	elif letter == 'x':
		returntuple = (xray, True)
	elif letter == 'd':
		returntuple = (dyspnoea, True)
	elif letter == '~p':
		returntuple = (pollution, False)
	elif letter == '~s':
		returntuple = (smoker, False)
	elif letter == '~c':
		returntuple = (cancer, False)
	elif letter == '~x':
		returntuple = (xray, False)
	elif letter == '~d':
		returntuple = (dyspnoea, False)
	else:
		print "Please give a good condition."
		exit()

	return returntuple

#--------------------------------------------------
# give back the left and right side of the | symbol
# right side given as lists
#--------------------------------------------------
def parseConditionalArgs(args):
	splitPipe = args.split('|')
	left = splitPipe[0]
	right = splitPipe[1]

	given = list(right)
	given = iter(given)
	conditionalArgs2 = []
	skip = False
	for string in given:
		if string == "~":
			conditionalArgs2.append("~" + given.next())
			continue
		else:
			conditionalArgs2.append(string)
	query = left
	return query, conditionalArgs2

#--------------------------------------------------
# given a string of args i.e. "PCS" will return
# an array i.e. ['P', 'C', 'S']
#--------------------------------------------------
def parseJointArgs(args):
	given = list(args)
	given = iter(given)
	jointArgs = []
	skip = False
	for string in given:
		if string == "~":
			jointArgs.append("~" + given.next())
			continue
		else:
			jointArgs.append(string)
	return jointArgs

#--------------------------------------------------
# check if true or false, or a full distrubution
#--------------------------------------------------
def checkArgs(args):
	if args.islower():
		if "~" in args:
			return "tilda"
		else:
			return "lower"
	elif args.isupper():
		return "upper"

#--------------------------------------------------
# return letter in lowercases
#--------------------------------------------------
def findArgValue(args):
	if args.islower():
		if "~" in args:
			return args.translate(None, '~')
		else:
			return args
	elif args.isupper():
		return args.lower()

if __name__ == "__main__":
	main()