
import sys
import os
from os.path import split, join, isfile, isdir

import traceback


script_dir = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(join(script_dir,'simplejson-2.1.1-py2.5-win32.egg'))

import simplejson
import urllib
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
	q = make_search_string(path)
	url, url0 = search_google(q)
	
	if url==None: # try without russian
		print '!!! try without russian'
		
		q = clean_russian(q)
		
		print 'q:',q
		
		if q != None:
			url, url1 = search_google(q)
			if url0 == None:
				url0 = url1
	
	if url==None:
		url = url0
	
	print 'URL:', url
	return url

def search_google(q):
	query = urllib.urlencode({'q' : q.decode('cp1251').encode("utf-8")})
	url = u'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=8&%s'.encode("utf-8") \
		% (query)
		
	search_results = urllib.urlopen(url)
	json = simplejson.loads(search_results.read())
	results = json['responseData']['results']

	for res in results:
		print 'url:', res['url']
		
	url = search_for_site(results, 'imdb.com/title/tt')
	if url == None:
		url = search_for_site(results, 'kinopoisk.ru/level')
		
	if len(results) > 0:
		url0 = results[0]['url'] # most relevant
	else:
		url0 = None
		
	return url, url0
	
def search_for_site(rr, site):
	for r in rr:
		url = r['url']
		if url.find(site) != -1:
			return url
	
def make_search_string(path):
	if isfile(path): 
		dn, fn = split(path)
		_, dn = split(dn)
	else: # dir
		_, dn = split(path)
		
	
	dn_clean = clean(dn)
	
	print dn
	print 'cleaned:', dn_clean
	#print fn
	
	return dn_clean
	
def clean(q):
	trash_re = '|'.join(r'\[%s\]' % t for t in TRASH)
	q = re.sub('(?i)' + trash_re,'',q)
	return q.strip()
	
def clean_russian(q):
	m = re.match(r'.+(\[.+?\]).+',q)
	
	if m != None:
		q = q[:m.start(1)] + ' '+q[m.end(1):]
	
	return q	
	

if __name__=='__main__':
	try:
		main(sys.argv[1:])
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback,file=sys.stdout)
		input()

	