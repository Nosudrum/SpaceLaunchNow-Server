import logging
from datetime import datetime, timedelta

from api.models import Launch
from django.core.management import BaseCommand

from bot.app.notifications.notification_handler import NotificationHandler
from bot.models import LaunchNotificationRecord

logger = logging.getLogger(__name__)

TAG = 'Notification Server'


class Command(BaseCommand):
    help = 'Run Notifications manually.'

    def add_arguments(self, parser):
        parser.add_argument('-version', dest="version", type=str)

    def handle(self, *args, **options):
        logger.info('Running Notifications...')
        notification = NotificationHandler()

        now = datetime.now()
        dayago = now - timedelta(days=1)
        launches = Launch.objects.all().filter(net__gte=dayago).order_by('net', 'id').distinct()
        for launch in launches[:1]:
            notification_obj = LaunchNotificationRecord.objects.get(launch_id=launch.id)
            # TODO pass in parameter for setting the notification_type
            notification.send_notification(launch, 'twentyFourHour', notification_obj)


