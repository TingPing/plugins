import re
import hexchat

__module_name__ = "Banhelper"
__module_author__ = "TingPing"
__module_version__ = "3"
__module_description__ = "Simplifies banning and quieting"

wasop = False

# Just found these on stackoverflow, hope they work ;)
ipv4re = re.compile(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
ipv6re = re.compile(r'(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,6}\Z)|(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,5}\Z)|(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4}){1,4}\Z)|(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]{1,4}){1,3}\Z)|(\A([0-9a-f]{1,4}:){1,5}(:[0-9a-f]{1,4}){1,2}\Z)|(\A([0-9a-f]{1,4}:){1,6}(:[0-9a-f]{1,4}){1,1}\Z)|(\A(([0-9a-f]{1,4}:){1,7}|:):\Z)|(\A:(:[0-9a-f]{1,4}){1,7}\Z)|(\A((([0-9a-f]{1,4}:){6})(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|(\A(([0-9a-f]{1,4}:){5}[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|(\A([0-9a-f]{1,4}:){5}:[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,3}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4}){1,2}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]{1,4}){1,1}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|(\A(([0-9a-f]{1,4}:){1,5}|:):(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|(\A:(:[0-9a-f]{1,4}){1,5}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)')

def is_ip(host):
	return bool(ipv4re.match(host)) or bool(ipv6re.match(host))

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
			hexchat.command('timer .5 cs deop {}'.format(chan))
		
def get_mask(nick):
	invalid_chars = ['*', '?', '!', '@']
	if any(char in nick for char in invalid_chars):
		return nick # It's already a mask.

	for user in hexchat.get_list('users'):
		if user.nick == nick:
			if user.account:
				return '$a:{}'.format(user.account)
			elif user.host:
				host = user.host.split('@')[1]
				if is_ip(host):
					return '*!*@*{}*'.format(host)
				else:
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
				hexchat.command('timer .3 mode +b {}'.format(mask))
			elif word[0] == 'kickban': 
				hexchat.command('timer .3 mode +b {}'.format(mask))
				hexchat.command('timer .3 kick {}'.format(word[1])) 
			elif word[0] == 'quiet':
				hexchat.command('timer .3 mode +q {}'.format(mask))
			do_op(deop=True)
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
