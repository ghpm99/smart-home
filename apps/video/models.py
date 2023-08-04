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

    STATUS = [
        (S_PENDING, "Pendente"),
        (S_PROCESSING, "Processando"),
        (S_PROCESSING_FAIL, "Processamento falhou"),
        (S_PROCESSING_SUCCESS, "Processamento concluido"),
        (S_UPLOADING, "Enviando"),
        (S_SUCCESS, "Sucesso"),
        (S_FAIL, "Falhou"),
    ]

    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True)
    status = models.IntegerField(choices=STATUS, default=S_PENDING)
    file_name = models.CharField(max_length=32, null=True, blank=True)
    youtube_id = models.CharField(max_length=12, null=True, blank=True)
    file_base = models.CharField(max_length=255, null=True, blank=True)
