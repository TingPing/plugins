import hexchat

__module_name__ = "Alias"
__module_author__ = "TingPing"
__module_version__ = "1"
__module_description__ = "Create aliases for commands"

help_msg = 'Alias: Valid commands are:\n \
					ALIAS name command\n \
					UNALIAS name\n \
					ALIASES\n \
					HELP name'

def load_aliases ():
	for pref in hexchat.list_pluginpref():
		if pref[:6] == 'alias_':
			name = pref[6:]
			hexchat.hook_command(name, alias_cmd_cb, help='Alias: "%s" is an alias for "%s"' %(name, get_alias(name)))

def get_alias(name):
	cmd = hexchat.get_pluginpref('alias_' + name)
	return cmd

def remove_alias(name, quiet=False):
	hexchat.del_pluginpref('alias_' + name)
	if hexchat.unhook(hook):
		return True
	return False


def add_alias(name, cmd):
	hexchat.set_pluginpref('alias_' + name, cmd)
	if hexchat.hook_command(name, alias_cmd_cb, help='Alias: "%s" is an alias for "%s"' %(name, get_alias(name))):
		return True
	return False


def alias_cmd_cb(word, word_eol, userdata):
	hexchat.command('%s %s' %(get_alias(word[0]), word_eol[1]))
	return hexchat.EAT_HEXCHAT

def unalias_cb(word, word_eol, userdata):
	if len(word) > 1:
		if remove_alias(word[1]):
			print('Alias: %s removed' %word[1])
		else:
			print('Alias: %s not found' %word[1])
	else:
		hexchat.prnt('Alias: Not enough arguements')
	return hexchat.EAT_ALL
	
def alias_cb(word, word_eol, userdata):
	if len(word) > 3:
		edited = False
		if remove_alias(word[1], True):
			edited = True
		if add_alias(word[1], word_eol[2]):
			if edited:
				print('Alias: %s edited' %word[1])
			else:
				print('Alias: %s added' %word[1])
		else:
			print('Alias: %s failed to hook' %word[1])
	else:		
		print(help_msg)
	return hexchat.EAT_ALL

# FIXME: Formatting
def aliases_cb(word, word_eol, userdata):
	print('\026NAME\t\t\t\tCMD                                                     ')
	for pref in hexchat.list_pluginpref():
		if pref[:6] == 'alias_':
			print('%s\t\t\t%s' %(pref[6:], get_alias(pref[6:])))
	return hexchat.EAT_ALL
		
def unload_callback(userdata):
	print(__module_name__ + ' version ' + __module_version__ + ' unloaded.')

hexchat.hook_command("alias", alias_cb, help=help_msg)
hexchat.hook_command("aliases", aliases_cb, help=help_msg)
hexchat.hook_command("unalias", unalias_cb, help=help_msg)
hexchat.hook_unload(unload_callback)
load_aliases()
print(__module_name__ + ' version ' + __module_version__ + ' loaded.')
