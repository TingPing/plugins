hexchat.register('MassHighlightIgnore', '1', 'Ignore mass highlight spam')

local MAX_COUNT = 4

local function match_nick_in_message (nick, message)
	local patterns = {
		'%s' .. nick .. '%s',
		'^'  .. nick .. '%s',
		'%s' .. nick .. '$',
		'^'  .. nick .. '%s',
	} -- match nick at start, end, or in the message
	for _, pattern in pairs(patterns) do
		if message:find(pattern) then
			return true
		end
	end
	return false
end

local function is_mass_highlight (context, message)
	local count = 0

	for user in context:iterate('users') do
		if match_nick_in_message (user.nick, message) then
			count = count + 1
			if count == MAX_COUNT then
				return true
			end
		end
	end

	return false
end

local function is_highlight (context, message)
	local nick = context:get_info('nick')

	if match_nick_in_message(nick, message) then
		return true
	end

	return false
end

local function ignore_highlight (nick)
	local ignore_list = hexchat.prefs['irc_no_hilight']
	local new_list

	if ignore_list == '' then
		new_list = nick
	else
		new_list = ignore_list .. ',' .. nick
	end		

	hexchat.command('set -quiet irc_no_hilight ' .. new_list)
	hexchat.command('timer .1 set -quiet irc_no_hilight ' .. ignore_list)
end

hexchat.hook_server('PRIVMSG', function (word, word_eol)
	local channel = word[3]
	local ctx = hexchat.find_context(hexchat.get_info('network'), channel)

	if not ctx then
		return
	end

	local message = hexchat.strip(word_eol[4])
	if is_highlight (ctx, message) and is_mass_highlight (ctx, message) then
		ignore_highlight (word[1]:match('^:([^!]+).*$'))
	end
end)
