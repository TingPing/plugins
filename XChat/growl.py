__module_name__='Growl for XChat'
__module_description__='Growl for Windows support for XChat-WDK' 
__module_version__='11'

#in theory works on any platform for growl but only tested on windows with wdk
#requires https://github.com/kfdm/gntp
import time
import re

import xchat
try:
	import gntp.notifier
except:
	xchat.prnt('Growl Error: Please install https://github.com/kfdm/gntp')

xchatlogo = 'http://forum.xchat.org/styles/prosilver/imageset/site_logo.png'
lasttime = time.time()
lastnick = ''

# initial setup of growl and list of possible notifications
# hostname and password are for over the network notifications
growl = gntp.notifier.GrowlNotifier(
	applicationName='XChat',
	notifications=['Highlight', 'Private Message', 'Invited', 'Topic Changed',
					'User Online', 'Server Notice', 'Disconnected', 'Banned',
					'Killed', 'Kicked'],
	defaultNotifications=['Highlight', 'Private Message', 'Invited', 'Server Notice',
							'Disconnected', 'Killed', 'Kicked', 'Banned'],
	applicationIcon=xchatlogo,
	hostname='localhost',
	password=''
)

try:
	growl.register() 
	xchat.prnt(__module_name__ + ' version ' + __module_version__ + ' loaded.')
except:
	xchat.prnt('Growl Error: Could not register with Growl')

# start list of notifications
def hilight_callback(word, word_eol, userdata):
	# now checks for and ignores mass hilights, performance impact not yet tested, maybe removed, optional, or only used on small channels
	# disabled for now
	# def masshilight():
	# 	userlist = ''

	# 	for user in xchat.get_list('users'):
	# 		if user.nick != word[0]:
	# 			userlist += user.nick + ' '

	# 	if re.search(userlist[:-1], xchat.strip(word[1])):
	# 		return True

	# 	else:
	# 		return False

	def spam():
		# this and PM now have spam protection which previously could crash XChat
		currenttime = time.time()
		currentnick = word[0]
		global lasttime
		global lastnick

		if xchat.nickcmp(lastnick, currentnick) != 0:
			lasttime = time.time()
			lastnick = word[0]
			return False

		elif lasttime + 3 < currenttime: 
			lasttime = time.time()
			return False

		else:
			lasttime = time.time()
			return True

	if not spam(): # and not masshilight():
		try:
			growl.notify(
				noteType='Highlight',
				title='Highlight by ' + word[0],
				description=word[1],
				icon=xchatlogo,
				sticky=False,
				priority=1
			)
		except: xchat.prnt('Growl Error: Growl is not running.')

def pm_callback(word, word_eol, userdata):
	currenttime = time.time()
	currentnick = word[0]

	def spam():
		currenttime = time.time()
		currentnick = word[0]
		global lasttime
		global lastnick

		if xchat.nickcmp(lastnick, currentnick) != 0:
			lasttime = time.time()
			lastnick = word[0]
			return False

		elif lasttime + 3 < currenttime: 
			lasttime = time.time()
			return False

		else:
			lasttime = time.time()
			return True


	if not spam():
		try:
			growl.notify(
				noteType='Private Message',
				title='Messaged by ' + word[0],
				description=word[1],
				icon=xchatlogo,
				sticky=False,
				priority=1
			)
		except: xchat.prnt('Growl Error: Growl is not running.')

def invited_callback(word, word_eol, userdata):
	try:
		growl.notify(
			noteType='Invited', 	
			title='Invited to ' + word[0],
			description='Invited to %s by %s on %s' % (word[0], word[1], word[2]),
			icon=xchatlogo,
			sticky=False,
			priority=0
		)
	except: xchat.prnt('Growl Error: Growl is not running.')

def topic_callback(word, word_eol, userdata):
	try:
		growl.notify(
			noteType='Topic Changed',
			title=word[2] + '\'s topic changed',
			description='%s \'s topic changed to %s by %s' % (word[2], word[1], word[0]),
			icon=xchatlogo,
			sticky=False,
			priority=-2
		)
	except: xchat.prnt('Growl Error: Growl is not running.')

def onlinenotify_callback(word, word_eol, userdata):
	try:
		growl.notify(
			noteType='User Online',
			title=word[0] + ' is online on ' + word[2],
			description='',
			icon=xchatlogo,
			sticky=False,
			priority=0
		)
	except: xchat.prnt('Growl Error: Growl is not running.')

def servernotice_callback(word, word_eol, userdata):
	try:
		growl.notify(
			noteType='Server Notice',
			title='Notice from ' + word[1],
			description=word[0],
			icon=xchatlogo,
			sticky=False,
			priority=-1
		)
	except: xchat.prnt('Growl Error: Growl is not running.')

def disconnect_callback(word, word_eol, userdata):
	try:
		growl.notify(
			noteType='Disconnected',
			title='Disonnected from server',
			description=word[0],
			icon=xchatlogo,
			sticky=False,
			priority=1
		)
	except: xchat.prnt('Growl Error: Growl is not running.')

def killed_callback(word, word_eol, userdata):
	try:
		growl.notify(
			noteType='Killed',
			title='Killed by ' + word[0],
			description=word[1],
			icon=xchatlogo,
			sticky=False,
			priority=2
		)
	except: xchat.prnt('Growl Error: Growl is not running.')

def kicked_callback(word, word_eol, userdata):
	try:
		growl.notify(
			noteType='Kicked',
			title='You have been kicked from ' + word[2],
			description='Kicked by %s for %s' % (word[1], word[3]),
			icon=xchatlogo,
			sticky=False,
			priority=1
		)
	except: xchat.prnt('Growl Error: Growl is not running.')

def banned_callback(word, word_eol, userdata):
	# this now works on a basic level, will possibly be improved
	nick = xchat.get_info('nick')
	for user in xchat.get_list('users'):
		if xchat.nickcmp(nick, user.nick) == 0:
			userhost = user.host
	hostip = re.split('@', userhost)[1]

	if re.search(nick, word[1]) or re.search(hostip, word[1]):
		try:
			growl.notify(
				noteType='Banned',
				title='You have been banned by ' + word[0],
				description='',
				icon=xchatlogo,
				sticky=False,
				priority=1
			)
		except: xchat.prnt('Growl Error: Growl is not running.')

# get events from xchat to call notifications
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