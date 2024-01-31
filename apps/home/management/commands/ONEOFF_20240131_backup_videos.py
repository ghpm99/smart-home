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

        processed_videos = Video.objects.filter(id__gte=800).filter(
            Q(status=Video.S_PROCESSING_SUCCESS)
            | Q(status=Video.S_UPLOADING)
            | Q(status=Video.S_SUCCESS)
            | Q(status=Video.S_FAIL)
            | Q(type=Video.T_BACKUP)
        ).all()

        files_to_update = []

        for video in processed_videos:
            if video.file_base is None:
                video.file_base = video.video.name

            try:
                url_file_proccessed = (
                    f"{str(settings.BASE_DIR)}/output/{video.file_name}.mp4"
                )

                if os.path.isfile(url_file_proccessed):
                    dir = f"{str(settings.SHARED_FOLDER)}Videos/backup"
                    file_name_without_ext = video.file_base.rsplit(".", maxsplit=1)[0]
                    target_file = f"{dir}/{video.id}_{file_name_without_ext}.mp4"

                    Path(dir).mkdir(parents=True, exist_ok=True)

                    print(f"Copiando {url_file_proccessed} para {target_file}")
                    shutil.copy(url_file_proccessed, target_file)

                files_to_update.append(video)

            except Exception as e:
                print(e)

        Video.objects.bulk_update(files_to_update, ["file_base"])

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS("Running..."))

        self.run_command()

        self.stdout.write(self.style.SUCCESS("Success! :)"))
        self.stdout.write(self.style.SUCCESS(f"Done with {time.time() - begin}s"))
