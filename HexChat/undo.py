from __future__ import print_function
from collections import deque
import hexchat

__module_name__ = "undo"
__module_author__ = "TingPing"
__module_version__ = "0"
__module_description__ = "Binds ctrl+z to undo"

undolevels = 10

buffers = {}

def keypress_cb(word, word_eol, userdata):
	global buffers
	buffername = '{}_{}'.format(hexchat.get_info('channel'), hexchat.get_info('network'))

	if not buffername in buffers:
		bufferlist = buffers[buffername] = deque(maxlen=undolevels)
	else:
		bufferlist = buffers[buffername]

	if word[0] == '122' and word[1] == '4': # ctrl+z
		try:
			text = bufferlist.pop()
			hexchat.command('settext {}'.format(text))
			hexchat.command('setcursor {}'.format(len(text)))
		except IndexError: pass
	else:
		bufferlist.append(hexchat.get_info('inputbox'))

def unload_cb(userdata):
	print('{} version {} unloaded'.format(__module_name__, __module_version__))

hexchat.hook_print('Key Press', keypress_cb) 
hexchat.hook_unload(unload_cb)
print('{} version {} loaded'.format(__module_name__, __module_version__))
