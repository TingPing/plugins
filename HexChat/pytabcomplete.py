from __future__ import print_function
import hexchat

__module_name__ = "PythonTabComplete"
__module_author__ = "TingPing"
__module_version__ = "0"
__module_description__ = "Tab completes modules in Interactive Console"

lastmodule = ''
lastcomplete = 0
lasttext = ''

def keypress_cb(word, word_eol, userdata):
  global lastmodule
	global lastcomplete
	global lasttext

	if not word[0] == '65289': # Tab
		return
	if not hexchat.get_info('channel') == '>>python<<':
		return

	text = hexchat.get_info('inputbox')
	#pos = hexchat.get_prefs('state_cursor') # TODO: allow completing mid line
	if not text:# or not pos:
		return

	try:
		module = text.split(' ')[-1].split('.')[0]
	except IndexError:
		return

	if lastmodule != module:
		lastcomplete = 0
		lasttext = text
	lastmodule = module

	try:
		exec('import {}'.format(module)) # Has to be imported to dir() it
		completes = eval('dir({})'.format(module))
		if lastcomplete + 1 < len(completes):
			lastcomplete = lastcomplete + 1
		else:
			lastcomplete = 0
	except (NameError, SyntaxError, ImportError):
		return

	if lasttext[-1] != '.':
		sep = '.'
	else:
		sep = ''
	
	newtext	= lasttext + sep + completes[lastcomplete]

	hexchat.command('settext {}'.format(newtext))
	hexchat.command('setcursor {}'.format(len(newtext)))

def unload_cb(userdata):
	print(__module_name__, 'version', __module_version__, 'unloaded.')

hexchat.hook_print('Key Press', keypress_cb)
hexchat.hook_unload(unload_cb)
print(__module_name__, 'version', __module_version__, 'loaded.')
