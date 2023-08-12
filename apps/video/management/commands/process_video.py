import time
import uuid
import httplib2
import http.client
import random

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from moviepy.editor import CompositeVideoClip, VideoFileClip
from video.models import Video
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.file import Storage


httplib2.RETRIES = 1

MAX_RETRIES = 10

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                        http.client.IncompleteRead, http.client.ImproperConnectionState,
                        http.client.CannotSendRequest, http.client.CannotSendHeader,
                        http.client.ResponseNotReady, http.client.BadStatusLine)


class Command(BaseCommand):
    """
        Process video
    """

    def run_command(self):

        print('Processando')
        is_processing = Video.objects.filter(
            status=Video.S_PROCESSING
        ).exists()

        if is_processing:
            print('Existe video sendo processado!')
            return

        videos = Video.objects.filter(
            Q(status=Video.S_PENDING) | Q(status=Video.S_PROCESSING_FAIL)
        ).all()

        keywords = 'black desert,bdo,solare,witch awakening,witch,bruxa,black desert sa'
        category = '20'
        privacy = 'private'
        tags = keywords.split(',')

        def process_video(video: Video):
            video.status = Video.S_PROCESSING
            if video.file_name is None:
                video.file_name = str(uuid.uuid4())[:32]
            video.save()

            try:
                print('Buscando arquivo de video')
                clip = VideoFileClip(
                    f'{str(settings.BASE_DIR)}{video.video.url}'
                )

                print('Buscando gif de overlay')
                image_gif = (VideoFileClip(f'{str(settings.BASE_DIR)}/media/image/original.gif', has_mask=True)
                             .loop()
                             .set_duration(clip.duration)
                             .resize(width=732, height=513)
                             .set_position((12, 927)))

                print('Mesclando video e overlay')
                video_composite = CompositeVideoClip([clip, image_gif])

                print('Renderizando video')
                video_composite.write_videofile(
                    f"{str(settings.BASE_DIR)}/output/{video.file_name}.mp4", fps=60
                )

                print('Processo concluido')
                video.status = Video.S_PROCESSING_SUCCESS

            except Exception as e:
                print('Processo falhou')
                print(e)
                video.status = Video.S_PROCESSING_FAIL

            video.save()

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
                            video.youtube_id = response['id']
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

        def upload_video(video: Video):
            if youtube is None:
                video.status = Video.S_FAIL
                video.save()
                print('youtube is none')
                return

            video.status = Video.S_UPLOADING
            video.save()

            try:
                print('Gerando youtube build')

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
                resumable_upload(insert_request, video)

                print('Envio finalizado')

                video.status = Video.S_SUCCESS

            except Exception as e:
                print('Falhou no envio')
                print(e)
                video.status = Video.S_FAIL

            video.save()

        youtube = get_authenticated_service()

        for video in videos:

            process_video(video)

            upload_video(video)

    def handle(self, *args, **options):
        begin = time.time()

        self.stdout.write(self.style.SUCCESS('Running...'))

        self.run_command()

        self.stdout.write(self.style.SUCCESS('Success! :)'))
        self.stdout.write(self.style.SUCCESS(
            f'Done with {time.time() - begin}s'))
