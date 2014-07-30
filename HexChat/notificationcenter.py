from __future__ import print_function
import hexchat

__module_name__ = 'notification-center'
__module_author__ = 'TingPing'
__module_version__ = '0'
__module_description__ = 'Integrate with the Notification Center on OSX'

loaded = False
try:
	from pync import Notifier
except ImportError:
	print('\002\00304Error:\017 Please install:\n  \037https://github.com/alloy/terminal-notifier\n  https://github.com/SeTeM/pync\017')
	hexchat.command('timer 0.1 py unload ' + __module_name__)
else:
	loaded = True
	print(__module_name__, 'version', __module_version__, 'loaded.')

def notify(title, message):
	if hexchat.get_prefs('away_omit_alerts') and hexchat.get_info('away'):
		return

	if hexchat.get_prefs('gui_focus_omitalerts') and hexchat.get_info('win_status') == 'active':
		return
	
	Notifier.notify(hexchat.strip(message), title=hexchat.strip(title), sender='org.hexchat', sound='default')

def hilight_cb(word, word_eol, userdata):
	notify('Highlight by ' + word[0], word[1])

def pm_cb(word, word_eol, userdata):
	notify('Messaged by ' + word[0], word[1])

def tray_cb(word, word_eol, userdata):
	if len(word) > 3 and word[1] == '-b':
		notify(word[2], word_eol[3])
		return hexchat.EAT_ALL

def unload_cb(userdata):
	if loaded:
		print(__module_name__, 'version', __module_version__, 'unloaded.')

hexchat.hook_print("Channel Msg Hilight", hilight_cb)
hexchat.hook_print("Channel Action Hilight", hilight_cb)
hexchat.hook_print("Private Message to Dialog", pm_cb)
hexchat.hook_print("Private Action to Dialog", pm_cb)
hexchat.hook_command("tray", tray_cb)
hexchat.hook_unload(unload_cb)
