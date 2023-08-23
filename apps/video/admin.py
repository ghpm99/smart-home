from django.contrib import admin
from video.models import Video, VideoYoutube


# Register your models here.
class VideoConfig(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'file_name', 'youtube_id', 'file_base']
    pass


class VideoYoutubeConfig(admin.ModelAdmin):
    list_display = ['id', 'youtube_id', 'upload_status', 'privacy_status']
    pass


admin.site.register(VideoYoutube, VideoYoutubeConfig)
admin.site.register(Video, VideoConfig)
