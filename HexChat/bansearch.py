import hexchat
import re

__module_name__ = 'BanSearch'
__module_author__ = 'TingPing'
__module_version__ = '1'
__module_description__ = 'Search for bans/quiets matching a user'

banhook = 0
quiethook = 0
endbanhook = 0
endquiethook = 0

banlist = []
quietlist = []

patterns = {'?': ".", '*': ".*", # translate wildcards to regex
            '{': r"\[", '}': r"\]", '|': r"\\", # IRC nick substitutions
            '[': r"\[", ']': r"\]", '$': r"\$", '.':r"\.", '!':r"\!"} # regex escapes

def print_result(mask, matchlist, matchnum, _type):
	if matchnum:
		print('\00318{}\017 had \00320{}\017 {} matches:'.format(mask, matchnum, _type))
		for match in matchlist:
			print('\t\t\t{}'.format(match))
	else:
		print('No {} matches for \00318{}\017 were found.'.format(_type, mask))

def match_mask(mask, searchmask):
	if searchmask is None:
		return False
	for match, repl in patterns.items():
		searchmask = searchmask.replace(match, repl)
	pattern = re.compile(searchmask.lower())
	return pattern.match(mask.lower())

def match_extban(mask, host, account, realname, usermask):
	try:
		extban, banmask = mask.split(':')
	except ValueError:
		extban = mask
		banmask = '*'

	if '~' in extban:
		invert = True
	else:
		invert = False

	# From http://freenode.net/using_the_network.shtml
	if 'a' in extban:
		ret = match_mask (account, banmask)
	elif 'r' in extban:
		ret = match_mask (realname, banmask)
	elif 'x' in extban:
		ret = match_mask ('{}#{}'.format(host, realname), banmask)
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

def banlist_cb(word, word_eol, userdata):
	global banlist
	banlist.append(word[4])
	return hexchat.EAT_HEXCHAT

def endbanlist_cb(word, word_eol, usermask):
	global banhook
	global endbanhook
	global banlist
	matchlist = []
	matchnum = 0

	# Cleanup hooks
	hexchat.unhook(banhook)
	banhook = 0
	hexchat.unhook(endbanhook)
	endbanhook = 0

	host, account, realname = get_user_info (usermask)

	if banlist:
		for mask in banlist:
			# If extban we require userinfo or are searching for extban
			if mask[0] == '$' and (host or usermask[0] == '$'):
				if match_extban (mask, host, account, realname, usermask):
					matchlist.append(mask)
					matchnum = matchnum + 1
			else:
				if host: # Was given a user
					if match_mask (mask, host):
						matchlist.append(mask)
						matchnum = matchnum + 1
				else: # Was given a mask or no userinfo found
					if match_mask (mask, usermask):
						matchlist.append(mask)
						matchnum = matchnum + 1

		banlist = []

	print_result (usermask, matchlist, matchnum, 'Ban')

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
	matchnum = 0

	# Cleanup hooks
	hexchat.unhook(quiethook)
	quiethook = 0
	hexchat.unhook(endquiethook)
	endquiethook = 0

	host, account, realname = get_user_info (usermask)

	if quietlist:
		for mask in quietlist:
			# If extban we require userinfo or are searching for extban
			if mask[0] == '$' and (host or usermask[0] == '$'):
				if match_extban (mask, host, account, realname, usermask):
					matchlist.append(mask)
					matchnum = matchnum + 1
			else:
				if host: # Was given a user
					if match_mask (mask, host):
						matchlist.append(mask)
						matchnum = matchnum + 1
				else: # Was given a mask or no userinfo found
					if match_mask (mask, usermask):
						matchlist.append(mask)
						matchnum = matchnum + 1

		quietlist = []

	print_result (usermask, matchlist, matchnum, 'Quiet')

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

hexchat.hook_command('bansearch', search_cb, help='BANSEARCH <mask|nick>')
hexchat.prnt(__module_name__ + ' version ' + __module_version__ + ' loaded.')

