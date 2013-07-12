import hexchat

__module_name__ = "RequireSASL"
__module_author__ = "TingPing"
__module_version__ = "0"
__module_description__ = "Disconnect if SASL fails"

def fail_cb(word, word_eol, userdata):
  hexchat.command("timer .1 discon") # Delay so disconnect happens after message.

hexchat.hook_server("904", fail_cb)
hexchat.hook_server("905", fail_cb)
