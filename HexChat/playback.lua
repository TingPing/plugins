-- SPDX-License-Identifier: MIT
local lgi = require('lgi')
local GLib = lgi.require('GLib')

hexchat.register('Playback', '1', "Integration with ZNC's Playback module")

--[[
 This should behave like this:

   On connect (end of MOTD):
       if new server, play all
       if old server, play all after latest timestamp
   On close query:
       clear all
   On new message:
       update latest timestamp
]]

local CAP_NAME = 'znc.in/playback'
local servers = {} -- Table of id to timestamp

-- Request capability
hexchat.hook_print('Capability List', function (args)
	if args[2]:find(CAP_NAME) then
		hexchat.command('quote CAP REQ :' .. CAP_NAME)

		local ctx = hexchat.props.context
		hexchat.hook_timer(1, function ()
			-- Emit this event right after the current one
			if ctx:set() then
				hexchat.emit_print('Capability Request', CAP_NAME)
			end
		end)
	end
end)

-- Capability supported
hexchat.hook_print('Capability Acknowledgement', function (args)
	local id = hexchat.prefs['id']
	if args[2]:find(CAP_NAME) and not servers[id] then
		servers[id] = 0 -- New server
	end
end)

-- On successful connection play history
hexchat.hook_server('376', function (word, word_eol)
	local timestamp = servers[hexchat.prefs['id']]

	if timestamp then
		hexchat.command('quote PRIVMSG *playback :play * ' .. tostring(timestamp))
	end
end)

-- Remove history when closed
hexchat.hook_print('Close Context', function (args)
	local id = hexchat.prefs['id']
	local timestamp = servers[id]
	if not timestamp then
		return
	end

	local ctx_type = hexchat.props['type']
	if ctx_type == 3 then -- Dialog
		hexchat.command('quote PRIVMSG *playback :clear ' .. hexchat.get_info('channel'))
	elseif ctx_type == 1 then -- Server
		servers[id] = nil
	end
end)

-- Store the timestamp of the latest message on the server
hexchat.hook_server_attrs('PRIVMSG', function (word, word_eol, attrs)
	local id = hexchat.prefs['id']
	if servers[id] then
		servers[id] = GLib.get_real_time() / 1000000 -- epoch in seconds with milisecond precision UTC
	end
end, hexchat.PRI_LOWEST)
