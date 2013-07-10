__module_name__ = "PMColor"
__module_author__ = "TingPing"
__module_version__ = "1"
__module_description__ = "Color PM tabs like Hilights"

import xchat

def pm_cb(word, word_eol, userdata):
  xchat.command('GUI COLOR 3')
	return None

xchat.hook_print("Private Message to Dialog", pm_cb)
xchat.hook_print("Private Action to Dialog", pm_cb)
