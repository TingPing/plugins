-- SPDX-License-Identifier: MIT
hexchat.register('MassHighlightIgnore', '3', 'Ignore mass highlight spam')

if unpack == nil then
	unpack = table.unpack -- fix lua 5.2
end

local MAX_COUNT = 4

-- http://lua-users.org/wiki/SplitJoin
local function split(str)
	local t = {}
	for i in string.gmatch(str, "%S+") do
		t[#t + 1] = i
	end
	return t
end

local function nick_in_list (nick, list)
	for _, word in pairs(list) do
		if hexchat.nickcmp(word, nick) == 0 then
			return true
		end
	end
	return false
end

local function is_mass_highlight (message)
	local count = 0
	local words = split(message)

	for user in hexchat.props.context:iterate('users') do
		if nick_in_list(user.nick, words) then
			count = count + 1
			if count == MAX_COUNT then
				return true
			end
		end
	end

	return false
end

local function ignore_mass_hilight (args, attrs, event)
	if is_mass_highlight(args[2]) then
		hexchat.emit_print_attrs(attrs, event, unpack(args))
		return hexchat.EAT_ALL
	end
end

hexchat.hook_print_attrs('Channel Msg Hilight', function (args, attrs)
	return ignore_mass_hilight(args, attrs, 'Channel Message')
end, hexchat.PRI_HIGHEST)

hexchat.hook_print('Channel Action Hilight', function (args, attrs)
	return ignore_mass_hilight(args, attrs, 'Channel Action')
end, hexchat.PRI_HIGHEST)
