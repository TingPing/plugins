import xchat as hexchat

__module_name__ = 'ServerPass'
__module_author__ = 'TingPing'
__module_version__ = '1'
__module_description__ = 'Alows using server password with another login method'
# This works around 2.9.6+'s new login methods

networks = ('freenode', )

def connected_cb(word, word_eol, userdata):
	if hexchat.get_info('network') in networks:
		username = hexchat.get_prefs ('irc_user_name')
		password = hexchat.get_info('password')
		hexchat.command('quote PASS {}:{}'.format(username, password))

hexchat.hook_print('Connected', connected_cb)
