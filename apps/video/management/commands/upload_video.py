
import http.client
import random
import time

import httplib2
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from video.models import Video

httplib2.RETRIES = 1

MAX_RETRIES = 10

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                        http.client.IncompleteRead, http.client.ImproperConnectionState,
                        http.client.CannotSendRequest, http.client.CannotSendHeader,
                        http.client.ResponseNotReady, http.client.BadStatusLine)


class Command(BaseCommand):
    """
        Process video and upload youtube
    """

    def run_command(self):

        print('Realizando upload')
        is_upload = Video.objects.filter(status=Video.S_UPLOADING).exists()

        if is_upload:
            print('Já existe video sendo feito upload')
            return

        def resumable_upload(insert_request):
            response = None
            error = None
            retry = 0
            while response is None:
                try:
                    print("Uploading file...")
                    status, response = insert_request.next_chunk()
                    if response is not None:
                        if 'id' in response:
                            print("Video id '%s' was successfully uploaded." %
                                  response['id'])
                        else:
                            exit(
                                "The upload failed with an unexpected response: %s" % response)
                except HttpError as e:
                    if e.resp.status in RETRIABLE_STATUS_CODES:
                        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                             e.content)
                    else:
                        raise
                except RETRIABLE_EXCEPTIONS as e:
                    error = "A retriable error occurred: %s" % e

                if error is not None:
                    print(error)
                    retry += 1
                    if retry > MAX_RETRIES:
                        exit("No longer attempting to retry.")

                    max_sleep = 2 ** retry
                    sleep_seconds = random.random() * max_sleep
                    print("Sleeping %f seconds and then retrying..." %
                          sleep_seconds)
                    time.sleep(sleep_seconds)

        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        keywords = 'black desert,bdo,solare,witch awakening,witch,bruxa,black desert sa'
        category = '20'
        privacy = 'private'
        tags = keywords.split(',')

        videos = Video.objects.filter(
            Q(status=Video.S_PROCESSING_SUCCESS) | Q(status=Video.S_FAIL)
        ).all()

        for video in videos:

            video.status = Video.S_UPLOADING
            video.save()

            try:
                print('Gerando youtube build')
                youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                                developerKey=settings.YOUTUBE_API_KEY)

                body = dict(
                    snippet=dict(
                        title=video.title,
                        description=video.description,
                        tags=tags,
                        categoryId=category
                    ),
                    status=dict(
                        privacyStatus=privacy
                    )
                )
                print('Criando request')
                insert_request = youtube.videos().insert(
                    part=",".join(body.keys()),
                    body=body,
                    media_body=MediaFileUpload(
                        f"{str(settings.BASE_DIR)}/output/{video.file_name}.mp4",
                        chunksize=-1,
                        resumable=True
                    )
                )
                print('Iniciando envio')
                resumable_upload(insert_request)

                print('Envio finalizado')

                video.status = Video.S_SUCCESS

            except Exception as e:
                print('Falhou no envio')
                print(e)
                video.status = Video.S_FAIL

            video.save()

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
