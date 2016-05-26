local lgi = require('lgi')
local GLib = lgi.require('GLib')
local Gio = lgi.require('Gio')

hexchat.register('NowPlaying', '1', 'Announce songs from MPRIS2 clients')

-- TODO: Everything Async
local bus = Gio.bus_get_sync(Gio.BusType.SESSION)

local function get_players ()
	local ret, err = bus:call_sync('org.freedesktop.DBus', -- bus
	                               '/org/freedesktop/DBus', -- object
	                               'org.freedesktop.DBus', -- interface
	                               'ListNames', -- method
	                               nil, -- params
	                               GLib.VariantType('(as)'), -- return type
	                               Gio.DBusCallFlags.NONE, 1000)

	if err then
		print('NP: Error ' .. tostring(err))
		return nil
	elseif #ret ~= 1 then
		return nil
	end

	local players = {}
	local array = ret.value[1]
	for i = 1, #array do
		local player_name = array[i]:match('^org%.mpris%.MediaPlayer2%.([^.]+)$')
		if player_name then
			players[#players + 1] = player_name
		end
	end

	if #players == 0 then
		return nil
	else
		return players
	end
end

local function print_nowplaying (player)
	local ret, err = bus:call_sync('org.mpris.MediaPlayer2.' .. player,
	                               '/org/mpris/MediaPlayer2',
	                               'org.freedesktop.DBus.Properties',
	                               'Get',
	                               GLib.Variant('(ss)', {'org.mpris.MediaPlayer2.Player', 'Metadata'}),
	                               GLib.VariantType('(v)'), 
	                               Gio.DBusCallFlags.NONE, 1000)

	if err then
		print('NP: Error ' .. tostring(err))
		return
	elseif #ret ~= 1 then
		return
	end

	local metadata = ret[1].value -- a{sv}
	local title = metadata['xesam:title']
	local artist = metadata['xesam:artist'][1]
	local album = metadata['xesam:album']
	-- TODO: Handle any of these missing

	-- TODO: Support customizing the command
	hexchat.command(string.format('me is now playing %s by %s on %s.', title, artist, album))
end

hexchat.hook_command('np', function (word, word_eol)
	local players = get_players()

	if not players then
		print('NP: No player found running.')
	elseif #word > 1 then
		local player = word[2]:lower()

		for _, name in pairs(players) do
			if player == name:lower() then
				print_nowplaying(name)
				return hexchat.EAT_ALL
			end
		end

		print('NP: Player ' .. word[2] .. ' not found.')
	elseif #players == 1 then
		print_nowplaying(players[1])
	else
		print('NP: You have multiple players running, please specify a name:\n\t' .. tostring(players))
	end

	return hexchat.EAT_ALL
end, 'NP [player]')
