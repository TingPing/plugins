import hexchat
import re

__module_name__ = 'BanSearch'
__module_author__ = 'TingPing'
__module_version__ = '2'
__module_description__ = 'Search for bans/quiets matching a user'

banhook = 0
quiethook = 0
endbanhook = 0
endquiethook = 0

banlist = []
quietlist = []

regexescapes = {'[':r'\[', ']':r'\]', '.':r'\.'}
ircreplace = {'{':'[', '}':']', '|':'\\'} # IRC nick substitutions
wildcards = {'?':r'.', '*': r'.*'} # translate wildcards to regex

def print_result(mask, matchlist, _type):
	if matchlist:
		print('\00318{}\017 had \00320{}\017 {} matches:'.format(mask, len(matchlist), _type))
		for match in matchlist:
			print('\t\t\t{}'.format(match))
	else:
		print('No {} matches for \00318{}\017 were found.'.format(_type, mask))

def match_mask(mask, searchmask):
	if searchmask is None:
		searchmask = ''

	# A mask of $a:* can match a user with no account
	if searchmask == '' and mask != '*':
		return False
	# A mask of $a will not match a user with no account
	elif mask == '' and searchmask != '':
		return True

	# These have to be replaced in a very specific order
	for match, repl in ircreplace.items():
		mask = mask.replace(match, repl)
		searchmask = searchmask.replace(match, repl)
	for match, repl in regexescapes.items():
		mask = mask.replace(match, repl)
	for match, repl in wildcards.items():
		mask = mask.replace(match, repl)

	if '$' in mask and mask[0] != '$': # $#channel is used to forward users, ignore it
		mask = mask.split('$')[0]

	return bool(re.match(mask, searchmask, re.IGNORECASE))

def match_extban(mask, host, account, realname, usermask):
	try:
		extban, banmask = mask.split(':')
	except ValueError:
		extban = mask
		banmask = ''

	if '~' in extban:
		invert = True
	else:
		invert = False

	# Extbans from http://freenode.net/using_the_network.shtml
	if ':' in usermask: # Searching for extban
		userextban, usermask = usermask.split(':') 
		if extban == userextban:
			ret = match_mask(banmask, usermask)
		else:
			return False
	elif 'a' in extban:
		ret = match_mask (banmask, account)
	elif 'r' in extban:
		ret = match_mask (banmask, realname)
	elif 'x' in extban:
		ret = match_mask (banmask, '{}#{}'.format(host, realname))
	else:
		return False

	if invert:
		return not ret
	else:
		return ret

def get_user_info(nick):
	invalid_chars = ['*', '?', '$', '@', '!']
	if any(char in nick for char in invalid_chars):
		return (None, None, None) # It's a mask not a nick.

	for user in hexchat.get_list('users'):
		if user.nick == nick:
			host = user.nick + '!' + user.host
			account = user.account
			realname = user.realname
			return (host, account, realname)

	return (None, None, None)

def search_list(list, usermask):
	matchlist = []
	host, account, realname = get_user_info (usermask)

	for mask in list:
		# If extban we require userinfo or we are searching for extban
		if mask[0] == '$' and (host or usermask[0] == '$'):
			if match_extban (mask, host, account, realname, usermask):
				matchlist.append(mask)
		elif mask[0] != '$':
			if host: # Was given a user
				if match_mask (mask, host):
					matchlist.append(mask)
			else: # Was given a mask or no userinfo found
				if match_mask (mask, usermask):
					matchlist.append(mask)

	return matchlist


def banlist_cb(word, word_eol, userdata):
	global banlist
	banlist.append(word[4])
	return hexchat.EAT_HEXCHAT

def endbanlist_cb(word, word_eol, usermask):
	global banhook
	global endbanhook
	global banlist
	matchlist = []

	hexchat.unhook(banhook)
	banhook = 0
	hexchat.unhook(endbanhook)
	endbanhook = 0

	if banlist:
		matchlist = search_list(banlist, usermask)
		banlist = []

	print_result (usermask, matchlist, 'Ban')

	return hexchat.EAT_HEXCHAT

def quietlist_cb(word, word_eol, userdata):
	global quietlist
	quietlist.append(word[5])
	return hexchat.EAT_HEXCHAT

def endquietlist_cb(word, word_eol, usermask):
	global quiethook
	global endquiethook
	global quietlist
	matchlist = []

	hexchat.unhook(quiethook)
	quiethook = 0
	hexchat.unhook(endquiethook)
	endquiethook = 0

	if quietlist:
		matchlist = search_list(quietlist, usermask)
		quietlist = []

	print_result (usermask, matchlist, 'Quiet')

	return hexchat.EAT_HEXCHAT

def search_cb(word, word_eol, userdata):
	global banhook
	global quiethook
	global endbanhook
	global endquiethook

	if len(word) == 2:
		hooks = [quiethook, banhook, endquiethook, endbanhook]
		if not any(hook for hook in hooks):
			banhook = hexchat.hook_server ('367', banlist_cb)
			quiethook = hexchat.hook_server ('728', quietlist_cb)
			endbanhook = hexchat.hook_server ('368', endbanlist_cb, word[1])
			endquiethook = hexchat.hook_server ('729', endquietlist_cb, word[1])

			hexchat.command('ban')
			hexchat.command('quiet')
		else:
			print('A ban search is already in progress.')

	else:
		hexchat.command('help bansearch')

	return hexchat.EAT_ALL

def unload_cb(userdata):
	print(__module_name__ + ' version ' + __module_version__ + ' unloaded.')

hexchat.hook_unload(unload_cb)
hexchat.hook_command('bansearch', search_cb, help='BANSEARCH <mask|nick>')
hexchat.prnt(__module_name__ + ' version ' + __module_version__ + ' loaded.')
