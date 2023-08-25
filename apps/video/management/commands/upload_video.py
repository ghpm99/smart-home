
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
from oauth2client.file import Storage
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
        upload video to youtube
    """

    def run_command(self):

        print('Realizando upload')
        is_upload = Video.objects.filter(status=Video.S_UPLOADING).exists()

        if is_upload:
            print('Já existe video sendo feito upload')
            return

        def get_authenticated_service():
            storage = Storage(f"{str(settings.BASE_DIR)}/youtube-oauth2.json")
            credentials = storage.get()

            if credentials is None or credentials.invalid:
                print('credentials invalid!')
                return None

            return build(
                settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION,
                http=credentials.authorize(httplib2.Http())
            )

        def resumable_upload(insert_request, video: Video):
            response = None
            error = None
            retry = 0
            while response is None:
                try:
                    print("Uploading file...")
                    status, response = insert_request.next_chunk()
                    if response is not None:
                        if 'id' in response:
                            video.youtube_id = response.get('id')
                            video_status = response.get('status')
                            video.upload_status = video_status.get('uploadStatus')
                            video.privacy_status = video_status.get('privacyStatus')

                            video_statistics = response.get('statistics')
                            video.view_count = video_statistics.get('viewCount')
                            video.like_count = video_statistics.get('likeCount')
                            video.dislike_count = video_statistics.get('dislikeCount')
                            video.comment_count = video_statistics.get('commentCount')

                            print("Video id '%s' was successfully uploaded." %
                                  response['id'])
                        else:
                            video.status = Video.S_FAIL
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

        category = '20'
        privacy = 'private'

        video = Video.objects.filter(
            Q(status=Video.S_PROCESSING_SUCCESS) | Q(status=Video.S_FAIL)
        ).first()

        youtube = get_authenticated_service()

        video.status = Video.S_UPLOADING
        video.save()

        if video.keywords:
            tags = list(set(video.keywords.split(',')))
        else:
            tags = ['Black Desert Online', 'Arena Solare', 'Luta Competitiva', 'Batalha Épica', 'PvP', 'Estratégia',
                    'Combate', 'MMO', 'Jogo Online', 'Ação', 'Emoção', 'Awakening', 'Witch', 'Bruxa', 'SA']

        try:
            print('Gerando youtube build')
            video_title = f"{video.title} #{video.id}"

            body = dict(
                snippet=dict(
                    title=video_title,
                    description=video.description,
                    tags=tags,
                    categoryId=category
                ),
                status=dict(
                    privacyStatus=privacy
                ),
                statistics=dict(
                    viewCount=''
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
            resumable_upload(insert_request, video)

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
