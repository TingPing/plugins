from __future__ import print_function
import os
import sys
if sys.version_info[0] < 3:
	import urllib as request
else:
	import urllib.request as request
import hexchat

__module_name__ = 'Script'
__module_author__ = 'TingPing'
__module_version__ = '3'
__module_description__ = 'Download scripts'

script_help = 'Script: Valid commands are:\n \
			INSTALL script\n \
			EDIT script\n \
			UPDATE script\n \
			REMOVE script'

addon_dir = os.path.join(hexchat.get_info('configdir'), 'addons')

# Store as preference?
addon_types = ('py', 'pl', 'lua', 'js') # tcl has no way to unload a single script?
addon_sites = ('http://raw.github.com/TingPing/plugins/master/HexChat/',
				'http://raw.github.com/Arnavion/random/master/hexchat/',
				'http://orvp.net/xchat/')


def expand_script(script):
	return os.path.join(addon_dir, script)


def download(script):
	if script.partition('.')[2] not in addon_types:
		print('Script: Not a valid script file type.')
		return False
	for site in addon_sites:
		if request.urlopen(site + script).getcode() == 200:
			print('Script: Downloading {}...'.format(script))
			request.urlretrieve(site + script, expand_script(script))
			return True
	print('Script: Could not find {}'.format(script))


def script_cb(word, word_eol, userdata):
	if len(word) > 2:
		cmd = word[1].lower()
		arg = word[2]
	else:
		hexchat.command('help script')
		return hexchat.EAT_ALL

	if cmd == 'install':
		if os.path.exists(expand_script(arg)):
			print('Script: {} is already installed.'.format(arg))
			return hexchat.EAT_ALL
		if download(arg):
			hexchat.command('timer .5 load ' + expand_script(arg))
	elif cmd == 'update':
		if os.path.exists(expand_script(arg)) and download(arg):
			hexchat.command('timer .5 unload ' + arg)
			hexchat.command('timer 1 load ' + arg)
	elif cmd == 'edit':
		hexchat.command('url ' + expand_script(arg))
	elif cmd == 'remove':
		if arg == 'script.py':
			print('Script: I refuse.')
			return hexchat.EAT_ALL
		if os.path.exists(expand_script(arg)):
			hexchat.command('unload ' + expand_script(arg))
			os.remove(expand_script(arg))
		else:
			print('Script: {} is not installed.'.format(arg))
	else:
		hexchat.command('help script')

	return hexchat.EAT_ALL


def unload_callback(userdata):
	print(__module_name__, 'version', __module_version__, 'unloaded.')

hexchat.hook_command('script', script_cb, help=script_help)
hexchat.hook_unload(unload_callback)
print(__module_name__, 'version', __module_version__, 'loaded.')
