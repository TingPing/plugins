-- SPDX-License-Identifier: MIT
hexchat.register('Buffextras', '1', "Format messages from ZNC's buffextras module")

local function strip_brackets (str)
	return str:sub(2, #str - 1)
end

hexchat.hook_server_attrs('PRIVMSG', function (word, word_eol, attrs)
	if not word[1]:match('^:%*buffextras!') then
		return
	end

	local channel = word[3]
	local nick, host = word[4]:match('^:([^!]+)!(.*)$')

	-- don't eat modes & kicks from servers (we can't split them into nick + host)
	if nick == '' or nick == nil then
		nick = word[4]:sub(2) -- chop off leading ":"
	end

	local function is_event (event)
		return word_eol[5]:sub(1, #event) == event
	end

	local function emit (event, ...)
		hexchat.emit_print_attrs(attrs, event, ...)
	end

	if is_event('joined') then
		emit('Join', nick, channel, host)
	elseif is_event('quit with message') then
		emit('Quit', nick, strip_brackets(word_eol[8]), host)
	elseif is_event('quit:') then
		emit('Quit', nick, word_eol[6], host)
	elseif is_event('parted with message') then
		local reason = strip_brackets(word_eol[8])
		if reason ~= '' then
			emit('Part with Reason', nick, host, channel, reason)
		else
			emit('Part', nick, host, channel)
		end
	elseif is_event('parted:') then
		local reason = word_eol[6]
		if reason ~= '' then
			emit('Part with Reason', nick, host, channel, reason)
		else
			emit('Part', nick, host, channel)
		end
	elseif is_event('is now known as') then
		emit('Change Nick', nick, word[9])
	elseif is_event('changed the topic to') then
		emit('Topic Change', nick, word_eol[9], channel)
	elseif is_event('kicked') then
		if word[7] == "Reason:" then
			emit('Kick', nick, word[6], channel, strip_brackets(word_eol[8]))
		else
			emit('Kick', nick, word[6], channel, word_eol[9])
		end
	elseif is_event('set mode') then
		emit('Raw Modes', nick, string.format('%s %s', channel, word_eol[7]))
	else
		return -- Unknown event
	end

	return hexchat.EAT_ALL
end, hexchat.PRI_HIGH)
