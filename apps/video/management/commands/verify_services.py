import argparse
import time
import requests

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

        print('Verificando serviços')

        r = requests.get(settings.KAWORI_API)
        if r.status_code != 200:
            requests.post(settings.WEBHOOK_URL, json={'content': 'Serviço offline'})


    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
