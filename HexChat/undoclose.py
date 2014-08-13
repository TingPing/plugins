from sys import platform
from collections import deque
import hexchat

__module_name__ = "Undo Close"
__module_version__ = "0.1"
__module_description__ = "Adds keybinding to undo close tab"
__module_author__ = "TingPing"

if platform == 'win32':
	shiftctrlmod = '5'
elif platform == 'darwin':
	shiftctrlmod = '268435473'
else:
	shiftctrlmod = '21'

close_history = deque(maxlen=30)

def contextclosed_cb(word, word_eol, userdata):
	global close_history

	ctx = hexchat.get_context()
	for chan in hexchat.get_list('channels'):
		if chan.context == ctx:
			if chan.type != 2: # Only want channels
				return

	net = hexchat.get_info('network')
	if not net:
		net = hexchat.get_info('server')
	if not net:
		return
	
	chan = hexchat.get_info('channel')
	if not chan:
		return

	close_history.append('irc://{}/{}'.format(net, chan))

def keypress_cb(word, word_eol, userdata):
	global close_history

	key, mod = word[0], word[1]
	
	if (key, mod) == ('84', shiftctrlmod): # Ctrl+Shift+t
		try:
			last = close_history.pop()
			hexchat.command('url {}'.format(last))
		except IndexError:
			pass

hexchat.hook_print("Close Context", contextclosed_cb)
hexchat.hook_print('Key Press', keypress_cb)
