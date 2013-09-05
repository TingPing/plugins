from __future__ import print_function
import xchat as hexchat

__module_name__ = "session"
__module_author__ = "TingPing"
__module_version__ = "0"
__module_description__ = "Saves current session for next start"
# To use just disable auto-connect and start using 'Quit and Save' from the menu.

def load_session():
	for pref in hexchat.list_pluginpref():
		if len(pref) > 8 and pref[:8] == 'session_':
			network = pref[8:]
			channels = hexchat.get_pluginpref('session_' + network).split(',')
			hexchat.command('url irc://"{}"/'.format(network)) # Using url avoids autojoin
			hexchat.find_context(server=network).set()
			delay = hexchat.get_prefs('irc_join_delay') + 10
			for chan in channels:
				if chan[0] != '#':
					hexchat.command('timer {} query -nofocus {}'.format(delay, chan))
				else:
					hexchat.command('timer {} join {}'.format(delay, chan))

			hexchat.del_pluginpref('session_' + network)

def quit_cb(word, word_eol, userdata):
	networks = {}

	for chan in hexchat.get_list('channels'):
		if chan.type != 1:
			if not chan.network in networks:
				networks[chan.network] = []
			networks[chan.network].append(chan.channel)

	for network, channels in networks.items():
		hexchat.set_pluginpref('session_' + network, ','.join(channels))
		hexchat.find_context(server=network).command('quit')
		
	hexchat.command('killall')

def unload_cb(userdata):
	print(__module_name__, 'version', __module_version__, 'unloaded.')

load_session()
hexchat.hook_command('quitandsave', quit_cb)
hexchat.hook_unload(unload_cb)
hexchat.command('menu -p-1 add "HexChat/Quit and Save" "quitandsave"')
print(__module_name__, 'version', __module_version__, 'loaded.')
