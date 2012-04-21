###
# Copyright (c) 2012, Patrick Griffis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.conf as conf
import supybot.registry as registry
from supybot.i18n import PluginInternationalization, internationalizeDocstring

_ = PluginInternationalization('TS3')

def configure(advanced):
	# This will be called by supybot to configure this module.  advanced is
	# a bool that specifies whether the user identified himself as an advanced
	# user or not.  You should effect your configuration by manipulating the
	# registry as appropriate.
	from supybot.questions import expect, getpass, something, yn
	conf.registerPlugin('TS3', True)
	output(_("""This plugin is used to get info from or configure a Teamspeak 3 Server."""))
	if yn(_('Allow ServerQuery?(default: No)')):
		conf.supybot.plugins.TS3.allowserverquery.setValue(True)
	if something(_('Query Username?')):
		conf.supybot.plugins.TS3.username.setValue(s)
	if getpass(_('Query Password?(Set this for clientquery)')):
		conf.supybot.plugins.TS3.password.setValue(password)


TS3 = conf.registerPlugin('TS3')
conf.registerGlobalValue(TS3, 'allowserverquery', 'False',
		_("""Serverquery can be abused, disable completely for security.""")
conf.registerChannelValue(TS3, 'querytype',
	registry.String('Client', _("""'Client' connects to a clients IP and can only get information,
	'Server' can make configuration changes or get info and directly connets to the server"""))
conf.registerChannelValue(TS3, 'ip', 'localhost')
conf.registerChannelValue(TS3, 'username')
conf.registerChannelValue(TS3, 'password')
conf.registerChannelValue(TS3, 'port', '10011')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(TS3, 'someConfigVariableName',
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
