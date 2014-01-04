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
__module_version__ = '0'
__module_description__ = 'Tell others what you are playing on last.fm'

lfm_help = """Lastfm Usage:
    LFM <username>
    LFM -e"""

USERNAME = hexchat.get_pluginpref('lfm_username')
KEY = '4847f738e6b34c0dc20b13fe42ea008e'

def lfm_cb(word, word_eol, userdata):
	global USERNAME
	echo = False
	
	if len(word) == 2:
		if word[1] == '-e':
			echo = True
		else:
			USERNAME = word[1]
			hexchat.set_pluginpref('lfm_username', word[1])
			print('Lastfm: Username set to {}'.format(word[1]))
			return hexchat.EAT_ALL

	if not USERNAME:
		print('Lastfm: No username set, use /lfm <username> to set it')
		return hexchat.EAT_ALL

	url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecentTracks&user={}&api_key={}&format=json'.format(USERNAME, KEY)
	try:
		response = urllib_request.urlopen(url)
		text = response.read().decode('utf-8')
		response.close()
	except urllib_error.HTTPError as err:
		print('Lastfm Error: {}'.format(err))
		return hexchat.EAT_ALL

	data = json.loads(text)
	track = data['recenttracks']['track'][0]
	if not '@attr' in track or not track['@attr']['nowplaying']:
		print('Lastfm: No song currently playing')
		return hexchat.EAT_ALL
		
	title = track['name']
	artist = track['artist']['#text']
	album = track['album']['#text']

	if echo:
		cmd = 'echo Lastfm: {} by {} on {}.'.format(title, artist, album)
	elif hexchat.get_pluginpref('lfm_say'):
		cmd = 'say Now playing {} by {} on {}.'.format(title, artist, album)
	else:
		cmd = 'me is now playing {} by {} on {}.'.format(title, artist, album)
	
	hexchat.command(cmd)
		
	return hexchat.EAT_ALL

hexchat.hook_command('lfm', lfm_cb, help=lfm_help)
