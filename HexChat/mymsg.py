import hexchat

__module_name__ = 'MyMessages'
__module_author__ = 'TingPing'
__module_version__ = '1'
__module_description__ = 'Properly show your messages in znc playback and with privmsg module'

def is_me(nick):
	if hexchat.nickcmp(nick, hexchat.get_info('nick')) == 0:
		return True
	else:
		return False

def print_cb(word, word_eol, print_type):
	if is_me(word[0]):
		hexchat.emit_print(print_type, word[0], word[1])
		return hexchat.EAT_ALL

# This could use some improvement..
def privmsg_cb(word, word_eol, userdata):
	if is_me(word[0].split('!')[0][1:]):
		hexchat.command('query -nofocus {}'.format(word[2]))
		ctx = hexchat.find_context(hexchat.get_info('network'), word[2])
		ctx.emit_print('Your Message', hexchat.get_info('nick'), word_eol[3][1:])
		return hexchat.EAT_ALL

hexchat.hook_print('Channel Message', print_cb, 'Channel Message')
hexchat.hook_print('Channel Action', print_cb, 'Channel Action')
hexchat.hook_server('PRIVMSG', privmsg_cb)
