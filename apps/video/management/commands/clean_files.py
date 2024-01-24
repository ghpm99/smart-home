import os
from pathlib import Path
import shutil
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from video.models import Video
from django.db.models import Q


class Command(BaseCommand):
    """
        Process video and upload youtube
    """

    def run_command(self):
        size_removed = 0
        print('Limpando arquivos')

        processed_videos = Video.objects.filter(
            Q(status=Video.S_PROCESSING_SUCCESS) |
            Q(status=Video.S_UPLOADING) |
            Q(status=Video.S_SUCCESS) |
            Q(status=Video.S_FAIL)
        ).exclude(video='').all()

        files_to_update = []

        for video in processed_videos:

            if video.file_base is None:
                video.file_base = video.video.name

            print(f'Video {video.id} já processado, removendo arquivo base')

            try:
                url_file_base = f'{str(settings.MEDIA_ROOT)}{video.video.name}'

                if os.path.isfile(url_file_base):
                    size_removed += os.path.getsize(url_file_base)
                    os.remove(url_file_base)

                video.video.delete(save=False)
                files_to_update.append(video)

            except Exception as e:
                print(e)

        Video.objects.bulk_update(files_to_update, ['video'])

        videos = Video.objects.filter(
            status=Video.S_SUCCESS,
            youtube_id__isnull=False
        ).exclude(status=Video.S_FINISHED).all()

        files_to_update = []
        for video in videos:
            try:
                url_file_proccessed = f'{str(settings.BASE_DIR)}/output/{video.file_name}.mp4'
                if os.path.isfile(url_file_proccessed):
                    if video.type is Video.T_BACKUP:
                        dir = f'{str(settings.SHARED_FOLDER)}Videos/backup'
                        file_name_without_ext = video.file_base.rsplit('.', maxsplit=1)[0]
                        target_file = f'{dir}/{video.id}_{file_name_without_ext}.mp4'

                        Path(dir).mkdir(parents=True, exist_ok=True)

                        print(f'Movendo {url_file_proccessed} para {target_file}')
                        shutil.move(url_file_proccessed, target_file)

                    else:
                        print(f'Removendo {url_file_proccessed}')
                        size_removed += os.path.getsize(url_file_proccessed)
                        os.remove(url_file_proccessed)

                    video.status = Video.S_FINNISHED
                    files_to_update.append(video)

                else:
                    print(f'Arquivo {url_file_proccessed} não existe, video {video.id}')

            except Exception as e:
                print(e)

        Video.objects.bulk_update(files_to_update, ['status'])

        print(f'Total de espaço liberado: {size_removed} bytes')

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
