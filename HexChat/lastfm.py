from __future__ import print_function

import sys
import json

if sys.version_info[0] == 2:
        import urllib2 as urllib_error
        import urllib as urllib_request
else:
        import urllib.error as urllib_error
        import urllib.request as urllib_request

import hexchat

__module_name__ = 'lastfm'
__module_author__ = 'TingPing'
__module_version__ = '1'
__module_description__ = 'Tell others what you are playing on last.fm'

lfm_help = """Lastfm Usage:
    LFM <username>
    LFM -e"""

USERNAME = hexchat.get_pluginpref('lfm_username')
KEY = '4847f738e6b34c0dc20b13fe42ea008e'

def print_nowplaying(track, echo=False):
	try:
		title = track['name']
		artist = track['artist']['#text']
		album = track['album']['#text']
		if sys.version_info[0] == 2:
			title = title.encode('utf-8')
			artist = artist.encode('utf-8')
			album = album.encode('utf-8')
	except KeyError:
		print('Lastfm: Song info not found')
		return

	if echo:
		cmd = 'echo Lastfm: {} by {} on {}.'.format(title, artist, album)
	elif hexchat.get_pluginpref('lfm_say'):
		cmd = 'say Now playing {} by {} on {}.'.format(title, artist, album)
	else:
		cmd = 'me is now playing {} by {} on {}.'.format(title, artist, album)

	hexchat.command(cmd)

def get_track():
	url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecentTracks&user={}&api_key={}&format=json'.format(USERNAME, KEY)
	try:
		response = urllib_request.urlopen(url)
		text = response.read().decode('utf-8')
		response.close()
	except urllib_error.HTTPError:
		return

	data = json.loads(text)

	try:
		track = data['recenttracks']['track'][0]
		if track['@attr']['nowplaying']:
			return track
	except (IndexError, KeyError):
		return

def lfm_cb(word, word_eol, userdata):
	global USERNAME
	echo = False
	
	if len(word) == 2:
		if word[1] == '-e':
			echo = True
		else:
			USERNAME = word[1]
			hexchat.set_pluginpref('lfm_username', USERNAME)
			print('Lastfm: Username set to {}'.format(USERNAME))
			return hexchat.EAT_ALL

	if not USERNAME:
		print('Lastfm: No username set, use /lfm <username> to set it')
		return hexchat.EAT_ALL
		
	track = get_track()
	if not track:
		print('Lastfm: No song currently playing')
	else:
		print_nowplaying(track, echo)
		
	return hexchat.EAT_ALL

hexchat.hook_command('lfm', lfm_cb, help=lfm_help)
