# Edward Zhu
# Artificial Intellengence - CSCI 3202
# Collaborated with: Josh Fermin, Louis, Sheefali Tewari, Andrew Arnip
#	

import getopt
import sys

def main():
	options, remainder = getopt.getopt(sys.argv[1:], 'gjm')
	for opt, arg in options:
		if opt in ('-g'):
			something = 'g'
		elif opt in ('-j'):
			something = 'j'
		elif opt in ('-m'):
			something = 'm'


	print 'remainder =', remainder
	print 'something =', something

if __name__ == "__main__":
	main()