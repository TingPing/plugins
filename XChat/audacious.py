import dbus
import xchat

__module_name__ = "Audacious"
__module_author__ = "TingPing"
__module_version__ = "0"
__module_description__ = "Announce Audacious Songs"

# May merge with Pithos plugin in future
session_bus = dbus.SessionBus()

def audacious(word, word_eol, userdata):
	try:
		player = session_bus.get_object('org.mpris.audacious', '/Player')
		song = player.GetMetadata()
	except (dbus.exceptions.DBusException, TypeError):
		xchat.prnt('Audacious: Could not find player.')
		return None

	try:
		msg = 'me is now playing %s by %s on %s.'%(song['title'], song['artist'], song['album'])
	except KeyError:
		xchat.prnt('Audacious: Could not find song info.')
		return None

	if len(word) > 1:
		if word[1] == 'info':
			xchat.prnt(msg[18:])
		else:
			xchat.prnt('Audacious: Valid commands are: info, or without args to announce')
	else:
		xchat.command(msg)
	return xchat.EAT_ALL

xchat.hook_command("audacious", audacious)
xchat.hook_command("aud", audacious)
# xchat.hook_command("np", audacious)  # enable if you prefer but may conflict
xchat.prnt(__module_name__ + ' version ' + __module_version__ + ' loaded.')