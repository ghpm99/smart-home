import time

import psutil
from django.core.management.base import BaseCommand

from home.models import Disk


class Command(BaseCommand):
    """
    Update disk db
    """

    def run_command(self):
        for disk in psutil.disk_partitions():
            is_exists = Disk.objects.filter(name=disk.device, mountpoint=disk.mountpoint).exists()
            if is_exists is False:
                Disk.objects.create(
                    name=disk.device,
                    mountpoint=disk.mountpoint,
                    fstype=disk.fstype,
                    opts=disk.opts
                )

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS("Running..."))

        self.run_command()

        self.stdout.write(self.style.SUCCESS("Success! :)"))
        self.stdout.write(self.style.SUCCESS(f"Done with {time.time() - begin}s"))
