from __future__ import print_function

import os
import sys
import json
import threading

THREADS_SUPPORTED = True
if sys.version_info[0] == 2:
	import urllib2 as urllib_error
	import urllib as urllib_request

	# Avoid threads on py2/win32. This will lockup HexChat
	if sys.platform == 'win32':
		THREADS_SUPPORTED = False
else:
	import urllib.error as urllib_error
	import urllib.request as urllib_request

import hexchat

__module_name__ = 'Script'
__module_author__ = 'TingPing'
__module_version__ = '6'
__module_description__ = 'Manage scripts'

# TODO:
# add preference for adding repos
# search subfolders
# command to refresh cache

script_help = 'Script: Valid commands are:\n \
			INSTALL script\n \
			SEARCH word\n \
			EDIT script\n \
			UPDATE script\n \
			REMOVE script'

addon_dir = os.path.join(hexchat.get_info('configdir'), 'addons')
addon_types = ('py', 'pl', 'lua', 'js') # tcl has no way to unload a single script?
addon_cache = {}
#               User,       Repo,      Folder
addon_sites = (('TingPing', 'plugins', 'HexChat'),
				('Arnavion', 'random', 'hexchat'),
				('Farow', 'hexchat-scripts', ''))


def expand_script(script):
	return os.path.join(addon_dir, script)

def build_url(site, type='', script=''):
	if type == 'raw':
		return 'https://raw.github.com/{1}/{2}/master/{3}/{0}'.format(script, *site)
	elif type == 'api':
		return 'https://api.github.com/repos/{0}/{1}/contents/{2}'.format(*site)
	else:
		return 'https://github.com/{1}/{2}/tree/master/{3}/{0}'.format(script, *site)


def update_addons():
	global addon_cache
	addon_cache = {}

	for site in addon_sites:
		try:
			response = urllib_request.urlopen(build_url(site, type='api'))
			text = response.read().decode('utf-8')
			response.close()
			data = json.loads(text)
			addon_cache[site] = [d['name'] for d in data if d['name'].split('.')[-1] in addon_types]
		except urllib_error.HTTPError: # 403 after rate-limit
			pass

	print('Script: Addon cache updated.')

def download(script, unload):
	for site in addon_cache.keys():
		if script in addon_cache[site]:
			print('Script: Downloading {}...'.format(script))
			try:
				urllib_request.urlretrieve(build_url(site, type='raw', script=script), expand_script(script))
			except urllib_error.HTTPError as err:
				print('Script: Error downloading {} ({})'.format(script, err))
			else:
				print('Script: Download complete, {}...'.format('reloading' if unload else 'loading'))
				if unload: # Updated
					# Threading causes odd timing issues, using timer fixes it.
					hexchat.command('timer .1 unload {}'.format(expand_script(script)))
				hexchat.command('timer .1 load {}'.format(expand_script(script)))
			
			return

	print('Script: Could not find {}'.format(script))


def install(script, unload):
	if THREADS_SUPPORTED:
		threading.Thread(target=download, args=(script, unload)).start()
	else:
		download(script, unload)

def search(word):
	matches = [(site, script) for site in addon_cache.keys() for script in addon_cache[site] if word in script]

	if not matches:
		print('Script: {} not found.'.format(word))
	else:
		print('Script: {} matches found for {}.'.format(len(matches), word))
		for (site, script) in matches:
			print('\t\t{}: \00318\037{}\017'.format(script, build_url(site, type='', script=script)))


def script_cb(word, word_eol, userdata):
	if len(word) > 2:
		cmd = word[1].lower()
		arg = word[2]
	else:
		hexchat.command('help script')
		return hexchat.EAT_ALL

	if cmd == 'install':
		if os.path.exists(expand_script(arg)):
			print('Script: {} is already installed.'.format(arg))
			return hexchat.EAT_ALL
		else:
			install(arg, False)
	elif cmd == 'update':
		if os.path.exists(expand_script(arg)):
			install(arg, True)
	elif cmd == 'edit':
		if sys.platform.startswith('linux'):
			# This will popup a choose program prompt /url doesn't
			hexchat.command('exec -d gvfs-open {}'.format(expand_script(arg)))
		else:
			hexchat.command('url {}'.format(expand_script(arg)))
	elif cmd == 'search':
		search(arg)
	elif cmd == 'remove':
		if arg == 'script.py':
			print('Script: I refuse.')
			return hexchat.EAT_ALL
		if os.path.exists(expand_script(arg)):
			hexchat.command('unload ' + expand_script(arg))
			os.remove(expand_script(arg))
		else:
			print('Script: {} is not installed.'.format(arg))
	else:
		hexchat.command('help script')

	return hexchat.EAT_ALL

def unload_callback(userdata):
	print(__module_name__, 'version', __module_version__, 'unloaded.')

if THREADS_SUPPORTED:
	threading.Thread(target=update_addons).start()
else:
	update_addons()
hexchat.hook_command('script', script_cb, help=script_help)
hexchat.hook_unload(unload_callback)
print(__module_name__, 'version', __module_version__, 'loaded.')
