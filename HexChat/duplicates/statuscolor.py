import hexchat

__module_name__ = 'statuscolor'
__module_author__ = 'TingPing'
__module_version__ = '0'
__module_description__ = 'Colors nicks based on user mode'
# This is just a direct port of LifeIsPain's statuscolor.pl script.

events = ('Channel Message',
		'Channel Action',
		'Channel Msg Hilight',
		'Channel Action Hilight',
		'Your Message',
		'Your Action')

# TODO: update these for hexchats default theme
modes = {'+':'24',
		'%':'28',
		'@':'19',
		'&':'21',
		'~':'22'}

edited = False

def msg_cb(word, word_eol, event, attrs):
	global edited
	if edited or len(word) < 3 or not word[2] in modes:
		return hexchat.EAT_NONE

	color = modes[word[2]]
	nick = '\003{}{}\00399'.format(color, hexchat.strip(word[0]))
	word = [(word[i] if len(word) > i else '') for i in range(4)]

	edited = True
	hexchat.emit_print(event, nick, word[1], word[2], word[3], time=attrs.time)
	edited = False

	return hexchat.EAT_ALL

for event in events:
	hexchat.hook_print_attrs(event, msg_cb, event, hexchat.PRI_HIGH)
