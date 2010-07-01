
import sys
#from simplejson-2.1.1-py2.5-win32.egg import simplejson as j

sys.path.insert(0, 'simplejson-2.1.1-py2.5-win32.egg')

import simplejson as j

def main(args):
	#print args
	
	if len(args) == 0:
		print 'Not enough args'
		sys.exit(1)
		
	path = args[0];
	print path
	
	input()


if __name__=='__main__':
	main(sys.argv[1:]);