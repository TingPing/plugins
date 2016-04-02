hexchat.register('MyMessage', '1', 'Properly show your own messages in ZNC playback')

hexchat.hook_print('Capability List', function (args)
	if args[2]:find('znc.in/self%-message') then
		hexchat.command('CAP REQ znc.in/self-message')
	end
end)

hexchat.hook_server_attrs('PRIVMSG', function (word, word_eol, attrs)
	-- Only want private messages
	if word[3]:sub(1, 1) == '#' then
		return -- TODO: More robust check
	end

	local mynick = hexchat.get_info('nick')
	local sender = word[1]:match('^:([^!]+)')
	local recipient = word[3]
	local network = hexchat.get_info('network')
	local message = word_eol[4]
	if message:sub(1, 1) == ':' then
		message = message:sub(2)
	end

	if hexchat.nickcmp(sender, mynick) == 0 and hexchat.nickcmp(recipient, mynick) ~= 0 then
		hexchat.command('query -nofocus ' .. recipient)
		local ctx = hexchat.find_context(network, recipient)

		if message:sub(1, 8) == '\001ACTION ' then
			local action = message:sub(9, #message-1)
			ctx:emit_print_attrs(attrs, 'Your Action', mynick, action)
		else
			ctx:emit_print_attrs(attrs, 'Your Message', mynick, message)
		end

		return hexchat.EAT_ALL
	end
end)
