import os
from pathlib import Path
import time
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from home.models import File


class Command(BaseCommand):
    """
        Backup shared files
    """

    def run_command(self):

        print('Iniciando backup de arquivos')

        for root, dirs, files in os.walk(settings.SHARED_FOLDER):

            dir = root.replace(settings.SHARED_FOLDER, settings.BACKUP_FOLDER)
            print(dir)
            Path(dir).mkdir(parents=True, exist_ok=True)

            for file in files:
                new_file, created = File.objects.get_or_create(
                    name=file,
                    path=root,
                    format=file.split('.')[-1]
                )
                if created:
                    print(f'Arquivo {file} criado')

                with open(file, 'w+', encoding='utf-8') as f:
                    data = {
                        'id': new_file.id,
                        'name': new_file.name,
                        'path': new_file.path,
                        'format': new_file.format,
                        'size': os.path.getsize(f'{root}/{file}'),
                        'last_modified': time.ctime(os.path.getmtime(f'{root}/{file}')),
                        'created': time.ctime(os.path.getctime(f'{root}/{file}'))
                    }
                    json.dump(data, f, ensure_ascii=False, indent=4)

        print('Concluiu')

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
