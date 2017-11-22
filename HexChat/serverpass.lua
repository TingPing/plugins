-- SPDX-License-Identifier: MIT
hexchat.register('ServerPass', '1', 'Allows using server password with another login method')

-- Configure networks here:
--   The key must match a network name in your network list
--   Set the value to an empty string to re-use the same network list password
--   Otherwise set the value to any string for a custom password
local NETWORKS = {
	['freenode'] = '',
--	['freenode'] = 'password',
}

hexchat.hook_print('Connected', function (args)
	local network = hexchat.get_info('network')
	local username = hexchat.prefs['irc_user_name']
	local password = NETWORKS[network]

	if password then
		if password == '' then
			password = hexchat.get_info('password')
		end

		hexchat.command(string.format('QUOTE PASS %s:%s', username, password))
	end
end)
