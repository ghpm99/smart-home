from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import Video


# Create your views here.
def video(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            video = Video(video=request.FILES["file"], title=request.POST.title)
            video.save()
            return HttpResponseRedirect("/video/")
    else:
        form = UploadFileForm()

    return render(request, "video.html", {"form": form})
