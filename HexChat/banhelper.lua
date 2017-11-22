-- SPDX-License-Identifier: MIT
hexchat.register('BanHelper', '1', 'Simpllifies banning and quieting')

local function is_op ()
	local nick = hexchat.get_info('nick')
	for user in hexchat.iterate('users') do
		if hexchat.nickcmp(user.nick, nick) == 0 then
			return user.prefix:find('^[@&]')
		end
	end

	print('BanHelper: Warning, could not find self in userlist!')
	return false
end

local function get_mask (nick)
	if nick:find('[%*?!@%$]') then
		return nick -- Already a mask
	end

	for user in hexchat.iterate('users') do
		if hexchat.nickcmp(user.nick, nick) == 0 then
			if user.account then
				return '$a:' .. user.account
			elseif user.host then
				return '*!*@' .. user.host:match('@(.+)$')
			else
				print('BanHelper: Warning, user info not found, try enabling irc_who_join')
				return nil
			end
		end
	end
end

for _, command in pairs({'kickban', 'ban', 'quiet'}) do
	hexchat.hook_command(command, function (word, word_eol)
		if not word[2] then
			return hexchat.EAT_NONE
		end

		local caller = word[1]:lower()
		local channel = hexchat.get_info('channel')
		local mask = get_mask(word[2])
		local command

		if not mask then
			return hexchat.EAT_ALL
		end

		if caller == 'ban' then
			command = 'MODE +b ' .. mask
		elseif caller == 'kickban' then
			command = string.format('MODE +b %s\r\nKICK %s %s :%s', mask,
			                        channel, word[2], word_eol[3] or '')
		elseif caller == 'quiet' then
			command = 'MODE +q ' .. mask
		end

		local wasop = is_op()
		if not wasop then
			hexchat.command('cs op ' .. channel)
		end
		hexchat.hook_timer(100, function ()
			if is_op() then
				hexchat.command(command)
				if not wasop then
					hexchat.command('cs deop ' .. channel)
				end
				return false
			end

			return true
		end)

		return hexchat.EAT_HEXCHAT
	end)
end
