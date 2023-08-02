import time
import uuid
from django.core.management.base import BaseCommand
from moviepy.editor import VideoFileClip, CompositeVideoClip
from video.models import Video
from django.conf import settings


class Command(BaseCommand):
    """
        Process video and upload youtube
    """

    def run_command(self):
        print('Processando')
        is_processing = Video.objects.filter(status=Video.S_PROCESSING).exists()

        if is_processing:
            return

        videos = Video.objects.filter(status=Video.S_PENDING).all()

        for video in videos:

            video.status = Video.S_PROCESSING
            video.file_name = str(uuid.uuid4())[:32]
            video.save()

            try:

                clip = VideoFileClip(str(settings.BASE_DIR) + video.video.url)

                image_gif = (VideoFileClip('media/image/original.gif', has_mask=True)
                             .loop()
                             .set_duration(clip.duration)
                             .resize(width=568, height=349)
                             .set_position((12, 1100)))

                video_composite = CompositeVideoClip([clip, image_gif])
                video_composite.write_videofile(
                    "output/{}.mp4".format(video.file_name), fps=60)

                video.status = Video.S_PROCESSING_SUCCESS

            except Exception:
                video.status = Video.S_PROCESSING_FAIL

            video.save()

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
