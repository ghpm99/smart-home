from django.contrib import admin
from home.models import File, Disk


# Register your models here.
class FileConfig(admin.ModelAdmin):
    list_display = ['id', 'name', 'path', 'format', 'size']
    pass


admin.site.register(File, FileConfig)


class DiskConfig(admin.ModelAdmin):
    list_display = ['id', 'name', 'mountpoint', 'fstype', 'opts']
    pass


admin.site.register(Disk, DiskConfig)
