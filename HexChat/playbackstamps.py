from __future__ import print_function
from time import time
import hexchat

__module_name__ = 'PlaybackStamps'
__module_author__ = 'TingPing'
__module_version__ = '0'
__module_description__ = 'Prints date on older playback messages'

edited = False

def msg_cb(word, word_eol, event_name, attrs):
  global edited

	event_time = attrs.time
	if not event_time or edited or event_time - time() < 86400: # Didn't happen today
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

hexchat.hook_print_attrs('Channel Message', msg_cb, 'Channel Message')
hexchat.hook_print_attrs('Channel Action', msg_cb, 'Channel Action')
hexchat.hook_print_attrs('Channel Msg Highlight', msg_cb, 'Channel Msg Hilight')
hexchat.hook_print_attrs('Channel Action Highlight', msg_cb, 'Channel Action Hilight')
hexchat.hook_print_attrs('Your Action', msg_cb, 'Your Action')
hexchat.hook_print_attrs('Your Message', msg_cb, 'Your Message')
hexchat.hook_unload(unload_cb)
print(__module_name__, 'version', __module_version__, 'loaded.')
