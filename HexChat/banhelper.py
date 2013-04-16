import hexchat

__module_name__ = "Banhelper"
__module_author__ = "TingPing"
__module_version__ = "1"
__module_description__ = "Simplifies banning and quieting"

wasop = False

def do_op(deop=False):
	global wasop
	if not deop:
		if not 'o' in hexchat.get_info('modes'):
			wasop = False
			hexchat.command('cs op %s' %hexchat.get_info('channel'))
		else:
			wasop = True
	else:
		if not wasop and 'o' in hexchat.get_info('modes'):
			hexchat.command('cs deop %s' %hexchat.get_info('channel'))
		
def get_mask(nick):
	for user in hexchat.get_list('users'):
		if user.nick == nick:
			if user.account:
				return '$a:%s' %user.account
			elif user.host:
				return '*!*@*%s*' %user.host
			else:
				hexchat.command('who %s %%chtsunfra,152' %nick)
				print('BH: User info not found, enable irc_who_join or try again.')
				return None

def ban_cb(word, word_eol, userdata):
	if len(word) > 1:
		mask = get_mask(word[1])
		if mask:
			do_op()
			if word[0] == 'ban':
				hexchat.command('mode +b %s' %mask)
			elif word[0] == 'kickban':
				hexchat.command('mode +b %s' %mask)
				hexchat.command('kick %s' %word[1])
			elif word[0] == 'quiet':
				hexchat.command('mode +q %s' %mask)
			do_op(deop=True)
			
	return hexchat.EAT_HEXCHAT
		
def unload_cb(userdata):
	print(__module_name__ + ' version ' + __module_version__ + ' unloaded.')

hexchat.hook_command('kickban', ban_cb)
hexchat.hook_command('ban', ban_cb)
hexchat.hook_command('quiet', ban_cb)
hexchat.hook_unload(unload_cb)
print(__module_name__ + ' version ' + __module_version__ + ' loaded.')
