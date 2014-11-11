# Edward Zhu
# Artificial Intellengence - CSCI 3202
# Collaborated with: Josh Fermin, Louis, Sheefali Tewari
#	


# P=Pollution
# S=Smoker
# C=Cancer
# D=Dyspnoea
# X=Xray
 
import getopt, sys, re
from numpy import *
import CancerModel as Cancer
from pbnt.Graph import *
from pbnt.Distribution import *
from pbnt.Node import *
from pbnt.Inference import *


def conditional_prob(args, BayesNet, engine):
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

	print "The conditional probability of", toCalculate.name, "=", leftTruth, ", given", given, "is: ", conditionalProbablity
	return conditionalProbablity

def joint_prob(args, BayesNet):
	print "\nThe joint probability for " + args + " is:\n"
	argtype = checkArgs(args)
	arglookup = findArgValue(args)
	for node in BayesNet.nodes:
		if node.value == arglookup:
			if argtype == "lower":
				return
			if argtype == "upper":
				return
			if argtype == "tilda":
				return

def marginal_prob(args, BayesNet, engine):
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
		print "\nThe marginal probability of " + CalcNode.name + "=true: ", Q[index]
		return Q[index]
	elif argtype == "tilda":
		index = Q.generate_index([False], range(Q.nDims))
		print "\nThe marginal probability of " + CalcNode.name + "=false: ", Q[index]
		return Q[index]
	elif argtype == "upper":
		index = Q.generate_index([True], range(Q.nDims))
		print "\nThe marginal probability of " + CalcNode.name + "=true: ", Q[index]
		index = Q.generate_index([False], range(Q.nDims))
		print "The marginal probability of " + CalcNode.name + "=false: ", Q[index]



def main():
	BayesNet = Cancer.cancer()
	engine = JunctionTreeEngine(BayesNet)

	options, remainder = getopt.getopt(sys.argv[1:], 'g:j:m:')
	for opt, arg in options:
		if opt in ('-g'):
			conditional_prob(arg, BayesNet, engine)

		elif opt in ('-j'):
			joint_prob(arg, BayesNet)
			# find conditional prob, then marginal, then multiply together

		elif opt in ('-m'):			
			marginal_prob(arg, BayesNet, engine)
		else:
			assert False, "unhandled option"

def bruteforcetuple(BayesNet, letter):
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


# check if false/true or a distribution
def checkArgs(args):
	if args.islower():
		if "~" in args:
			return "tilda"
		else:
			return "lower"
	elif args.isupper():
		return "upper"

# returns the letter in lowercasepyc
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