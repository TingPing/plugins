import hexchat

__module_name__ = "LogPM"
__module_author__ = "TingPing"
__module_version__ = "0"
__module_description__ = "Auto log pm's"

def open_cb(word, word_eol, userdata):
  if hexchat.get_info('channel')[0] != '#':
		hexchat.command('chanopt text_logging on')

hexchat.hook_print("Open Context", open_cb)
