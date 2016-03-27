from __future__ import print_function
import hexchat

__module_name__ = "PythonTabComplete"
__module_author__ = "TingPing, FichteFoll"
__module_version__ = "0.3"
__module_description__ = "Tab-completes module attributes in Interactive Console"

last_index = None
last_completes = None
last_text = None
last_pos = None

exec_scope = {}


def keypress_cb(word, word_eol, userdata):
	global last_index
	global last_completes
	global last_text
	global last_pos

	if not word[0] == '65289':  # Tab
		return
	if not hexchat.get_info('channel') == '>>python<<':
		return
	shift_key_is_down = bool(int(word[1]) & 1)  # check if shift modifier is hold

	text = hexchat.get_info('inputbox')
	pos = hexchat.get_prefs('state_cursor')
	if not text:
		return

	base = text[:pos].split(' ')[-1]
	module, _, prefix = base.rpartition('.')
	if not module:
		# can not dir() the console's interpreter state sadly
		return

	if last_text != text or last_pos != pos:
		# new completion context
		try:
			exec('import {}'.format(module), exec_scope)  # Has to be imported to dir() it
			completions = eval('dir({})'.format(module), exec_scope)
		except (NameError, SyntaxError, ImportError):
			return
		completions = [c for c in completions if c.startswith(prefix)]
		if not completions:
			return
		index = 0
	else:
		# same context, insert next completion
		completions = last_completes
		direction = 1 if not shift_key_is_down else -1
		index = (last_index + direction) % len(completions)

	complete_text = completions[index]

	new_text = text[:pos - len(prefix)] + complete_text + text[pos:]
	new_pos = pos - len(prefix) + len(complete_text)

	hexchat.command('settext {}'.format(new_text))
	hexchat.command('setcursor {}'.format(new_pos))

	last_index = index
	last_completes = completions
	last_text = new_text
	last_pos = new_pos


def unload_cb(userdata):
	print(__module_name__, 'version', __module_version__, 'unloaded.')


hexchat.hook_print('Key Press', keypress_cb)
hexchat.hook_unload(unload_cb)
print(__module_name__, 'version', __module_version__, 'loaded.')
