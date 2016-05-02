import hexchat

__module_name__ = 'Highlight Logger'
__module_version__ = '2'
__module_description__ = 'Prints highlights to another tab'
# Forked from Arnavion's

TAB_NAME = '(highlights)'

def find_highlighttab():
	context = hexchat.find_context(channel=TAB_NAME)
	if context == None: # Create a new one in the background
		newtofront = hexchat.get_prefs('gui_tab_newtofront')

		hexchat.command('set -quiet gui_tab_newtofront 0')
		hexchat.command('newserver -noconnect {0}'.format(TAB_NAME))
		hexchat.command('set -quiet gui_tab_newtofront {}'.format(newtofront))

		return hexchat.find_context(channel=TAB_NAME)
	else:
		return context

def highlight_callback(word, word_eol, user_data):
	
	word = [(word[i] if len(word) > i else '') for i in range(4)]
	
	highlight_context = find_highlighttab()
	
	channel = hexchat.get_info('channel')
	
	if user_data == 'Channel Msg Hilight':
		highlight_context.prnt('\00322{0}\t\00318<{4}{3}{1}>\017 {2}'.format(channel, *word))
	elif user_data == 'Channel Action Hilight':
		highlight_context.prnt('\00322{0}\t\002\00318{4}{3}{1}\017 {2}'.format(channel, *word))	

	# Can't easily intelligently manage color so lets just ignore it
	highlight_context.command('gui color 0')
	
	return hexchat.EAT_NONE

hexchat.hook_print('Channel Msg Hilight', highlight_callback, 'Channel Msg Hilight')
hexchat.hook_print('Channel Action Hilight', highlight_callback, 'Channel Action Hilight')
