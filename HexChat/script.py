import os, urllib
import hexchat

__module_name__ = "Script"
__module_author__ = "TingPing"
__module_version__ = "0"
__module_description__ = "Download scripts"

#TODO: Error handling, multiple sites, custom urls

script_help = 'Script: Valid commands are:\n \
  			INSTALL script\n \
			UPDATE script\n \
			UNINSTALL script'
addon_dir = os.path.join(hexchat.get_info('configdir'), 'addons')
addon_site = 'http://raw.github.com/TingPing/plugins/master/HexChat/'

def script_cb(word, word_eol, userdata):
	if len(word) > 2:
		cmd = word[1].lower()
		arg = word[2]
	else:
		hexchat.command('help script')
		return hexchat.EAT_ALL

	if cmd == 'install':
		if os.path.exists(os.path.join(addon_dir, arg)):
			print('Script: %s is already installed.' %arg)
			return hexchat.EAT_ALL
		urllib.urlretrieve(addon_site + arg, os.path.join(addon_dir, arg))
		hexchat.command('load ' + arg)
	elif cmd == 'update':
		if arg == 'script.py':
			print('Script: I cannot update myself.')
			return hexchat.EAT_ALL
		urllib.urlretrieve(addon_site + arg,os.path.join(addon_dir, arg))
		hexchat.command('reload ' + arg)
	elif cmd == 'uninstall':
		if arg == 'script.py':
			print('Script: I refuse.')
			return hexchat.EAT_ALL
		hexchat.command('unload ' + arg)
		os.remove(os.path.join(addon_dir, arg))
	else:
		hexchat.command('help script')

	return hexchat.EAT_ALL

def unload_callback(userdata):
	print(__module_name__ + ' version ' + __module_version__ + ' unloaded.')

hexchat.hook_command("script", script_cb, help=script_help)
hexchat.hook_unload(unload_callback)
hexchat.prnt(__module_name__ + ' version ' + __module_version__ + ' loaded.')
