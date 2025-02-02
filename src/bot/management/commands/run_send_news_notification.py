import logging

from api.models import Article
from django.core.management import BaseCommand

from bot.app.notifications.news_notification_handler import NewsNotificationHandler

logger = logging.getLogger(__name__)

TAG = 'Notification Server'


class Command(BaseCommand):
    help = 'Run Notifications manually.'

    def add_arguments(self, parser):
        parser.add_argument('-version', dest="version", type=str)

    def handle(self, *args, **options):
        logger.info('Running Notifications...')
        notification = NewsNotificationHandler()
        article = Article.objects.filter(created_at__isnull=False).latest('created_at')
        notification.send_notification(article)

