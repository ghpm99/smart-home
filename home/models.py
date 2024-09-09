from django.db import models


# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=256)
    path = models.CharField(max_length=512)
    format = models.CharField(max_length=256)
    size = models.IntegerField()
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    last_interaction = models.DateTimeField(auto_now=True)
    last_backup = models.DateTimeField(null=True)


class Disk(models.Model):
    name = models.CharField(max_length=512)
    mountpoint = models.CharField(max_length=256)
    fstype = models.CharField(max_length=16)
    opts = models.CharField(max_length=512)
