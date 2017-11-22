-- SPDX-License-Identifier: MIT
hexchat.register('ZNC Buffers', '1', 'Add menu options to manage ZNC buffers')

-- Add menus
hexchat.command('menu -p4 add "$TAB/ZNC"')
hexchat.command('menu add "$TAB/ZNC/Clear Buffer" ".zncclearbuffer %s"')
hexchat.command('menu add "$TAB/ZNC/Play Buffer" "znc playbuffer %s"')
hexchat.hook_unload(function () hexchat.command('menu del "$TAB/ZNC') end)


-- Ignore our own actions
local recently_cleared = {}

hexchat.hook_command('.zncclearbuffer', function(word, word_eol)
	local name = word[2]

	-- Ignore znc queries
	if name:sub(1, 1) ~= '*' then
		recently_cleared[name] = true
		hexchat.command('znc clearbuffer ' .. name)
	end

	return hexchat.EAT_ALL
end)

hexchat.hook_server('PRIVMSG', function(word, word_eol)
	local cleared_channel = word_eol[1]:match('^:%*status!znc@znc.in [^:]+:%[%d+] buffers matching %[([^%]]+)] have been cleared$')

	if cleared_channel and recently_cleared[cleared_channel] then
		recently_cleared[cleared_channel] = nil
		return hexchat.EAT_ALL
	end
end)

hexchat.hook_command('zncclosepm', function (word, word_eol)
  local id = hexchat.props.id

  for chan in hexchat.iterate('channels') do
    if chan.id == id and chan.type == 3 then
      hexchat.command('.zncclearbuffer ' .. chan.channel)
      chan.context:command('close')
    end
  end

  return hexchat.EAT_ALL
end)
