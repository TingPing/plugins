-- SPDX-License-Identifier: MIT
hexchat.register('RequireSASL', '1', 'Disconnect if SASL fails')

hexchat.hook_print('SASL Response', function (args)
	if args[2] == '904' then
		-- Delayed so print happens first
		hexchat.command('timer .1 discon')
	end
end)
