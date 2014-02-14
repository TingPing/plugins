import xchat as hexchat

__module_name__ = "LogPMs"
__module_author__ = "TingPing"
__module_version__ = "2"
__module_description__ = "Auto log pm's"

def open_cb(word, word_eol, userdata):
	chan = hexchat.get_info('channel')
	# Assume nick if not prefixed with #
	# Ignore ZNC and Python
	# Use existing pref for nicks I usually ignore (i.e. chanserv)
	if chan and chan[0] != '#' \
		and chan[0] != '*' \
		and chan != '>>python<<' \
		and chan not in hexchat.get_prefs('irc_no_hilight').split(','):
		hexchat.command('chanopt -quiet text_logging on')
		hexchat.command('chanopt -quiet text_scrollback on')

hexchat.hook_print("Open Context", open_cb)
