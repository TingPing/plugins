import dbus
import xchat

__module_name__ = "Pithos"
__module_author__ = "TingPing"
__module_version__ = "2"
__module_description__ = "Announce Pithos Songs"

session_bus = dbus.SessionBus()

def pithos(word, word_eol, userdata):
	try:
		player = session_bus.get_object('net.kevinmehall.Pithos', '/net/kevinmehall/Pithos')
	except (dbus.exceptions.DBusException, TypeError):
		xchat.prnt('Pithos: Could not find player.')
		return None

	song = player.GetCurrentSong()
	# to be configurable
	msg = 'me is now playing %s by %s on %s.'%(song['title'], song['artist'], song['album'])

	if len(word) > 1:
		# not very useful?
		if word[1] == 'info':
			xchat.prnt(msg[18:])

		elif word[1] == 'next':
			player.SkipSong()

		elif word[1] == 'love':
			player.LoveCurrentSong()

		elif word[1] == 'hate':
			player.BanCurrentSong()

		else:
			xchat.prnt('Pithos: Valid commands are: info, next, love, hate, or without args to announce')
	else:
		xchat.command(msg)
	return xchat.EAT_ALL

xchat.hook_command("pithos", pithos)
# xchat.hook_command("np", pithos)  # enable if you prefer but may conflict
xchat.prnt(__module_name__ + ' version ' + __module_version__ + ' loaded.')