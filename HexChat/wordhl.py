import hexchat

__module_name__ = 'wordhl'
__module_author__ = 'TingPing'
__module_version__ = '1'
__module_description__ = 'Highlights some words of importance'
# When you want to notice something, but not really get 'highlighted'

hlwords = ('hexchat', )
edited = False

def print_cb(word, word_eol, event, attr):
	global edited
	# Ignore our own events, bouncer playback, empty messages
	if edited or attr.time or not len(word) > 1:
		return

	if any(_word in word[1] for _word in hlwords):
		msg = word[1]
		for _word in hlwords:
			msg = msg.replace(_word, '\00320' + _word + '\00399').strip() # Color red

		edited = True
		hexchat.emit_print(event, word[0], msg)
		edited = False

		hexchat.command('gui color 3')
		return hexchat.EAT_ALL

hexchat.hook_print_attrs('Channel Message', print_cb, 'Channel Message', priority=hexchat.PRI_HIGH)
hexchat.hook_print_attrs('Channel Action', print_cb, 'Channel Action', priority=hexchat.PRI_HIGH)
