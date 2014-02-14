import hexchat

__module_name__ = 'Twitch'
__module_author__ = 'TingPing'
__module_version__ = '3'
__module_description__ = 'Better integration with Twitch.tv'
# Very much a work in progress...

# Commands from http://help.twitch.tv/customer/portal/articles/659095-chat-moderation-commands
# /ban may conflict with other scripts nothing we can do about that
# /clear is an existing command, just override it
commands = ('timeout', 'slow', 'slowoff', 'subscribers', 'subscribersoff',
			'mod', 'unmod', 'mods', 'clear', 'ban', 'unban', 'commercial',
			'r9kbeta', 'r9kbetaoff', 'color')

aliases = {'op':'mod', 'deop':'unmod'}

def twitchOnly(func):
	def if_twitch(*args, **kwargs):
		server = hexchat.get_info('server')
		if server and ('twitch.tv' in server or 'justin.tv' in server):
			return func(*args, **kwargs)
		else:
			return hexchat.EAT_NONE
	return if_twitch

# Twitch returns a lot of 'unknown command' errors, ignore them.
@twitchOnly
def servererr_cb(word, word_eol, userdata):
	return hexchat.EAT_ALL

# Print jtv messages in server tab.
@twitchOnly
def privmsg_cb(word, word_eol, userdata):
	if word[0][1:].split('!')[0] == 'jtv':
		for chan in hexchat.get_list('channels'):
			if chan.type == 1 and chan.id == hexchat.get_prefs('id'):
				chan.context.set()
		hexchat.emit_print('Server Text', word_eol[3][1:])
		return hexchat.EAT_ALL

# Eat any message starting with a '.', twitch eats all of them too.
@twitchOnly
def yourmsg_cb(word, word_eol, userdata):
	if word[1][0] == '.':
		return hexchat.EAT_ALL

# Just prefix with a '.'.
@twitchOnly
def command_cb(word, word_eol, alias):
	if alias:
		if len(word_eol) > 1:
			hexchat.command('say .{} {}'.format(alias, word_eol[1]))
		else:
			hexchat.command('say .{}'.format(alias))
	else:
		hexchat.command('say .{}'.format(word_eol[0]))
	return hexchat.EAT_ALL

for command in commands:
	hexchat.hook_command(command, command_cb)
for command, alias in aliases.items():
	hexchat.hook_command(command, command_cb, alias)
hexchat.hook_print('Your Message', yourmsg_cb)
hexchat.hook_server('421', servererr_cb)
hexchat.hook_server('PRIVMSG', privmsg_cb)
