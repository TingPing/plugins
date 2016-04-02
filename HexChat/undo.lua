local bit = bit
if not bit then
	bit = require('bit32')
end
local lgi = require('lgi')
local Gdk = lgi.require('Gdk', '2.0')

hexchat.register('Undo', '1', 'Add keybindings to undo/redo')

local MAX_LEVELS = 10

local undobufs = {}
local redobufs = {}


local stack = {}

function stack:new ()
	local new_stack = {}
	setmetatable(new_stack, {__index=stack})
	return new_stack
end

function stack:push (val)
	if #self == MAX_LEVELS then
		table.remove(self, 1)
	end

	self[#self + 1] = val
end

function stack:pop ()
	local val = self[#self]
	self[#self] = nil
	return val
end


local function get_valid_mod (modifier)
	-- We only care about a few modifiers
	local mods = 0
	for _, mod in ipairs({0, 2, 3, 28}) do
		mods = bit.bor(mods, bit.lshift(1, mod))
	end

	return bit.band(tonumber(modifier), mods)
end

hexchat.hook_print('Key Press', function (args)
	local bufname = hexchat.get_info('channel') .. '_' .. hexchat.get_info('network')
	local key = tonumber(args[1])
	local mod = get_valid_mod(args[2])
	local input = hexchat.get_info('inputbox')

	local undostack = undobufs[bufname] or stack:new()
	local redostack = redobufs[bufname] or stack:new()
	if #undostack == 0 and #redostack == 0 then
		undobufs[bufname] = undostack
		redobufs[bufname] = redostack
	end

	if key == Gdk.KEY_z and mod == Gdk.ModifierType.CONTROL_MASK then
		local text = undostack:pop()
		if text then
			if text == input then
				redostack:push(text)
				text = undostack:pop() or ''
			end
			hexchat.command('settext ' .. text)
			hexchat.command('setcursor ' .. tostring(#text))
			redostack:push(text)
		end
	elseif (key == Gdk.KEY_y or key == Gdk.KEY_Z) and mod == Gdk.ModifierType.CONTROL_MASK then
		local text = redostack:pop()
		if text then
			if text == input then
				text = redostack:pop() or ''
			end
			hexchat.command('settext ' .. text)
			hexchat.command('setcursor ' .. tostring(#text))
		end
	else -- Any key press
		if undostack[#undostack] ~= input then
			undostack:push(input)
		end
	end
end)
