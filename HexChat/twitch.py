import hexchat

__module_name__ = 'Twitch'
__module_author__ = 'TingPing'
__module_version__ = '1'
__module_description__ = 'Better integration with Twitch.tv'
# Very much a work in progress...

# Best used with my 'mymsg.py' script so you can sync your messages with the web clients.

# Commands from http://help.twitch.tv/customer/portal/articles/659095-chat-moderation-commands
# /ban may conflict with other scripts nothing we can do about that
# /clear is an existing command, just override it
commands = ('timeout', 'slow', 'slowoff', 'subscribers', 'subscribersoff',
			'mod', 'unmod', 'mods', 'clear', 'ban', 'unban', 'commercial')

aliases = {'op':'mod', 'deop':'unmod'}

def is_twitch():
	if 'twitch.tv' in hexchat.get_info('server'):
		return True
	else: return False

# Twitch returns a lot of 'unknown command' errors, ignore them.
def servererr_cb(word, word_eol, userdata):
	if is_twitch():
		return hexchat.EAT_ALL

# Print jtv messages in server tab.
def privmsg_cb(word, word_eol, userdata):
	if is_twitch():
		if word[0][1:4] == 'jtv':
			hexchat.find_context(channel=hexchat.get_info('network')).set()
			hexchat.emit_print('Server Text', word_eol[3][1:])
			return hexchat.EAT_ALL

# Eat any message starting with a '.', twitch eats all of them too.
def yourmsg_cb(word, word_eol, userdata):
	if is_twitch() and word[1][0] == '.':
		return hexchat.EAT_ALL

# Just prefix with a '.'.
def command_cb(word, word_eol, alias):
	if is_twitch():
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
