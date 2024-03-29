# coding: utf-8

__author__ = 'xonixx@gmail.com'

import sys
import os
from os.path import split, join, isfile, splitext

import traceback


script_dir = os.path.realpath(os.path.dirname(sys.argv[0]))
sys.path.append(join(script_dir, 'simplejson-2.1.1-py2.5-win32.egg'))

import simplejson
import urllib
import re

import webbrowser

from cfg import *

def fail(s):
    print s
    sys.exit(1)


def p(s):
    print
    print s
    print


def main(args):
    #print args

    if not len(args):
        fail('Not enough args')

    path = args[0]
    print path

    url = do_search(path)

    if url is None:
    #        url='data:text/html,Film not found =(';
        pass
    else:
        webbrowser.open(url, new=NEW_BROWSER_WINDOW)
        #webbrowser.open_new_tab(url)

    if DEBUG:
        input()


def do_search(path):
    # todo: if only not folder
    to_try_search = [
        ('by film file name', make_search_string(path, True)),
        ('by film folder name', make_search_string(path, False)),
    ]

    for name in NOT_SEARCH_FOLDERS:
        for k,v in to_try_search:
            if name.lower() == v.lower():
                to_try_search.remove((k,v))

    print 'to_try_search:', to_try_search

    url, url0 = None, None

    for search_name, search_str in to_try_search:
        p('Searching ' + search_name + " : \n"
                                       'q=' + search_str)

        url, url0 = search_google(search_str)

        if url is not None:
            break

#    q = make_search_string(path)
#    url, url0 = search_google(q)
#
#    if url is None: # try without russian
#        print '\n!!! try without russian'
#
#        qe = clean_russian(q)
#
#        print 'qe:', qe
#
#        if qe is not None:
#            url, url1 = search_google(qe)
#            if url0 is None:
#                url0 = url1
#
#    if url is None: # try only russian
#        print '\n!!! try russian'
#
#        qr = clean_eng(q)
#
#        print 'qr:', qr
#
#        if qr is not None:
#            url, url1 = search_google(qr)
#            if url0 is None:
#                url0 = url1

    if url is None:
    #        url = url0 # if not found - return most relevant
        print 'Opening Google Search...'
        url = 'http://google.ru/search?q=%s' % ('site:%s %s' % (SITES[0], to_try_search[0][1]),)

    p('Result URL: %s' % url)

    return url


def search_google(q):
    url, url0 = None, None

    if APPEND_SITE:
        for site in SITES:
            url, url0 = query_google(q + ' site:' + site)
            if url is not None:
                break
    else:
        url, url0 = query_google(q)

    return url, url0


def cp1251_to_utf8(s):
    return s.decode('cp1251').encode('utf-8')


def query_google(q):
    p('Querying Google: q=' + q)

    query = urllib.urlencode({'q': cp1251_to_utf8(q)})
    g_url = u'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=8&%s'.encode("utf-8")\
    % (query,)

    search_results = urllib.urlopen(g_url)
    google_reply = search_results.read()

    #    p('Google reply: \n' + google_reply)

    json = simplejson.loads(google_reply)
    results = json['responseData']['results']

    for res in results:
        print 'url:', res['url']

    url = None

    for site in SITES:
        print '\n>> Checking site:', site

        url = search_for_site(results, site)
        if url is not None:
            break

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


def make_search_string(path, need_file_name):
    n = None

    if not need_file_name:
        if isfile(path):
            dn, fn = split(path)
            _, n = split(dn)
        else: # dir
            _, n = split(path)
    else:
        n = split(path)[1]

        if isfile(path):
            n = splitext(n)[0]

    n_clean = clean(n)

    p('Name: ' + n +
      '\nCleaned: ' + n_clean)

    return n_clean


def clean(q):
    trash_re = '|'.join(r'\[%s\]' % t for t in TRASH)
    trash_re1 = '|'.join(r'\b%s\b' % t for t in TRASH)

    trash_re = '|'.join([trash_re, trash_re1])

#    q = re.sub('(?i)' + trash_re, '', q)
#    q = re.sub('(?i)' + trash_re1, '', q)
    q = re.split('(?i)' + trash_re, q, 1)[0]
    q = re.sub(r'[,.\(\)\[\]\s]+',' ',q)

#    raw_input(q)

    return q.strip().strip(' .,')


def clean_russian(q):
    m = re.match(r'.+(\[.+?\]).+', q)

    if m is not None:
        return q[:m.start(1)] + ' ' + q[m.end(1):]

    return None


def clean_eng(q):
    m = re.match(r'.+(\[.+?\]).+', q)

    if m is not None:
        return q[m.start(1):]

    return None


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
        input()
