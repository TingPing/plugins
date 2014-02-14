__module_name__='Growl'
__module_description__='Growl notification support'
__module_author__='TingPing'
__module_version__='16'

from time import time
import xchat
try:
	import gntp.notifier
except ImportError:
	xchat.prnt('\002\00304Growl Error:\017 Please install \037https://github.com/kfdm/gntp\017')
	xchat.command('timer 0.1 unload growl.py')

hexchatlogo = 'https://raw.github.com/hexchat/hexchat/master/data/icons/hexchat.png'
lasttime = time()
lastnick = ''
lasterrtime = 0

# initial setup of growl and list of possible notifications
# hostname and password are for over the network notifications
growl = gntp.notifier.GrowlNotifier(
	applicationName='HexChat',
	notifications=['Highlight', 'Private Message', 'Invited', 'Topic Changed',
					'User Online', 'Server Notice', 'Disconnected', 'Banned',
					'Killed', 'Kicked', 'Custom'],
	defaultNotifications=['Highlight', 'Private Message', 'Invited', 'Server Notice',
							'Disconnected', 'Killed', 'Kicked', 'Banned', 'Custom'],
	applicationIcon=hexchatlogo,
	#hostname='localhost',
	#password=''
)

try:
	growl.register() 
except:
	xchat.prnt('Growl Error: Could not register with Growl')


def growlnotify(_type, title, desc='', pri=0):
	if xchat.get_prefs('away_omit_alerts') and xchat.get_info('away'):
		return None

	if xchat.get_prefs('gui_focus_omitalerts') and xchat.get_info('win_status') == 'active':
		return None

	try:
		growl.notify(
			noteType=_type,
			title=xchat.strip(title),
			description=xchat.strip(desc),
			icon=hexchatlogo,
			sticky=False,
			priority=pri
		)
	except:
		global lasterrtime
		# Avoid more spam, 1 error a min.
		if lasterrtime + 60 < time():
			xchat.prnt('Growl Error: Growl is not running.')
		lasterrtime = time()

	return None


# now checks for and ignores mass hilights, performance impact not yet tested, maybe removed, optional, or only used on small channels
# disabled for now
# def masshilight(nick, message):
# 	userlist = ''

# 	for user in xchat.get_list('users'):
# 		if user.nick != word[0]:
# 			userlist += user.nick + ' '

# 	if re.search(userlist[:-1], xchat.strip(message)):
# 		return True

# 	else:
# 		return False

def spam(currenttime, currentnick):
	# Highlight and PM now have spam protection which previously could hang XChat
	global lasttime
	global lastnick

	if xchat.nickcmp(lastnick, currentnick) != 0:
		lasttime = time()
		lastnick = currentnick
		return False

	elif lasttime + 3 < currenttime: 
		lasttime = time()
		return False

	else:
		lasttime = time()
		return True

def active(chan):
	# Checks to see if chat is active to reduce annoying notifications
	try:
		chat = xchat.find_context()
		currentchat = chat.get_info("channel")
		status = xchat.get_info("win_status")
		if currentchat == chan and status == "active":
			return True
		else:
			return False
	except:
		return False


# start list of notifications
def hilight_callback(word, word_eol, userdata):
	if not spam(time(), word[0]): # and not masshilight(word[0], word[1]):
		growlnotify('Highlight',
					'Highlight by ' + word[0],
					word[1],
					1)

def pm_callback(word, word_eol, userdata):
	if not spam(time(), word[0]) and not active(word[0]):
		growlnotify('Private Message',
				'Messaged by ' + word[0],
				word[1],
				1)

def invited_callback(word, word_eol, userdata):
	growlnotify('Invited',
				'Invited to ' + word[0],
				'Invited to %s by %s on %s' % (word[0], word[1], word[2]))

def topic_callback(word, word_eol, userdata):
	growlnotify('Topic Changed',
				word[2] + '\'s topic changed',
				'%s \'s topic changed to %s by %s' % (word[2], word[1], word[0]),
				-2)

def onlinenotify_callback(word, word_eol, userdata):
	growlnotify('User Online',
				word[0] + ' is online on ' + word[2])

def servernotice_callback(word, word_eol, userdata):
	growlnotify('Server Notice',
				'Notice from ' + word[1],
				word[0])

def disconnect_callback(word, word_eol, userdata):
	growlnotify('Disconnected',
				'Disonnected from server',
				word[0],
				1)

def killed_callback(word, word_eol, userdata):
	growlnotify('Killed',
				'Killed by ' + word[0],
				word[1],
				2)

def kicked_callback(word, word_eol, userdata):
	growlnotify('Kicked',
				'You have been kicked from ' + word[2],
				'Kicked by %s for %s' % (word[1], word[3]),
				1)

def banned_callback(word, word_eol, userdata):
	# this now works on a basic level, will possibly be improved
	nick = xchat.get_info('nick')
	for user in xchat.get_list('users'):
		if xchat.nickcmp(nick, user.nick) == 0:
			userhost = user.host
	if not userhost:
		return None
	hostip = userhost.split('@')[1]

	if nick in word[1] or hostip in word[1]:
		growlnotify('Banned',
		'You have been banned by ' + word[0])

def tray_callback(word, word_eol, userdata):
	if len(word) > 3 and word[1] == '-b':
		growlnotify('Custom', word[2], word_eol[3], 1)
		return xchat.EAT_ALL
	
	return xchat.EAT_NONE

def unload_callback(userdata):
	xchat.prnt(__module_name__ + ' version ' + __module_version__ + ' unloaded.')

# get events from hexchat to call notifications
xchat.hook_print("Channel Msg Hilight", hilight_callback)
xchat.hook_print("Channel Action Hilight", hilight_callback)
xchat.hook_print("Private Message to Dialog", pm_callback)
xchat.hook_print("Private Action to Dialog", pm_callback)
xchat.hook_print("Invited", invited_callback)
xchat.hook_print("Notice", servernotice_callback)
xchat.hook_print("Notify Online", onlinenotify_callback)
xchat.hook_print("Topic Change", topic_callback)
xchat.hook_print("You Kicked", kicked_callback)
xchat.hook_print("Killed", killed_callback)
xchat.hook_print("Channel Ban", banned_callback)
# hook the tray command for other scripts to use
xchat.hook_command("tray", tray_callback)
# just to print its unloaded
xchat.hook_unload(unload_callback)
# Nothing broke yet, its loaded! =)
xchat.prnt(__module_name__ + ' version ' + __module_version__ + ' loaded.')
