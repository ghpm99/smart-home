import time
from django.core.management.base import BaseCommand
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, VideoFileClip
from video.models import Video
from django.conf import settings


class Command(BaseCommand):
    """
        Process video and upload youtube
    """

    def run_command(self):
        print('Processando')
        videos = Video.objects.filter(status=Video.S_PENDING).all()

        for video in videos:

            video.status = Video.S_PROCESSING
            video.save()

            clip = VideoFileClip(str(settings.BASE_DIR) + video.video.url)

            image = VideoFileClip('media/image/original.gif').set_start(0).set_position(('left', 'left'))

            video_composite = CompositeVideoClip([clip, image])
            video_composite.write_videofile("output/{}.mp4".format(video.title), fps=60)

            video.status = Video.S_UPLOADING
            video.save()


    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
