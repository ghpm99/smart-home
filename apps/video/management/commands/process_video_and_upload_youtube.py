import time
from django.core.management.base import BaseCommand
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from video.models import Video
from django.conf import settings


class Command(BaseCommand):
    """
        Create invoice
    """

    def run_command(self):
        print('Processando')
        print(settings.BASE_DIR)
        # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
        video = Video.objects.first()
        clip = VideoFileClip(str(settings.BASE_DIR) + video.video.url)

        # Reduce the audio volume (volume x 0.8)
        # clip = clip.volumex(0.8)

        # Generate a text clip. You can customize the font, color, etc.
        txt_clip = TextClip(
            "Edited By kawori Using Python", fontsize=30, color='white')

        # Say that you want it to appear 10s at the center of the screen
        txt_clip = txt_clip.set_pos('center').set_duration(10)

        # Overlay the text clip on the first video clip
        video = CompositeVideoClip([clip, txt_clip])

        # Write the result to a file (many options available !)
        video.write_videofile("output/teste.mp4")

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
