hexchat.register('WordHL', '1', 'Highlights some words of importance')
-- When you want to notice something, but not really get 'highlighted'

local HLWORDS = {
	'hexchat',
	'HexChat',
} -- case sensitive
local COLOR = '20' -- Red


local function replace_word (message, word, replacement)
	local patterns = {
		['^'  .. word .. '%s'] = replacement .. ' ',
		['^'  .. word .. '$'] = replacement,
		['%s' .. word .. '%s'] = ' ' .. replacement .. ' ',
		['%s' .. word ..  '$'] = ' ' .. replacement,
	} -- Match word at start, middle, or end of string

	for pattern, sub in pairs(patterns) do
		message = message:gsub(pattern, sub)
	end

	return message
end

local event_edited = false
local function on_message (args, event_type)
	if event_edited then
		return -- Ignore own events
	end

	local message = args[2]
	for _, word in ipairs(HLWORDS) do
		message = replace_word (message, word, '\003' .. COLOR .. word .. '\00399')
	end

	if message ~= args[2] then
		event_edited = true
		args[2] = message
		hexchat.emit_print(event_type, unpack(args))
		event_edited = false

		hexchat.command('gui color 3')
		return hexchat.EAT_ALL
	end

end

for _, event in ipairs({'Channel Action', 'Channel Message'}) do
	hexchat.hook_print(event, function (args)
		on_message (args, event)
	end, hexchat.PRI_HIGH)
end
