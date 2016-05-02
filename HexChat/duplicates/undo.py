from __future__ import print_function
from collections import deque
from sys import platform
import xchat as hexchat

__module_name__ = "Undo"
__module_author__ = "TingPing"
__module_version__ = "1"
__module_description__ = "Binds ctrl+z to undo and ctrl+y/shift+ctrl+z to redo."

undolevels = 10
redolevels = 10

undobufs = {}
redobufs = {}

if platform == 'darwin':
	primarymod = 1 << 28
else:
	primarymod = 1 << 2
shiftmod = 1 << 0

def get_valid_mod (mod):
	"""Modifiers are full of junk we dont care about, remove them"""
	return int(mod) & (1 << 0 | 1 << 2 | 1 << 3 | 1 << 28)

def keypress_cb(word, word_eol, userdata):
	global undobufs
	global redobufs
	bufname = '{}_{}'.format(hexchat.get_info('channel'), hexchat.get_info('network'))
	key = word[0]
	mod = get_valid_mod(word[1])
	inputtext = hexchat.get_info('inputbox')

	# Previous strings are stored as deque's in a dict for each channel
	if not bufname in undobufs:
		undobuflist = undobufs[bufname] = deque(maxlen=undolevels)
	else:
		undobuflist = undobufs[bufname]

	if not bufname in redobufs:
		redobuflist = redobufs[bufname] = deque(maxlen=redolevels)
	else:
		redobuflist = redobufs[bufname]

	if (key, mod) == ('122', primarymod): # ctrl+z
		try:
			# Get last saved string
			text = undobuflist.pop()
			if text == inputtext: # First undo may result in same text
				redobuflist.append(text)
				text = undobuflist.pop()
			hexchat.command('settext {}'.format(text))
			hexchat.command('setcursor {}'.format(len(text)))

			redobuflist.append(text)

		except IndexError: pass # No undos left

	elif ((key, mod) == ('121', primarymod) or # ctrl+y
			(key, mod) == ('90', shiftmod|primarymod)): # ctrl+shift+z 
		try:
			text = redobuflist.pop()
			if text == inputtext:
				text = redobuflist.pop()
			hexchat.command('settext {}'.format(text))
			hexchat.command('setcursor {}'.format(len(text)))

		except IndexError: pass

	else:
		# Just throw anything else in here if it has changed
		if not undobuflist or undobuflist[-1] != inputtext:
			undobuflist.append(inputtext)

def unload_cb(userdata):
	print(__module_name__, 'version',  __module_version__, 'unloaded.')

hexchat.hook_print('Key Press', keypress_cb) 
hexchat.hook_unload(unload_cb)
print(__module_name__, 'version',  __module_version__, 'loaded.')
