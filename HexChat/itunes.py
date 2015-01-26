from __future__ import print_function
import hexchat

__module_name__ = 'iTunes'
__module_author__ = 'TingPing'
__module_version__ = '0'
__module_description__ = 'Announces current song playing in iTunes for Windows'

loaded = False
try:
	import win32com.client
	import pywintypes
	loaded = True
	print(__module_name__, 'version', __module_version__, 'loaded.')
except ImportError:
	print('You must install pywin32')
	hexchat.command('timer 0.1 py unload iTunes')

def np_cb(word, word_eol, userdata):
	try:
		itunes = win32com.client.Dispatch('iTunes.Application')
	except pywintypes.com_error:
		print("itunes: Failed to communicate with itunes. Note that this requires admin access and you should have had a UAC prompt.")
		return hexchat.EAT_ALL

	# TODO: Settings
	try:
		track = itunes.CurrentTrack
		hexchat.command('me is now playing {} by {} on {}'.format(track.Name, track.Artist, track.Album))
	except AttributeError:
		print('No song was found playing.')
	
	return hexchat.EAT_ALL

def unload_cb(userdata):
	if loaded: print(__module_name__, 'version', __module_version__, 'unloaded.')

hexchat.hook_command('np', np_cb)
hexchat.hook_unload(unload_cb)
