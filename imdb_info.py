
import sys
import os
from os.path import split, join, isfile, isdir
import traceback

script_dir = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(join(script_dir,'simplejson-2.1.1-py2.5-win32.egg'))

import simplejson as j

import re


IMDB, KINOPOISK = 'imdb', 'kinopoisk'
TRASH = [
	'ru','rus','en','eng',
	'dvdrip', 'tvrip']

def fail(s):
	print s
	sys.exit(1)

def main(args):
	#print args
	
	if len(args) == 0:
		fail('Not enough args')
		
	path = args[0];
	print path
	
	do_search(path, IMDB)
	
	input()

def do_search(path, site):
	if (isfile(path)): 
		keywords = make_keywords(path)
	else:
		fail('dir not supported yet')
	
def make_search_string(path):
	dn, fn = split(path)
	_, dn = split(dn)
	
	dn_clean = clean(dn)
	
	print dn
	print 'cleaned:', dn_clean
	print fn
	
def clean(q):
	trash_re = '|'.join(r'\[%s\]' % t for t in TRASH)
	q = re.sub('(?i)' + trash_re,'',q)
	return q
	

if __name__=='__main__':
	try:
		main(sys.argv[1:])
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback,file=sys.stdout)
		input()

	