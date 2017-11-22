-- SPDX-License-Identifier: MIT
hexchat.register('StatusColor', '1', 'Color nicks based upon user modes')

-- TODO: Update these to reflect default theme
local MODES = {
	['+'] = '24',
	['%'] = '28',
	['@'] = '19',
	['&'] = '21',
	['~'] = '22',
}

local edited = false
local function on_message (args, attrs, event)
	if edited then
		return hexchat.EAT_NONE
	end

	local color = MODES[args[3]]
	if not color then
		return hexchat.EAT_NONE
	end

	-- In > 2.12.3 we need to be explicit about color changes
	if event:sub(-7, -1) == 'Hilight' then
		hexchat.command('gui color 3')
	elseif event:sub(1, 4) ~= 'Your' then
		hexchat.command('gui color 2')
	end

	edited = true
	args[1] = '\003' .. color .. hexchat.strip(args[1]) .. '\00399'
	args[3] = '\003' .. color .. args[3] .. '\00399'
	hexchat.emit_print_attrs(attrs, event, unpack(args))
	edited = false

	return hexchat.EAT_ALL
end

for _, event in pairs({
	'Channel Message',
	'Channel Action',
	'Channel Msg Hilight',
	'Channel Action Hilight',
	'Your Message',
	'Your Action'
}) do
	hexchat.hook_print_attrs(event, function (args, attrs)
		return on_message(args, attrs, event)
	end, hexchat.PRI_LOW)
end
