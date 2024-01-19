import os
import shutil
import time
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from home.models import File
from django.utils import timezone
from django.db.models import F, Q


class Command(BaseCommand):
    """
        Backup shared files
    """

    def run_command(self):

        print('Iniciando backup de arquivos')
        backup_start = datetime.now(tz=timezone.utc)
        meta_data = f'bkp_{backup_start.strftime("%Y%m%d_%H%M%S")}.txt'
        Path(settings.BACKUP_FOLDER).mkdir(parents=True, exist_ok=True)

        for root, dirs, files in os.walk(settings.SHARED_FOLDER):

            for file in files:
                new_file, created = File.objects.get_or_create(
                    name=file,
                    path=root,
                    defaults={
                        'format': file.split('.')[-1],
                        'size': os.path.getsize(f'{root}/{file}'),
                        'updated_at': datetime.fromtimestamp(os.path.getmtime(f'{root}/{file}'), tz=timezone.utc),
                        'created_at': datetime.fromtimestamp(os.path.getctime(f'{root}/{file}'), tz=timezone.utc),
                        'last_interaction': backup_start,
                    }
                )
                if created:
                    print(f'Arquivo {file} criado')
                else:
                    new_file.last_interaction = backup_start
                    new_file.save()

        files_to_backup = File.objects.filter(Q(last_backup__isnull=True) | Q(last_backup__lte=F('updated_at'))).all()

        print(f'Arquivos para backup: {files_to_backup.count()}')
        print(f'Lista de arquivos pode ser encontrado em {settings.BACKUP_FOLDER}{meta_data}')

        with open(f'{settings.BACKUP_FOLDER}{meta_data}', 'a+', encoding='utf-8') as f:
            f.write(f'Arquivos para backup: {files_to_backup.count()}\n')
            f.write(f'Horario de inicio: {backup_start.strftime("%Y-%m-%d %H:%M:%S")}\n')
            for file in files_to_backup:
                f.write(f'{file.path}{file.name}\n')
            f.close()

        for file_to_backup in files_to_backup:
            dir = file_to_backup.path.replace(settings.SHARED_FOLDER, settings.BACKUP_FOLDER)
            Path(dir).mkdir(parents=True, exist_ok=True)
            target_file = f'{file_to_backup.path}/{file_to_backup.name}'
            print(f'Copiando {target_file} para {dir}')
            shutil.copy(target_file, dir)

        print('Concluiu')

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
