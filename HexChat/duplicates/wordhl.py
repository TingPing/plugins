import re
import hexchat

__module_name__ = 'wordhl'
__module_author__ = 'TingPing'
__module_version__ = '2'
__module_description__ = 'Highlights some words of importance'
# When you want to notice something, but not really get 'highlighted'

# Case insensitive words
hlwords = ('hexchat', )

# Don't touch
edited = False

def print_cb(word, word_eol, event, attr):
	global edited
	# Ignore our own events, bouncer playback, empty messages
	if edited or attr.time or not len(word) > 1:
		return

	msg = word[1]
	for _word in hlwords:
		# Color red
		msg = re.sub(_word, '\00320' + _word + '\00399', msg, flags=re.I)

	if msg != word[1]: # Something replaced
		edited = True
		word = [(word[i] if len(word) > i else '') for i in range(4)]
		hexchat.emit_print(event, word[0], msg, word[2], word[3])
		edited = False

		hexchat.command('gui color 3')
		return hexchat.EAT_ALL

hexchat.hook_print_attrs('Channel Message', print_cb, 'Channel Message', priority=hexchat.PRI_HIGH)
hexchat.hook_print_attrs('Channel Action', print_cb, 'Channel Action', priority=hexchat.PRI_HIGH)
