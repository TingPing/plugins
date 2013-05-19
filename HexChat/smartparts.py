from time import time
import hexchat

__module_name__ = 'SmartParts'
__module_author__ = 'TingPing'
__module_version__ = '0'
__module_description__ = 'Intelligently hide parts, joins, and nick changes'

def check_notify (nick):
	for user in hexchat.get_list('notify'):
		if user.nick == nick:
			return True
		
	return False

def check_lasttalk (nick):
	for user in hexchat.get_list('users'):
		if user.nick == nick:
			if time() - user.lasttalk > 60 * 5:
				return hexchat.EAT_HEXCHAT
			else:
				return hexchat.EAT_NONE

def nick_cb(word, word_eol, userdata):
	if check_notify(word[0]) or check_notify(word[1]):
		return hexchat.EAT_NONE

	return check_lasttalk(word[0])

def join_cb(word, word_eol, userdata):
	if check_notify(word[0]):
		return hexchat.EAT_NONE
	else:
		return hexchat.EAT_HEXCHAT
	#return check_lasttalk(word[0])

def part_cb(word, word_eol, userdata):
	if check_notify(word[0]):
		return hexchat.EAT_NONE

	return check_lasttalk(word[0])


hexchat.hook_print('Quit', part_cb)
hexchat.hook_print('Part', part_cb)
hexchat.hook_print('Part with Reason', part_cb)
hexchat.hook_print('Join', join_cb)
hexchat.hook_print('Change Nick', nick_cb)
