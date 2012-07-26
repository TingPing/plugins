import logging
from xl import event, player, common
logger = logging.getLogger(__name__)
try:
	import gntp.notifier
except ImportError:
	logger.warning('gntp module not found; install https://github.com/kfdm/gntp')

class ExaileGrowl(object):

	def __init__(self):
		self.exailelogo = 'http://upload.wikimedia.org/wikipedia/commons/7/70/Exaile-logo.png'
		self.growl = gntp.notifier.GrowlNotifier(
		applicationName='Exaile',
		notifications=['Song Changed'],
		defaultNotifications=['Song Changed'],
		applicationIcon=self.exailelogo,
		#hostname='localhost',
		#password=''
		)
		self.growl.register()

	@common.threaded
	def on_play(self, type, player, track):
		self.growl.notify(
			noteType='Song Changed',
			title=track.get_tag_display('title'),
			description='by %s on %s' %(track.get_tag_display('artist'), track.get_tag_display('album')),
			icon=self.exailelogo,
			sticky=False,
			priority=0
		)

EXAILE_GROWL = ExaileGrowl()

def enable(exaile):  
	EXAILE_GROWL.exaile = exaile
	event.add_callback(EXAILE_GROWL.on_play, 'playback_track_start', player.PLAYER)


def disable(exaile):
	event.remove_callback(EXAILE_GROWL.on_play, 'playback_track_start', player.PLAYER)

