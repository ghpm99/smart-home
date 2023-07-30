from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='home', permanent=True)),
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
]
