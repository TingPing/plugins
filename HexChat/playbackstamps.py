from __future__ import print_function
from time import time
import hexchat

__module_name__ = 'PlaybackStamps'
__module_author__ = 'TingPing'
__module_version__ = '0'
__module_description__ = 'Prints date on older playback messages'

edited = False

events = ['Channel Message', 'Channel Msg Hillight',
		'Channel Action', 'Channel Action Hillight',
		'Your Action', 'Your Message']

def msg_cb(word, word_eol, event_name, attrs):
	global edited

	event_time = attrs.time
	if not event_time or edited or event_time - time() < 86400: # Ignore if within 24hrs
		return

	format = hexchat.get_prefs('stamp_text_format')
	hexchat.command('set -quiet stamp_text_format {}'.format('%m-%d ' + format))

	edited = True
	hexchat.emit_print(event_name, word[0], word[1], time=attrs.time)
	edited = False

	hexchat.command('set -quiet stamp_text_format {}'.format(format))

	return hexchat.EAT_ALL

def unload_cb(userdata):
	print(__module_name__, 'version', __module_version__, 'unloaded.')

for event in events:
	hexchat.hook_print_attrs(event, msg_cb, event)
hexchat.hook_unload(unload_cb)
print(__module_name__, 'version', __module_version__, 'loaded.')
