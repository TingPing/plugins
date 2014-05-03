import hexchat

__module_name__ = 'MyMessages'
__module_author__ = 'TingPing'
__module_version__ = '3'
__module_description__ = 'Properly show your messages in ZNC'

def privmsg_cb(word, word_eol, userdata, attrs):
	# We only care about private messages, HexChat handles the rest now.
	if word[2][0] == '#':
		return

	mynick = hexchat.get_info('nick')
	sender = word[0].split('!')[0][1:]
	recipient = word[2]
	network = hexchat.get_info('network')
	msg = word_eol[3][1:]

	if hexchat.nickcmp(sender, mynick) == 0 and hexchat.nickcmp(recipient, mynick) != 0:
		hexchat.command('query -nofocus {}'.format(recipient))
		ctx = hexchat.find_context(network, recipient)

		if '\001ACTION' in msg:
			for repl in ('\001ACTION', '\001'):
				msg = msg.replace(repl, '')
			ctx.emit_print('Your Action', mynick, msg.strip(), time=attrs.time)
		else:
			ctx.emit_print('Your Message', mynick, msg, time=attrs.time)

		return hexchat.EAT_ALL

hexchat.hook_server_attrs('PRIVMSG', privmsg_cb)
