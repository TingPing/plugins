# Originally written by Wil Cooley <wcooley@nakedape.cc>
# http://haus.nakedape.cc/svn/public/trunk/small-projects/desktop/screensaverAutoAway.py

import dbus
from dbus.mainloop.glib import DBusGMainLoop

import hexchat

__module_author__= 'TingPing'
__module_name__ = 'screensaver'
__module_version__ = '1'
__module_description__ = 'Sets user away when the GNOME screensaver is activated'

def screensaver_cb(state):
  if state:
		hexchat.command('allserv away')
	else:
		hexchat.command('allserv back')

def unload_cb(userdata):
	print(__module_name__ + ' version ' + __module_version__ + ' unloaded.')

DBusGMainLoop(set_as_default=True)
sesbus = dbus.SessionBus()
sesbus.add_signal_receiver(screensaver_cb, 'SessionIdleChanged', 'org.gnome.ScreenSaver')
sesbus.add_signal_receiver(screensaver_cb, 'ActiveChanged', 'org.gnome.ScreenSaver')

hexchat.hook_unload(unload_cb)
print(__module_name__ + ' version ' + __module_version__ + ' loaded.')
