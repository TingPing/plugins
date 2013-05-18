from time import time
import hexchat

__module_name__ = 'SmartParts'
__module_author__ = 'TingPing'
__module_version__ = '0'
__module_description__ = 'Intelligently hide parts'

def join_cb(word, word_eol, userdata):
  return hexchat.EAT_HEXCHAT

def part_cb(word, word_eol, userdata):
	nick = word[0]
	lasttalk = 0
	for user in hexchat.get_list('users'):
		if user.nick == nick:
			lasttalk = user.lasttalk
			break

	if time() - lasttalk > 60 * 5:
		return hexchat.EAT_HEXCHAT

hexchat.hook_print('Quit', part_cb)
hexchat.hook_print('Part', part_cb)
hexchat.hook_print('Part with Reason', part_cb)
hexchat.hook_print('Join', join_cb)
