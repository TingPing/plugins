-- SPDX-License-Identifier: MIT
hexchat.register('SmartParts', '1', 'Intelligently hide parts, joins, modes, and nick changes')

local TIME_THRESHOLD = 60 * 5 -- in seconds

local function check_lasttalk (nick)
	local nick = hexchat.strip(nick)
	for user in hexchat.iterate('users') do
		if hexchat.nickcmp(nick, user.nick) == 0 then
			if os.time() - user.lasttalk > TIME_THRESHOLD then
				return hexchat.EAT_HEXCHAT
			else
				return hexchat.EAT_NONE
			end
		end
	end

	return hexchat.EAT_HEXCHAT
end

local function check_you (nick)
	return hexchat.nickcmp(hexchat.get_info('nick'), nick) == 0
end

local function check_notify (nick)
	local nick = hexchat.strip(nick)
	for user in hexchat.iterate('notify') do
		if user.nick == nick then
			return true
		end
	end

	return false
end


hexchat.hook_print('Join', function (args)
	if check_notify (args[1]) then
		return hexchat.EAT_NONE
	else
		return hexchat.EAT_HEXCHAT
	end
end, hexchat.PRI_LOW)

hexchat.hook_print('Change Nick', function (args)
	if check_notify(args[1]) or check_notify(args[2]) then
		return hexchat.EAT_NONE
	end

	return check_lasttalk(args[1])
end, hexchat.PRI_LOW)

hexchat.hook_print('Raw Modes', function (args)
	if check_you(args[1]) or check_notify(args[1]) then
		return hexchat.EAT_NONE
	end

	-- TODO: Parse targets

	return check_lasttalk(args[1])
end, hexchat.PRI_LOW)

for _, event in pairs({'Quit', 'Part', 'Part with Reason'}) do
	hexchat.hook_print(event, function (args)
		if check_notify(args[1]) then
			return hexchat.EAT_NONE
		end

		return check_lasttalk(args[1])
	end, hexchat.PRI_LOW)
end

for _, event in pairs({'Channel Operator', 'Channel Voices'}) do
	hexchat.hook_print(event, function (args)
		if check_you(args[1]) or check_you(args[2]) or check_notify(args[2]) then
			return hexchat.EAT_NONE
		end

		return check_lasttalk(args[2])
	end, hexchat.PRI_LOW)
end
