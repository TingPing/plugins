-- SPDX-License-Identifier: MIT
hexchat.register('LogPM', '2', 'Automatically log private queries')

hexchat.hook_print('Open Context', function (args)
	-- We only want queries
	if hexchat.props['type'] ~= 3 then
		return
	end

	-- Ignore empty tabs, znc queries, and scripting consoles
	if not hexchat.get_info('channel'):match('^[%*%(>]') then
		hexchat.command('chanopt -quiet text_logging on')
	end
end)
