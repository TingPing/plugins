# Originally written by Wil Cooley <wcooley@nakedape.cc>
# http://haus.nakedape.cc/svn/public/trunk/small-projects/desktop/screensaverAutoAway.py

import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

import hexchat

__module_author__= 'TingPing'
__module_name__ = 'screensaver'
__module_version__ = '2'
__module_description__ = 'Sets user away when the GNOME screensaver is activated'

screensavers = ('org.gnome.ScreenSaver',
		'org.cinnamon.ScreenSaver',
		'org.freedesktop.ScreenSaver')

sesbus = dbus.SessionBus()

def screensaver_cb(state):
	if state:
		hexchat.command('allserv away')
	else:
		hexchat.command('allserv back')

def unload_cb(userdata):
	print(__module_name__ + ' version ' + __module_version__ + ' unloaded.')


for screensaver in screensavers:
	sesbus.add_signal_receiver(screensaver_cb, 'ActiveChanged', screensaver)

hexchat.hook_unload(unload_cb)
print(__module_name__ + ' version ' + __module_version__ + ' loaded.')
