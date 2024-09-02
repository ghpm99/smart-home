from django.contrib import admin
from video.models import Video


# Register your models here.
class VideoConfig(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'file_name', 'youtube_id', 'privacy_status', 'view_count', 'file_base']
    pass


admin.site.register(Video, VideoConfig)
