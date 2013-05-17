import hexchat

__module_name__ = "LogPMs"
__module_author__ = "TingPing"
__module_version__ = "1"
__module_description__ = "Auto log pm's"

def open_cb(word, word_eol, userdata):
	chan = hexchat.get_info('channel')
	# Assume nick if not prefixed with #
	# Use existing pref for nicks I usually ignore (i.e. chanserv)
	if chan and chan[0] != '#' and chan not in hexchat.get_prefs('irc_no_hilight'):
		hexchat.command('chanopt text_logging on')

hexchat.hook_print("Open Context", open_cb)
