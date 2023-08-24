
import time

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

        videos = Video.objects.filter(status=Video.S_SUCCESS).order_by('id').all()

        videos_paginator = Paginator(videos, 50)

        print(videos_paginator.num_pages)

        separator = ','
        current_page = 1

        while current_page <= videos_paginator.num_pages:
            videos_id = []

            for video in videos_paginator.get_page(current_page):
                videos_id.append(video.youtube_id)

            youtube_id_separator = separator.join(videos_id)

            youtube = get_authenticated_service()

            request = youtube.videos().list(
                part="statistics,status",
                id=youtube_id_separator
            )
            response = request.execute()

            for youtube_data in response.get('items'):
                video_youtube = Video.objects.filter(youtube_id=youtube_data.get('id')).first()
                video_status = youtube_data.get('status')
                video_youtube.upload_status = video_status.get('uploadStatus')
                video_youtube.privacy_status = video_status.get('privacyStatus')
                video_statistics = youtube_data.get('statistics')
                video_youtube.view_count = video_statistics.get('viewCount')
                video_youtube.like_count = video_statistics.get('likeCount')
                video_youtube.dislike_count = video_statistics.get('dislikeCount')
                video_youtube.comment_count = video_statistics.get('commentCount')
                video_youtube.save()
            current_page +=1

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
