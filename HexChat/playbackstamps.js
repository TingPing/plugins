SCRIPT_NAME = 'PlaybackStamps';
SCRIPT_VER = '1';
SCRIPT_DESC = 'Prints date on older playback messages';
// I wrote this in Python first but this is noticably faster

const events = ['Channel Message', 'Channel Msg Hilight',
                'Channel Action', 'Channel Action Hilight',
                'Your Action', 'Your Message'];

var edited = false;

function is_today (event_time)
{
	let now = new Date();
	let etime = new Date(event_time); // Duplicate since we edit it later

	if (now.getTime() - etime.getTime() > 86400000)
		return false; // Was over 24hrs ago

	// Set time to 0, we only care about date
	if (etime.setHours(0,0,0,0) != now.setHours(0,0,0,0))
		return false; // Different date

	return true;
}

function msg_cb(word, event_time, event)
{
	if (edited || is_today(event_time))
		return EAT_NONE;

	let format = get_prefs('stamp_text_format');
	command('set -quiet stamp_text_format' + ' %m-%d ' + format);

	edited = true;
	emit_print_at(event_time, event, word[0], word[1]);
	edited = false;

	command('set -quiet stamp_text_format ' + format);

	return EAT_ALL;
}

for each (let event in events) {
	hook_print(event, msg_cb, event, PRI_LOWEST);
}
