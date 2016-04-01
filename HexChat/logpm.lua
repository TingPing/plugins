hexchat.register('LogPM', '1', 'Automatically log private queries')

hexchat.hook_print('Open Context', function (args)
	local channel = hexchat.get_info('channel')

	-- Ignore channels, empty tabs, znc queries, and scripting consoles
	if not channel:match('^[#%*%(>]') then
		hexchat.command('chanopt -quiet text_logging on')
	end

end)
