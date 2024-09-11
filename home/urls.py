
from django.urls import include, path

from . import views

urlpatterns = [
    path('', view=views.home, name='home'),
    path('media/', include([
        path('files', view=views.files, name='media-files'),
        path('documents', view=views.documents, name='media-documents'),
        path('images', view=views.images, name='media-images'),
        path('video', view=views.video, name='media-video')
    ]))
]
