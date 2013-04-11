import hexchat

__module_name__ = "MyMessages"
__module_author__ = "TingPing"
__module_version__ = "0"
__module_description__ = "Properly show your messages in znc playback"

def message_cb(word, word_eol, userdata):
  if hexchat.nickcmp(word[0], hexchat.get_info('nick')) == 0:
		hexchat.emit_print('Your Message', word[0], word[1], '', '')
		return hexchat.EAT_HEXCHAT
		
def action_cb(word, word_eol, userdata):
	if hexchat.nickcmp(word[0], hexchat.get_info('nick')) == 0:
		hexchat.emit_print('Your Action', word[0], word[1], '', '')
		return hexchat.EAT_HEXCHAT

hexchat.hook_print("Channel Message", message_cb)
hexchat.hook_print("Channel Action", action_cb)
