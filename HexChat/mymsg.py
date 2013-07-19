import hexchat

__module_name__ = 'MyMessages'
__module_author__ = 'TingPing'
__module_version__ = '2'
__module_description__ = 'Properly show your messages in znc playback and with privmsg module'

def privmsg_cb(word, word_eol, userdata, attrs):
	mynick = hexchat.get_info('nick')
	sender = word[0].split('!')[0][1:]
	recipient = word[2]
	network = hexchat.get_info('network')
	msg = word_eol[3][1:]

	if hexchat.nickcmp(sender, mynick) == 0:
		if recipient[0] != '#':
			hexchat.command('query -nofocus {}'.format(recipient))
		hexchat.find_context(network, recipient).set()

		if '\001ACTION' in msg:
			msg = msg.strip('\001ACTION')
			msg = msg.strip('\001')
			hexchat.emit_print('Your Action', mynick, msg.strip(), time=attrs.time)
		else:
			hexchat.emit_print_at('Your Message', mynick, msg, time=attrs.time)

		return hexchat.EAT_ALL

hexchat.hook_server_attrs('PRIVMSG', privmsg_cb)
