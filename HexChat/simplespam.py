import hexchat

__module_name__='Ignore spam'
__module_description__='ignores the most basic of spam.'
__module_author__='TingPing'
__module_version__='0'

lastmsg = ''
spamcount = 0

def chan_cb(word, word_eol, userdata):
    global lastmsg
    global spamcount
    if word[1] == lastmsg:
        spamcount += 1
        if spamcount > 2:
            hexchat.command('ignore %s CHAN' %hexchat.strip(word[0]))
        return xchat.EAT_XCHAT
    else:
        lastmsg = word[1]
        spamcount = 0
    
hexchat.hook_print('Channel Message', chan_cb)
