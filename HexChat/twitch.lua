-- SPDX-License-Identifier: MIT
hexchat.register('Twitch', '1', 'Better integration with twitch.tv')

local function is_twitch ()
	local server = hexchat.get_info('server')
	if hexchat.nickcmp(hexchat.get_info('network'), 'Twitch') == 0 then
		return true
	elseif server and server:find('twitch.tv$') then
		return true
	else
		return false
	end
end


-- Commands from http://help.twitch.tv/customer/portal/articles/659095-chat-moderation-commands
-- /ban may conflict with other scripts nothing we can do about that
-- /clear is an existing command, just override it
for _, command in pairs({
	'timeout', 'slow', 'slowoff', 'subscribers', 'subscribersoff',
	'mod', 'unmod', 'mods', 'clear', 'ban', 'unban', 'commercial',
	'r9kbeta', 'r9kbetaoff', 'color', 'host',
}) do
	hexchat.hook_command(command, function (word, word_eol)
		if not is_twitch() then return end

		hexchat.command('say .' .. word_eol[1])
		return hexchat.EAT_ALL
	end)
end

for command, alias in pairs({['op'] = 'mod', ['deop'] = 'unmod'}) do
	hexchat.hook_command(command, function (word, word_eol)
		if not is_twitch() then return end

		if word[2] then
			hexchat.command(string.format('say .%s %s', alias, word_eol[2]))
		else
			hexchat.command('say .' .. alias)
		end
		return hexchat.EAT_ALL
	end)
end

hexchat.hook_server('PRIVMSG', function (word, word_eol)
	if not is_twitch() then return end

	-- Move jtv messages to the server tab
	if word[1]:find('^:jtv!') and word[3]:sub(1, 1) ~= '#' then
		local id = hexchat.prefs['id']
		for chan in hexchat.iterate('channels') do
			if chan.type == 1 and chan.id == id then
				chan.context:emit_print('Server Text', word_eol[4]:sub(2))
				return hexchat.EAT_ALL
			end
		end
	end
end)

hexchat.hook_server('421', function (word, word_eol)
	if not is_twitch() then return end

	-- Ignore unknown command errors
	if word[4] == 'WHO' or word[4] == 'WHOIS' then
		return hexchat.EAT_ALL
	end
end)

hexchat.hook_print('Your Message', function (args)
	if not is_twitch() then return end

	-- Eat any message starting with a '.', twitch eats all of them too
	if args[2]:sub(1, 1) == '.' then
		return hexchat.EAT_ALL
	end
end)

hexchat.hook_print('Channel Message', function (args)
	if not is_twitch() then return end

	-- Format messages from twitchnotify
	if args[1] == 'twitchnotify' then
		print('\00314*\t' .. args[2])
		return hexchat.EAT_HEXCHAT
	end
end, hexchat.PRI_LOW)
