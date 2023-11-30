import platform
from datetime import datetime, timedelta

import pytz
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadFileForm
from .models import Video


def video(request):

    req = request.GET

    videos = Video.objects.all().order_by('-id')

    paginator = Paginator(videos, req.get('per_page', 25))

    page_number = request.GET.get('page', 1)

    page_obj = paginator.get_page(page_number)

    status = dict(Video.STATUS)

    videos_data = [{
        'id': video.id,
        'name': video.name or video.title,
        'description': video.description,
        'status': status.get(video.status),
        'privacy': video.privacy_status or '',
        'publish_at': video.publish_at,
        'view_count': video.view_count or '-',
        'file_base': video.file_base or '',
    } for video in page_obj.object_list]

    page_obj.object_list = videos_data

    ctx = {
        'computer_name': platform.node(),
        "videos": page_obj,
    }

    return render(request, "video/video.html", ctx)


def new_video(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            req = request.POST
            file = request.FILES["file"]

            last_date = Video.objects.order_by('publish_at').last().publish_at
            now = datetime.now(pytz.utc)
            if last_date < now:
                last_date = datetime.strptime('2023-12-01 19:00:00', '%Y-%m-%d %H:%M:%S')
                last_date = pytz.utc.localize(last_date)
            else:
                last_date += timedelta(days=1)

            video = Video(
                video=file,
                name=req.get('name'),
                title=req.get('title'),
                description=req.get('description'),
                keywords=req.get('keywords'),
                file_base=file.name,
                publish_at=last_date
            )
            video.save()
            return HttpResponseRedirect("/video/")
    else:
        form = UploadFileForm()

    class_options = [
        {'value': 'Archer', 'label': 'Arqueiro'},
        {'value': 'Berserker', 'label': 'Berserker'},
        {'value': 'Witch', 'label': 'Bruxa'},
        {'value': 'Dark Knight', 'label': 'Cavaleira das Trevas'},
        {'value': 'Ranger', 'label': 'Caçadora'},
        {'value': 'Corsair', 'label': 'Corsaria'},
        {'value': 'Tamer', 'label': 'Domadora'},
        {'value': 'Drakania', 'label': 'Drakania'},
        {'value': 'Sorceress', 'label': 'Feiticeira'},
        {'value': 'Guardian', 'label': 'Guardia'},
        {'value': 'Warrior', 'label': 'Guerreiro'},
        {'value': 'Hashashin', 'label': 'Hashashin'},
        {'value': 'Kunoichi', 'label': 'Kunoichi'},
        {'value': 'Lahn', 'label': 'Lahn'},
        {'value': 'Striker', 'label': 'Lutador'},
        {'value': 'Maehwa', 'label': 'Maehwa'},
        {'value': 'Wizard', 'label': 'Mago'},
        {'value': 'Maegu', 'label': 'Me-gu'},
        {'value': 'Mystic', 'label': 'Mistica'},
        {'value': 'Musa', 'label': 'Musa'},
        {'value': 'Ninja', 'label': 'Ninja'},
        {'value': 'Nova', 'label': 'Nova'},
        {'value': 'Sage', 'label': 'Sage'},
        {'value': 'Shai', 'label': 'Shai'},
        {'value': 'Valkyrie', 'label': 'Valquiria'},
        {'value': 'Woosa', 'label': 'Wu-sa'},
    ]

    ctx = {
        'computer_name': platform.node(),
        "form": form,
        "class_options": class_options,
    }

    return render(request, "video/new_video.html", ctx)
