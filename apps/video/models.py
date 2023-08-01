from django.db import models


# Create your models here.
class Video(models.Model):
    S_PENDING = 0
    S_PROCESSING = 1
    S_UPLOADING = 2
    S_SUCCESS = 2
    S_FAIL = 3

    STATUS = [
        (S_PENDING, "Pendente"),
        (S_PROCESSING, "Processando"),
        (S_UPLOADING, "Enviando"),
        (S_SUCCESS, "Sucesso"),
        (S_FAIL, "Falhou"),
    ]

    title = models.CharField(max_length=100, null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True)
    status = models.IntegerField(choices=STATUS, default=S_PENDING)

