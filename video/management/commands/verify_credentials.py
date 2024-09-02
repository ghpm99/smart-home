
import argparse
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow


class Command(BaseCommand):
    """
        verify credentials youtube
    """

    def run_command(self):

        print('Verificando credenciais')

        flow = flow_from_clientsecrets(
            f"{str(settings.BASE_DIR)}{settings.CLIENT_SECRETS_FILE}",
            scope=settings.YOUTUBE_UPLOAD_SCOPE,
            message=settings.MISSING_CLIENT_SECRETS_MESSAGE
        )

        storage = Storage(f"{str(settings.BASE_DIR)}/youtube-oauth2.json")
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            print('Credenciais invalidas')
            flags = argparse.Namespace(
                logging_level='ERROR',
                noauth_local_webserver=True
            )
            credentials = run_flow(flow, storage, flags)

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
