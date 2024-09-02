
import time
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from video.models import Video


class Command(BaseCommand):
    """
        update data video youtube
    """

    def run_command(self):

        videos = Video.objects.exclude(privacy_status='public').order_by('id').all()
        publish_at = datetime(2023, 8, 28, 3, 0, 0)

        for video in videos:
            if publish_at.hour > 3 and publish_at.hour < 14:
                publish_at += timedelta(hours=8)

            video.publish_at = publish_at
            video.save()

            publish_at += timedelta(hours=4)

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
