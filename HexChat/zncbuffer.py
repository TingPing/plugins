import hexchat

__module_name__ = 'ZNC Buffers'
__module_author__ = 'fladd & TingPing'
__module_version__ = '1.0'
__module_description__ = 'Add menu options to manage ZNC buffers'

# TODO:
#   Don't run on non-znc networks
#   Actually check for channel type

recently_cleared = []

def privmsg_cb(word, word_eol, userdata):
	# ZNC helpfully tells us what we just did.. so lets hide that spam
	if word[0] == ':*status!znc@znc.in' and len(word_eol) > 4 and word_eol[4].startswith('buffers matching'):
		cleared = word[6][1:-1] # [nick]
		if cleared in recently_cleared:
			recently_cleared.remove(cleared)
			return hexchat.EAT_ALL

def clearbuffer_cmd_cb(word, word_eol, userdata):
	# We just want to track which one is cleared by menu to silence it
	name = word[1]

	# Ignore ZNC queries and channels
	if name[0] != '*':
		recently_cleared.append(name)
		hexchat.command('znc clearbuffer {}'.format(name))

	return hexchat.EAT_ALL

def unload_cb(userdata):
	# Remove menu entries
	hexchat.command('menu del "$TAB/ZNC"')

hexchat.command('menu -p4 add "$TAB/ZNC"')
hexchat.command('menu add "$TAB/ZNC/Clear Buffer" ".zncclearbuffer %s"')
hexchat.command('menu add "$TAB/ZNC/Play Buffer" "znc playbuffer %s"')
hexchat.hook_unload(unload_cb)
hexchat.hook_command('.zncclearbuffer', clearbuffer_cmd_cb)
hexchat.hook_server('PRIVMSG', privmsg_cb)
