import os
from pathlib import Path
import shutil
import time
import uuid

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from moviepy.editor import CompositeVideoClip, VideoFileClip
from video.models import Video


class Command(BaseCommand):
    """
        Process video
    """

    def run_command(self):

        print('Processando')
        is_processing = Video.objects.filter(
            status=Video.S_PROCESSING
        ).exists()

        if is_processing:
            print('Existe video sendo processado!')
            return

        videos = Video.objects.filter(
            Q(status=Video.S_PENDING) | Q(status=Video.S_PROCESSING_FAIL)
        ).all()

        for video in videos:
            video.status = Video.S_PROCESSING
            if video.file_name is None:
                video.file_name = str(uuid.uuid4())[:32]
            video.save()

            output_file_name = f"{str(settings.BASE_DIR)}/output/{video.file_name}.mp4"

            try:
                print('Buscando arquivo de video')
                url_file_base = f'{str(settings.MEDIA_ROOT)}{video.video.name}'
                clip = VideoFileClip(url_file_base)

                if video.type is Video.T_SOLARE_RANKED or video.type is Video.T_SOLARE_PRACTICE:
                    print('Buscando gif de overlay')
                    image_gif = (
                        VideoFileClip(f'{str(settings.BASE_DIR)}/media/image/original.gif', has_mask=True)
                        .loop()
                        .set_duration(clip.duration)
                        .resize(width=732, height=513)
                        .set_position((12, 927))
                    )

                    print('Mesclando video e overlay')
                    video_composite = CompositeVideoClip([clip, image_gif])

                    print('Renderizando video')
                    video_composite.write_videofile(
                        output_file_name, fps=60
                    )
                else:
                    print('Renderizando video')
                    clip.write_videofile(
                        output_file_name, fps=60
                    )

                print('Processo concluido')
                video.status = Video.S_PROCESSING_SUCCESS

                if video.type is Video.T_BACKUP:
                    dir = f'{str(settings.SHARED_FOLDER)}Videos/backup'
                    file_name_without_ext = video.file_base.rsplit('.', maxsplit=1)[0]
                    target_file = f'{dir}/{video.id}_{file_name_without_ext}.mp4'

                    Path(dir).mkdir(parents=True, exist_ok=True)

                    print(f'Copiando {output_file_name} para {target_file}')
                    shutil.copy(output_file_name, target_file)

                if os.path.isfile(url_file_base):
                    os.remove(url_file_base)
                    print(f'Arquivo {url_file_base} removido, video {video.id}')

                video.video.delete(save=False)

            except Exception as e:
                print('Processo falhou')
                print(e)
                video.status = Video.S_PROCESSING_FAIL

            video.save()

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
