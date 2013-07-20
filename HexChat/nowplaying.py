import dbus
import hexchat

__module_name__ = "NowPlaying"
__module_author__ = "TingPing"
__module_version__ = "0"
__module_description__ = "Announce Pithos or Audacious Songs"

# This is just me duct-taping two of my scripts together
# Don't expect adding players to this list.

np_help_msg = 'NP: Valid commands are (see /help for specifics):\n \
  				np [option] [value]\n \
					audacious [option]\n \
					audacious [option]\n \
					pithos [option]\n \
					(without args sends to default player)'
					
aud_help_msg = 'AUD: Valid commands are:\n \
					info (prints song)\n \
					(without args sends to chan)'
					
pithos_help_msg = 'PITHOS: Valid commands are:\n \
					info (prints song)\n \
					next (skips song)\n \
					love\n \
					hate\n \
					(without args sends to chan)'

session_bus = dbus.SessionBus()

def get_player(name):
	if name == 'audacious':
		bus_object = ['org.mpris.audacious', '/Player']
	elif name == 'pithos':
		bus_object = ['net.kevinmehall.Pithos', '/net/kevinmehall/Pithos']
	
	try:
		player = session_bus.get_object(bus_object[0], bus_object[1])
		return player
	except (dbus.exceptions.DBusException, TypeError):
		print('NP: Could not find player.')
		return None
		
def print_song(title, artist, album, echo=False):
	# TODO: customization
	if echo:
		cmd = 'echo NP: %s by %s on %s.'%(title, artist, album)
	elif hexchat.get_pluginpref('np_say'):
		cmd = 'say Now playing %s by %s on %s.'%(title, artist, album)
	else:
		cmd = 'me is now playing %s by %s on %s.'%(title, artist, album)
		
	hexchat.command(cmd)
	
			
def audacious_cb(word, word_eol, userdata):
	player = get_player('audacious')
	if not player:
		return hexchat.EAT_ALL
		
	song = player.GetMetadata()

	if len(word) > 1:
		if word[1].lower() == 'info':
			try:
				print_song(song['title'], song['artist'], song['album'], echo=True)
			except KeyError:
				print('NP: Failed to get song information')
		else:
			print('Audacious: Valid commands are: info, or without args to announce')
	else:
		try:
			print_song(song['title'], song['artist'], song['album'])
		except KeyError:
			print('Audacious: Failed to get song information')
	return hexchat.EAT_ALL

def pithos_cb(word, word_eol, userdata):
	player = get_player('pithos')
	if not player:
		return hexchat.EAT_ALL

	song = player.GetCurrentSong()

	if len(word) > 1:
		if word[1].lower() == 'info':
			print_song(song['title'], song['artist'], song['album'], echo=True)
		elif word[1].lower() == 'next':
			player.SkipSong()
		elif word[1].lower() == 'love':
			player.LoveCurrentSong()
		elif word[1].lower() == 'hate':
			player.BanCurrentSong()
		else:
			print('Pithos: Valid commands are: info, next, love, hate, or without args to announce')
	else:
		print_song(song['title'], song['artist'], song['album'])
	return hexchat.EAT_ALL


def np_cb(word, word_eol, userdata):
	if len(word) > 1:
		if len(word) > 2:
			if word[1].lower() == 'default':
				if hexchat.set_pluginpref('np_default', word[2]):
					print('NP: Default set to %s' %word[2])				
			elif word[1].lower() == 'say':
				try:
					if hexchat.set_pluginpref('np_say', bool(int(word[2]))):
						print('NP: Say set to %r' %bool(int(word[2])))
				except ValueError:
					print('NP: Setting must be a 1 or 0')
	else:
		if hexchat.get_pluginpref('np_default'):
			default = hexchat.get_pluginpref('np_default').lower()
		else:
			print('NP: No valid default set, use /np default <player> to set one')
			return hexchat.EAT_ALL	
		if default == 'pithos':
			pithos_cb(word, word_eol, userdata)
		elif default == 'audacious':
			audacious_cb(word, word_eol, userdata)
		else:
			print('NP: No valid default set, use /np default <player> to set one')
	return hexchat.EAT_ALL
	
def unload_cb(userdata):
	print(__module_name__ + ' version ' + __module_version__ + ' unloaded.')

hexchat.hook_command("pithos", pithos_cb, help=pithos_help_msg)
hexchat.hook_command("audacious", audacious_cb, help=aud_help_msg)
hexchat.hook_command("aud", audacious_cb, help=aud_help_msg)
hexchat.hook_command("np", np_cb, help=np_help_msg)
hexchat.hook_unload(unload_cb)
hexchat.prnt(__module_name__ + ' version ' + __module_version__ + ' loaded.')
