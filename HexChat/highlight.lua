-- SPDX-License-Identifier: MIT
hexchat.register('Highlights', '1', 'Prints highlights to another tab')

local TAB_NAME = '(highlights)'
local OPEN_PER_SERVER = false

local function find_highlighttab ()
	local network = nil
	if OPEN_PER_SERVER then
		network = hexchat.get_info('network')
	end
	local ctx = hexchat.find_context(network, TAB_NAME)
	if not ctx then
		if OPEN_PER_SERVER then
			hexchat.command('query -nofocus ' .. TAB_NAME)
		else
			local newtofront = hexchat.prefs['gui_tab_newtofront']
			hexchat.command('set -quiet gui_tab_newtofront off')
			hexchat.command('newserver -noconnect ' .. TAB_NAME)
			hexchat.command('set -quiet gui_tab_newtofront ' .. tostring(newtofront))
		end

		return hexchat.find_context(network, TAB_NAME)
	end

	return ctx
end

local function on_highlight (args, event_type)
	local channel = hexchat.get_info('channel')
	local highlight_context = find_highlighttab()

	local format
	if event_type == 'Channel Msg Hilight' then
		format = '\00322%s\t\00318<%s%s%s>\015 %s'
	elseif event_type == 'Channel Action Hilight' then
		format = '\00322%s\t\002\00318%s%s%s\015 %s'
	end

	highlight_context:print(string.format(format, channel,
	                       args[3] or '', args[4] or '', hexchat.strip(args[1]), args[2]))
	highlight_context:command('gui color 0') -- Ignore colors
end

for _, event in ipairs({'Channel Msg Hilight', 'Channel Action Hilight'}) do
	hexchat.hook_print(event, function (args)
		return on_highlight(args, event)
	end, hexchat.PRI_LOW)
end
