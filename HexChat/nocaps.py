from __future__ import division
import hexchat

__module_name__ = 'NoCaps'
__module_author__ = 'TingPing'
__module_version__ = '2'
__module_description__ = 'Lowercase all cap messages'

cap_percentage = 0.6

events = ['Channel Message', 'Channel Msg Hillight',
  	'Channel Action', 'Channel Action Hillight', 
		'Private Action', 'Private Action to Dialog',
		'Private Message', 'Private Message to Dialog']

def msg_cb(words, word_eol, print_type):
	capwords = 0
	split_words = words[1].split(' ')

	for word in split_words:
		if word.isupper():
			capwords = capwords + 1

	if capwords / len(split_words) > cap_percentage:
		hexchat.emit_print(print_type, words[0], words[1].lower())
		return hexchat.EAT_ALL

for event in events:
	hexchat.hook_print(event, msg_cb, event)
