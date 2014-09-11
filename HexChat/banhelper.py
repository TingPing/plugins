import hexchat

__module_name__ = "Banhelper"
__module_author__ = "TingPing"
__module_version__ = "5"
__module_description__ = "Simplifies banning and quieting"

wasop = False

def is_op():
	for user in hexchat.get_list('users'):
		if user.nick == hexchat.get_info('nick'):
			if user.prefix == '@':
				return True
			else:
				return False

def do_op(deop=False):
	global wasop
	chan = hexchat.get_info('channel')

	if not deop:
		if not is_op():
			wasop = False
			hexchat.command('cs op {}'.format(chan))
		else:
			wasop = True
	else:
		if not wasop:
			hexchat.command('cs deop {}'.format(chan))

def do_command(cmd):
	if is_op():
		hexchat.command(cmd)
		do_op(deop=True)
		return False

	return True
		
def get_mask(nick):
	invalid_chars = ('*', '?', '!', '@', '$')
	if any(char in nick for char in invalid_chars):
		return nick # It's already a mask.

	for user in hexchat.get_list('users'):
		if hexchat.nickcmp(user.nick, nick) == 0:
			if user.account:
				return '$a:{}'.format(user.account)
			elif user.host:
				host = user.host.split('@')[1]
				return '*!*@{}'.format(host)
			else:
				hexchat.command('whois {}'.format(nick))
				print('BH: User info not found, enable irc_who_join or try again.')
				return None

def ban_cb(word, word_eol, userdata):
	if len(word) > 1:
		mask = get_mask(word[1])

		if mask:
			do_op()

			if word[0] == 'ban':
				command = 'mode +b {}'.format(mask)
			elif word[0] == 'kickban':
				nick = word[1]
				chan = hexchat.get_info('channel')
				message = word_eol[2] if len(word_eol) > 2 else ""

				command = 'mode +b {}\r\nKICK {} {} :{}'.format(mask, chan, nick, message)
			elif word[0] == 'quiet':
				command = 'mode +q {}'.format(mask)

			hexchat.hook_timer(100, do_command, command)

		return hexchat.EAT_HEXCHAT
	else:			
		return hexchat.EAT_NONE
		
def unload_cb(userdata):
	print(__module_name__ + ' version ' + __module_version__ + ' unloaded.')

hexchat.hook_command('kickban', ban_cb) 
hexchat.hook_command('ban', ban_cb)
hexchat.hook_command('quiet', ban_cb)
hexchat.hook_unload(unload_cb)
print(__module_name__ + ' version ' + __module_version__ + ' loaded.')
