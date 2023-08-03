from django.contrib import admin
from video.models import Video


# Register your models here.
class VideoConfig(admin.ModelAdmin):
    list_display = ['id']
    pass


admin.site.register(Video, VideoConfig)
