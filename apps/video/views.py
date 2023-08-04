from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import Video


def video(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            req = request.POST
            file = request.FILES["file"]
            video = Video(
                video=file,
                title=req.get('title'),
                description=req.get('description'),
                file_base=file.name
            )
            video.save()
            return HttpResponseRedirect("/video/")
    else:
        form = UploadFileForm()

    videos = Video.objects.all().order_by('-id')

    status = dict(Video.STATUS)

    videos_data = [{
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'status': status.get(video.status),
        'file_name': video.file_name or '',
        'youtube_id': video.youtube_id or '',
        'file_base': video.file_base or '',
    } for video in videos]

    ctx = {
        "form": form,
        "videos": videos_data,
    }

    return render(request, "video.html", ctx)
