from __future__ import print_function
import sys
import json
import re

if sys.version_info[0] == 2:
	import HTMLParser as htmlparser
	import urllib as request
	from cgi import escape
else:
	import html.parser as htmlparser
	import urllib.request as request
	from html import escape

import hexchat

__module_name__ = 'Define'
__module_author__ = 'TingPing'
__module_version__ = '2'
__module_description__ = 'Show word definitions'

help_str = 'Define Usage: /define word [number]\n\tnumber being alternate definition'

# From http://blog.abhijeetr.com/2011/11/google-dictionary-api-example-in-python.html
def asciirepl(match):
	s = match.group()  
	return '\\u00' + match.group()[2:]

def define(word, word_eol, userdata):

	if len(word) >= 2:
		define_word = hexchat.strip(word[1])
		definition_number = 1
		if len(word) >= 3:
			definition_number = int(hexchat.strip(word[2]))
	else:
		print(help_str)
		return hexchat.EAT_ALL

	url = 'http://www.google.com/dictionary/json?callback=s&q={}&sl=en&tl=en&restrict=pr,de&client=te'.format(escape(define_word))
	response = request.urlopen(url)
	content = response.read()[2:-10].decode('utf-8')
	ascii = re.compile(r'\\x(\w{2})')
	content = ascii.sub(asciirepl, content)
	response.close()
	
	parser = htmlparser.HTMLParser()
	dic = json.loads(content)
	if 'webDefinitions' in dic:
		try:
			entry = dic['webDefinitions'][0]['entries'][definition_number - 1]
			if entry['type'] == 'meaning':
				definition = entry['terms'][0]['text']
				print('\002{}\017: {}'.format(define_word, parser.unescape(definition)))
		except IndexError:
			print('Alternate definition {} unavailable for {}'.format(definition_number, define_word))
	else:
		print('Definition unavailable for {}'.format(define_word))
	
	return hexchat.EAT_ALL

hexchat.hook_command('define', define, help=help_str)
print(__module_name__, 'version',  __module_version__, 'loaded.')
