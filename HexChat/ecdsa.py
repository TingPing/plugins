from __future__ import print_function
import base64
import subprocess
from os import path
import hexchat

__module_name__ = 'ECDSA'
__module_author__ = 'TingPing'
__module_version__ = '0'
__module_description__ = 'Implements ECDSA SASL mech'


# README
#
# This script is not necessarily complete or user friendly (this mech isn't in general)
# but it does work here are some basic steps:
#
# - Install https://github.com/atheme/ecdsatool
# - Run `ecdsatool keygen ~/.config/hexchat/irc.pem`
# - Take the output of that and run `/msg nickserv set property pubkey THEKEY`
# - Configure options below
#
# I recommend also using my requiresasl.py script for a more secure experience
#

# CONFIGUREME
NETWORKS = (
	'freenode-testnet',
)
USERNAME = '' # If empty uses global username
KEY_FILE = path.join(hexchat.get_info('configdir'), 'irc.pem')


def cap_cb(word, word_eol, userdata):
	if not hexchat.get_info('network') in NETWORKS:
		return

	# We will handle SASL for this one instead of hexchat
	if word[3] == 'ACK' and 'sasl' in word_eol[4]:
		hexchat.command('recv {}'.format(word_eol[0].replace('sasl', '')))
		hexchat.command('quote AUTHENTICATE ECDSA-NIST256P-CHALLENGE')
		return hexchat.EAT_ALL

def auth_cb(word, word_eol, userdata):
	if not hexchat.get_info('network') in NETWORKS:
		return

	# This will fail if user does not have pubkey set
	if word[1] == '+':
		user = hexchat.get_prefs('irc_user_name') if not USERNAME else USERNAME
		hexchat.emit_print('SASL Authenticating', user, 'ECDSA-NIST256P-CHALLENGE') 
		encoded = base64.b64encode(user + '\000' + user)
		hexchat.command('quote AUTHENTICATE {}'.format(encoded))
		return hexchat.EAT_ALL

	try:
		ret = subprocess.check_output(['ecdsatool', 'sign', KEY_FILE, word_eol[1]])
		hexchat.command('quote AUTHENTICATE {}'.format(ret)) # TODO: Long messages?
	except (subprocess.CalledProcessError, OSError) as e:
		print('Error running ecdsatool: {}'.format(e))
		hexchat.command('quote AUTHENTICATE *')

	return hexchat.EAT_ALL

def unload_cb(userdata):
	print(__module_name__, 'version', __module_version__, 'unloaded.')

hexchat.hook_server('CAP', cap_cb)
hexchat.hook_server('AUTHENTICATE', auth_cb)
hexchat.hook_unload(unload_cb)
print(__module_name__, 'version', __module_version__, 'loaded.')
