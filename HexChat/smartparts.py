from time import time
import hexchat

__module_name__ = 'SmartParts'
__module_author__ = 'TingPing'
__module_version__ = '1'
__module_description__ = 'Intelligently hide parts, joins, autoop, and nick changes'

def check_notify (nick):
	for user in hexchat.get_list('notify'):
		if user.nick == hexchat.strip(nick):
			return True
		
	return False

def check_lasttalk (nick):
	for user in hexchat.get_list('users'):
		if user.nick == hexchat.strip(nick):
			if time() - user.lasttalk > 60 * 5:
				return hexchat.EAT_HEXCHAT
			else:
				return hexchat.EAT_NONE

	return hexchat.EAT_HEXCHAT

def nick_cb(word, word_eol, userdata):
	if check_notify(word[0]) or check_notify(word[1]):
		return hexchat.EAT_NONE

	return check_lasttalk(word[0])

def mode_cb(word, word_eol, userdata):
	if check_notify(word[1]):
		return hexchat.EAT_NONE

	return check_lasttalk(word[1])

def join_cb(word, word_eol, userdata):
	if check_notify(word[0]):
		return hexchat.EAT_NONE
	else:
		return hexchat.EAT_HEXCHAT

def part_cb(word, word_eol, userdata):
	if check_notify(word[0]):
		return hexchat.EAT_NONE

	return check_lasttalk(word[0])

for event in ('Quit', 'Part', 'Part with Reason'):
	hexchat.hook_print(event, part_cb)
for event in ('Channel Operator', 'Channel Voice'):
	hexchat.hook_print(event, mode_cb)
hexchat.hook_print('Join', join_cb)
hexchat.hook_print('Change Nick', nick_cb)
