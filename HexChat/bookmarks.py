import hexchat

__module_name__ = "Bookmarks"
__module_author__ = "TingPing"
__module_version__ = "1"
__module_description__ = "Bookmark channels to easily rejoin them."

def get_network(name):
	return hexchat.get_pluginpref('bookmark_' + name)

def load_bookmarks():
	hexchat.command('menu -p-2 add "$TAB/Bookmark" "bookmark %s"')
	hexchat.command('menu add "$CHAN/Bookmark Channel" "bookmark %s"')
	hexchat.command('menu -p3 add "Bookmarks"')
	hexchat.command('menu add "Bookmarks/-"')
	hexchat.command('menu add "Bookmarks/Add or Remove Current Channel" "bookmark"')
	for pref in hexchat.list_pluginpref():
		if pref[:9] == 'bookmark_':
			chan = pref[9:]
			net = get_network(chan)
			hexchat.command('menu -p-2 add "Bookmarks/{}'.format(net))
			hexchat.command('menu add "Bookmarks/{0}/{1}" "netjoin {1} {0}"'.format(net, chan))

def toggle_bookmark(chan, net): # It's a toggle because /menu sucks
	if chan == None:
		chan = hexchat.get_info('channel')
	if net == None:
		try: # If from a $TAB it may be a different network.
			net = hexchat.find_context(None, chan).get_info('network')
		except AttributeError:
			net = hexchat.get_info('network')

	if get_network(chan) == net:
		hexchat.del_pluginpref('bookmark_' + chan)
		hexchat.command('menu del "Bookmarks/{}/{}"'.format(net, chan))
	else:
		hexchat.set_pluginpref('bookmark_' + chan, net)
		hexchat.command('menu -p-2 add "Bookmarks/{}'.format(net))
		hexchat.command('menu add "Bookmarks/{0}/{1}" "netjoin {1} {0}"'.format(net, chan))

def netjoin_cb(word, word_eol, userdata):
	joinchan = word[1]
	joinnet = word_eol[2]

	for chan in hexchat.get_list('channels'):
		if chan.network == joinnet:
			chan.context.command('join {}'.format(joinchan))
			return hexchat.EAT_ALL

	# Not found, connect to network automatically.
	hexchat.command('url irc://"{}"/{}'.format(joinnet, joinchan))
	return hexchat.EAT_ALL
	
def bookmark_cb(word, word_eol, userdata):
	chan = None
	net = None

	try:
		chan = word[1]
		net = word[2]
	except IndexError:
		pass

	toggle_bookmark(chan, net)

	return hexchat.EAT_ALL
		
def unload_callback(userdata):
	hexchat.command('menu del "Bookmarks"')
	hexchat.command('menu del "$TAB/Bookmark"')
	hexchat.command('menu del "$CHAN/Bookmark Channel"')
	print(__module_name__ + ' version ' + __module_version__ + ' unloaded.')

hexchat.hook_command("bookmark", bookmark_cb, help='Usage: bookmark [channel] [network]\n\tToggles a bookmark.')
hexchat.hook_command("netjoin", netjoin_cb, help='netjoin <channel> <network>')
hexchat.hook_unload(unload_callback)
load_bookmarks()
print(__module_name__ + ' version ' + __module_version__ + ' loaded.')
