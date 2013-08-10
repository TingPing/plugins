from __future__ import print_function
import hexchat

__module_name__ = ''
__module_author__ = 'TingPing'
__module_version__ = '0'
__module_description__ = ''

def _cb(word, word_eol, userdata):

def unload_cb(userdata):
	print(__module_name__, 'version', __module_version__, 'unloaded.')

hexchat.hook_('', _cb)
hexchat.hook_unload(unload_cb)
print(__module_name__, 'version', __module_version__, 'loaded.')
