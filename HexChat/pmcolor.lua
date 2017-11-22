-- SPDX-License-Identifier: MIT
hexchat.register('PMColor', '1', 'Color PM tabs like highlights')

for _, event in pairs({'Private Message to Dialog', 'Private Action to Dialog'}) do
	hexchat.hook_print(event, function (args)
		hexchat.command('gui color 3')
	end)
end
