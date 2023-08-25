
from django.urls import path

from . import views

urlpatterns = [
    path('', view=views.video, name='video'),
    path('new', view=views.new_video, name='new_video'),
]
