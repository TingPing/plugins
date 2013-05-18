from time import time
import hexchat

__module_name__ = 'SmartParts'
__module_author__ = 'TingPing'
__module_version__ = '0'
__module_description__ = 'Intelligently hide parts'

def join_cb(word, word_eol, userdata):
  return hexchat.EAT_HEXCHAT

def part_cb(word, word_eol, userdata):
	for user in hexchat.get_list('users'):
		if user.nick == word[0]:
			if time() - user.lasttalk > 60 * 5:
				return hexchat.EAT_HEXCHAT
			else
				return hexchat.EAT_NONE


hexchat.hook_print('Quit', part_cb)
hexchat.hook_print('Part', part_cb)
hexchat.hook_print('Part with Reason', part_cb)
hexchat.hook_print('Join', join_cb)
