from django.db import models


# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=256)
    path = models.CharField(max_length=512)
    format = models.CharField(max_length=256)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
