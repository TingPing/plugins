-- SPDX-License-Identifier: MIT
hexchat.register('MyMessage', '2', 'Properly show your own messages in ZNC playback')

local function get_server_ctx()
	local id = hexchat.prefs['id']
	for chan in hexchat.iterate('channels') do
		if chan.type == 1 and chan.id == id then
			return chan.context
		end
	end
	return hexchat.props.context
end

hexchat.hook_print('Capability List', function (args)
	if args[2]:find('znc.in/self%-message') then
		hexchat.command('CAP REQ znc.in/self-message')

		local ctx = get_server_ctx()
		hexchat.hook_timer(1, function ()
			-- Emit right after this event
			if ctx:set() then
				hexchat.emit_print('Capability Request', 'znc.in/self-message')
			end
		end)
	end
end)

local function prefix_is_channel (prefix)
	local chantypes = hexchat.props['chantypes']
	for i = 1, #chantypes do
		if chantypes:sub(i, i) == prefix then
			return true
		end
	end
	return false
end

hexchat.hook_server_attrs('PRIVMSG', function (word, word_eol, attrs)
	-- Only want private messages
	if prefix_is_channel(word[3]:sub(1, 1)) then
		return
	end

	local mynick = hexchat.get_info('nick')
	local sender = word[1]:match('^:([^!]+)')
	local recipient = word[3]

	if hexchat.nickcmp(sender, mynick) == 0 and hexchat.nickcmp(recipient, mynick) ~= 0 then
		hexchat.command('query -nofocus ' .. recipient)
		local ctx = hexchat.find_context(hexchat.get_info('network'), recipient)
		local message = word_eol[4]
		if message:sub(1, 1) == ':' then
			message = message:sub(2)
		end

		if message:sub(1, 8) == '\001ACTION ' then
			local action = message:sub(9, #message-1)
			ctx:emit_print_attrs(attrs, 'Your Action', mynick, action)
		else
			ctx:emit_print_attrs(attrs, 'Your Message', mynick, message)
		end

		return hexchat.EAT_ALL
	end
end)
