import xchat as hexchat
 
__module_name__ = 'closeondisc'
__module_author__ = 'TingPing'
__module_version__ = '2'
__module_description__ = 'Close tabs on Disconnect'
 
def discon_cb(word, word_eol, userdata):
        network = hexchat.get_info('network')
 
        for chan in hexchat.get_list('channels'):
                if chan.network == network and chan.type == 2: # Don't close server tab or queries
                        chan.context.command('timer 1 close') # Delay to avoid crash
 
hexchat.hook_print('Disconnected', discon_cb)
