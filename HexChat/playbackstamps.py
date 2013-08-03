from __future__ import print_function
from datetime import date
import hexchat

__module_name__ = 'PlaybackStamps'
__module_author__ = 'TingPing'
__module_version__ = '1'
__module_description__ = 'Prints date on older playback messages'

edited = False

events = ['Channel Message', 'Channel Msg Hillight',
		'Channel Action', 'Channel Action Hillight',
		'Your Action', 'Your Message']

def is_today(event_time):
	# 0 means now
	if not event_time:
		return True

	now = date.today()
	event = date.fromtimestamp(event_time)
	diff = now - event

	# Was over 24hrs ago
	if diff.total_seconds() > 86400:
		return False

	# Different date
	if event.year < now.year or event.month < now.month or event.day < now.day:
		return False

	return True

def msg_cb(word, word_eol, event_name, attrs):
	global edited

	if edited or is_today(attrs.time):
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
