from __future__ import print_function
import hexchat

__module_name__ = 'NowPlaying'
__module_author__ = 'TingPing'
__module_version__ = '1'
__module_description__ = 'Announce songs from mpris2 clients'

try:
	import dbus
	from dbus.mainloop.glib import DBusGMainLoop
	import pympris
	print(__module_name__, 'version', __module_version__, 'loaded.')
except ImportError:
	print('NP: Please install python-dbus and pympris.')
	hexchat.command('timer 0.1 py unload NowPlaying')

np_help = 'NP [player]'

session_bus = dbus.SessionBus(mainloop=DBusGMainLoop())

def print_nowplaying(mp, echo=False):
	metadata = mp.player.Metadata

	try:
		title = metadata['xesam:title']
		artist = metadata['xesam:artist'][0]
		album = metadata['xesam:album']
	except KeyError:
		print('NP: Song info not found.')
		return

	# TODO: Settings for these
	if echo:
		cmd = 'echo NP: {} by {} on {}.'.format(title, artist, album)
	elif hexchat.get_pluginpref('np_say'):
		cmd = 'say Now playing {} by {} on {}.'.format(title, artist, album)
	else:
		cmd = 'me is now playing {} by {} on {}.'.format(title, artist, album)

	hexchat.command(cmd)

def np_cb(word, word_eol, userdata):
	player_ids = tuple(pympris.available_players())
	player_num = len(player_ids)
	player_names = [pympris.MediaPlayer(_id).root.Identity for _id in player_ids]

	# TODO: commands for next/pause
	if player_num == 0:
		print('NP: No player found running.')
	elif player_num == 1:
		mp = pympris.MediaPlayer(player_ids[0], session_bus)
		print_nowplaying(mp)
	elif len(word) == 2:
		player = word[1]
		if player in player_names:
			index = player_names.index(player)
			mp = pympris.MediaPlayer(player_ids[index])
			print_nowplaying(mp)
		else:
			print('NP: Player {} not found.'.format(player))
	else:
		print('You have multple players running please insert a name:\n\t', ' '.join(player_names))

	return hexchat.EAT_ALL

def unload_cb(userdata):
	print(__module_name__, 'version', __module_version__, 'unloaded.')

hexchat.hook_command('np', np_cb, help=np_help)
hexchat.hook_unload(unload_cb)
