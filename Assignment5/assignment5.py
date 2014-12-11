#! /usr/bin/python
# 
# Edward Zhu
# Artificial Intelligence
# Assignment 5
# 
# <Collaboration> with Josh Fermin, Louis Babuuou, Sheefali Tewari, and YOU!


# imports
import sys, time
from hmm import *
import getopt

#
# Classes
#
class DataSet:
	def __init__(self, filename):
		#Open file for reading
		file = open(filename,"r")
		states = set([])
		outputs = set([])
		
		# A sequence - list of (state, output)
		sequences = []
		seq = []
		switched = False

		for line in file.readlines():
			line = line.strip()
			if len(line) == 0:
				continue

			if line ==  "." or line == "..":
				# end of sequence
				sequences.append(seq)
				seq = []
				if line == "..":
					if switched:
						raise Exception("File must have exactly one '..' line")
					# Switch to test sequences
					switched = True
					train_sequences = sequences
					sequences = []

			else:
				words = line.split();
				
				state = words[0]
				# Keep track of all the states/outputs
				states.add(state)

				for output in words[1:]:
					outputs.add(output)
					seq.append( (state, output) )

		# By the time we get here, better have seen the train/test
		# divider
		if not switched:
			raise Exception("File must have exactly one '..' line")

		# Don't forget to add the last sequence!
		if len(seq) > 0:
			sequences.append(seq)
					
		# Ok, the sequences we have now are the test ones
		test_sequences = sequences

		# Now that we have all the states and outputs, create a numbering
		self.states = list(states)
		self.states.sort()
		self.outputs = list(outputs)
		self.outputs.sort()
		state_map = list_index(self.states)
		output_map = list_index(self.outputs)

		self.train_state = map((lambda seq: map(lambda p: state_map[p[0]], seq)),
							   train_sequences)
		self.train_output = map((lambda seq: map (lambda p: output_map[p[1]], seq)), 
							   train_sequences)

		self.test_state = map((lambda seq: map (lambda p: state_map[p[0]], seq)), 
							   test_sequences)
		self.test_output = map((lambda seq: map (lambda p: output_map[p[1]], seq)), 
							   test_sequences)

#
# Utility Functions:
#

# ------------------
# list all the indexesin a matrix
# ------------------
def list_index(xs):
	"""
	Return a mapping from each element of xs to its index
	"""
	m = {}
	for (i, x) in enumerate(xs):
		m[x] = i
	return m

#
#
#



#
# Running Viterbi
#
@print_timing
def viterbi(hmm, d, debug=False):
	#Run the viterbi algorithm for each test sequence in the given dataset
	total_error = 0
	total_n = 0
	if debug:
		print "\nRunning viterbi on each test sequence..."
	for i in range(len(d.test_output)):
		if debug:
			print "Test sequence %d:" % i
		errors = 0
		most_likely = [d.states[j] for j in hmm.most_likely_states(d.test_output[i])]
		actual = [d.states[j] for j in d.test_state[i]]
		n = len(most_likely)
		#print "len(most_likely) = %d  len(actual) = %d" % (n, len(actual))
		for j in range(n):
			# if debug:
			# 	print "%s     %s      %s" % (
			# 	actual[j], most_likely[j], d.outputs[d.test_output[i][j]])
			if actual[j] != most_likely[j]:
				errors += 1
			# if debug:
			# 	print "errors: %d / %d = %.3f\n" % (errors, n, errors * 1.0 / n)
	total_error += errors
	total_n += n

	err =  total_error * 1.0 / total_n

	print "Total mistakes = %d / %d = %f" % (total_error, total_n, err)
	return err

# -----
# Train hmm from data
#
# -----
def train_hmm_from_data(data_filename, debug=False):
	print "\n\nReading in file %s ..." % data_filename
	d = DataSet(data_filename)

	print "Building & Training an HMM from data..."
	hmm = HMM(d.states, d.outputs)
	hmm.learn_from_labeled_data(d.train_state, d.train_output)
	if debug:
		print "The model:"
		print hmm
	return (hmm, d)
	
def main(argv=None):
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:o:f:", ["help", "problem=", "option=", "file="])
	except getopt.GetoptError as err:
		# print help information and exit:s
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
	filename = None
	output = None
	verbose = False
	HMMorder = 1
	for o, a in opts:
		if o in ("-h", "--help"):
			print "\n\n-p is problem flag 1 - 3\n-o is hmm order flag\n-f is the filename being read in specifically\nIF YOU WANT TO USE -f PLEASE DO IT AFTER -p\n"
			sys.exit()
		elif o in ("-o", "--option"):
			if int(a) > 2 or int(a) < 1:
				assert False, "Not a valid hmm order flag"
			else:
				option = int(a)
				if option == 2:
					print "Extra Credit Funcitonality not implemented"
					sys.exit()
		elif o in ("-p", "--problem"):
			if int(a) > 3 or int(a) < 1:
				assert False, "Not a valid problem number"
			else:
				problem = int(a)
		
		elif o in ("-f", "--file"):
			filename = a
			# print filename
			hmm, d = train_hmm_from_data(filename, True)
			err_full = viterbi(hmm, d , True)
		else:
			assert False, "unhandled option"

	if filename == None:
		if problem == 1:
			hmm, d = train_hmm_from_data("Assignment5DataSets/robot_no_momemtum.data", True)
			err_full = viterbi(hmm, d , True)
			print "Finished robot_no_momemtum.data \n Sleeping for 3 seconds and then running robot_with_momemtum.data"
			time.sleep(3)
			hmm, d = train_hmm_from_data("Assignment5DataSets/robot_with_momemtum.data", True)
			err_full = viterbi(hmm, d , True)
			print "Finished robot_with_momemtum.data\n"
		elif problem == 2:
			hmm, d = train_hmm_from_data("Assignment5DataSets/typos10.data", True)
			err_full = viterbi(hmm, d , True)
			print "Finished typos10.data \n Sleeping for 3 seconds and then running typos20.data"
			time.sleep(3)
			hmm, d = train_hmm_from_data("Assignment5DataSets/typos20.data", True)
			err_full = viterbi(hmm, d , True)
			print "Finished typos20.data\n"
		elif problem == 3:
			hmm, d = train_hmm_from_data("Assignment5DataSets/topics.data", False)
			err_full = viterbi(hmm, d , True)
			print "Finished topics.data\n"
	# 	HMMorder = 2
	# if option == 1:
	# 	HMMorder == 1
		
	
	return 0



if __name__ == "__main__":
	sys.exit(main())