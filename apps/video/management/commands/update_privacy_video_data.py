
import time
from datetime import datetime, timedelta

import httplib2
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from googleapiclient.discovery import build
from oauth2client.file import Storage
from video.models import Video


class Command(BaseCommand):
    """
        update data video youtube
    """

    def run_command(self):

        def get_authenticated_service():
            storage = Storage(f"{str(settings.BASE_DIR)}/youtube-oauth2.json")
            credentials = storage.get()

            if credentials is None or credentials.invalid:
                print('credentials invalid!')
                return None

            return build(
                settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION,
                http=credentials.authorize(httplib2.Http())
            )

        youtube = get_authenticated_service()
        videos = Video.objects.filter(status=Video.S_SUCCESS).exclude(privacy_status='public').order_by('id').all()
        publish_at = datetime(2023, 8, 28, 00, 00, 00)

        for video in videos:
            request = youtube.videos().update(
                part="status",
                body={
                    "id": video.youtube_id,
                    "status": {
                        "privacyStatus": "private",
                        "publishAt": publish_at.strftime('%Y-%m-%dT%H:%M:%SZ')
                    }
                }
            )
            response = request.execute()

            print(response)
            publish_at += timedelta(hours=6)

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
