import hexchat

__module_name__ = 'autoclearbuf'
__module_author__ = 'fladd & TingPing'
__module_version__ = '1.0'
__module_description__ = 'Auto clear buffer of closed queries with znc'

# TODO:
#   Don't run on non-znc networks
#   Actually check for channel type (currently crashes)

recently_cleared = []

def privmsg_cb(word, word_eol, userdata):
	# ZNC helpfully tells us what we just did.. so lets hide that spam
	if word[0] == ':*status!znc@znc.in' and word_eol[4].startswith('buffers matching'):
		cleared = word[6][1:-1] # [nick]
		if cleared in recently_cleared:
			recently_cleared.remove(cleared)
			return hexchat.EAT_ALL

def close_cb(word, word_eol, userdata):
	name = hexchat.get_info('channel')

	# Ignore ZNC queries and channels
	if name[0] != '*' and name[0] != '#':
		recently_cleared.append(name)
		hexchat.command('znc clearbuffer {}'.format(name))

hexchat.hook_print('Close Context', close_cb)
hexchat.hook_server('PRIVMSG', privmsg_cb)
