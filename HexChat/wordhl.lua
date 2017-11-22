-- SPDX-License-Identifier: MIT
hexchat.register('WordHL', '1', 'Highlights some words of importance')
-- When you want to notice something, but not really get 'highlighted'

local function nocase (s)
      s = string.gsub(s, "%a", function (c)
            return string.format("[%s%s]", string.lower(c),
                                           string.upper(c))
          end)
      return '(' .. s .. ')'
end

local HLWORDS = {
    nocase('hexchat'),
} -- case insensitive
local COLOR = '20' -- Red

local function replace_x(s)
    return '\003' .. COLOR .. s .. '\00399'
end

local event_edited = false
local function on_message (args, event_type)
    if event_edited then
        return -- Ignore own events
    end

    local message = args[2]
    for _, word in ipairs(HLWORDS) do
        message = message:gsub("%f[%w_]" .. word .. "%f[^%w_]", replace_x)
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
        return on_message (args, event)
    end, hexchat.PRI_HIGH)
end
