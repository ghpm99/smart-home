from django.db import models


# Create your models here.
class Video(models.Model):
    S_PENDING = 0
    S_PROCESSING = 1
    S_PROCESSING_FAIL = 2
    S_PROCESSING_SUCCESS = 3
    S_UPLOADING = 4
    S_SUCCESS = 6
    S_FAIL = 7
    S_FINISHED = 8

    STATUS = [
        (S_PENDING, "Pendente"),
        (S_PROCESSING, "Processando"),
        (S_PROCESSING_FAIL, "Processamento falhou"),
        (S_PROCESSING_SUCCESS, "Processamento concluido"),
        (S_UPLOADING, "Enviando"),
        (S_SUCCESS, "Sucesso"),
        (S_FAIL, "Falhou"),
        (S_FINISHED, "Finalizado")
    ]

    T_SOLARE_RANKED = 0
    T_SOLARE_PRACTICE = 1
    T_BACKUP = 2
    T_UPLOAD = 3

    TYPES = [
        (T_SOLARE_RANKED, "Solare Ranked"),
        (T_SOLARE_PRACTICE, "Solare Practice"),
        (T_BACKUP, "Backup"),
        (T_UPLOAD, "Upload"),
    ]

    name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    keywords = models.TextField(max_length=500, null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True)
    status = models.IntegerField(choices=STATUS, default=S_PENDING)
    type = models.IntegerField(choices=TYPES, default=T_SOLARE_RANKED)
    file_name = models.CharField(max_length=32, null=True, blank=True)
    youtube_id = models.CharField(max_length=12, null=True, blank=True)
    file_base = models.CharField(max_length=255, null=True, blank=True)
    upload_status = models.CharField(max_length=32, null=True, blank=True)
    privacy_status = models.CharField(max_length=32, null=True, blank=True)
    view_count = models.CharField(max_length=32, null=True, blank=True)
    like_count = models.CharField(max_length=32, null=True, blank=True)
    dislike_count = models.CharField(max_length=32, null=True, blank=True)
    comment_count = models.CharField(max_length=32, null=True, blank=True)
    publish_at = models.DateTimeField(null=True)
