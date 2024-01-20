import os
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from video.models import Video


class Command(BaseCommand):
    """
        Process video and upload youtube
    """

    def run_command(self):
        size_removed = 0
        print('Limpando arquivos')

        videos = Video.objects.filter(
            status=Video.S_SUCCESS,
            youtube_id__isnull=False
        ).all()

        for video in videos:

            if video.file_base is None:
                video.file_base = video.video.name

            try:

                if video.type is not Video.T_BACKUP:
                    url_file_proccessed = f'{str(settings.BASE_DIR)}/output/{video.file_name}.mp4'
                    if os.path.isfile(url_file_proccessed):
                        size_removed += os.path.getsize(url_file_proccessed)
                        os.remove(url_file_proccessed)

                if video.video:
                    url_file_base = f'{str(settings.MEDIA_ROOT)}{video.video.name}'
                    if os.path.isfile(url_file_base):
                        size_removed += os.path.getsize(url_file_base)
                        os.remove(url_file_base)
                    video.video.delete()

                video.save()

            except Exception as e:
                print(e)

        print(f'Total de espaço liberado: {size_removed} bytes')

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
