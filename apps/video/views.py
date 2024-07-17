import platform
from datetime import datetime, timedelta

import pytz
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q

from .forms import UploadFileForm
from .models import Video


def video(request):
    req = request.GET

    videos = Video.objects.all().order_by("-id")

    paginator = Paginator(videos, req.get("per_page", 25))

    page_number = request.GET.get("page", 1)

    page_obj = paginator.get_page(page_number)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_obj.number)

    status = dict(Video.STATUS)

    types = dict(Video.TYPES)

    videos_data = [
        {
            "id": video.id,
            "name": video.name or video.title,
            "description": video.description,
            "status": status.get(video.status),
            "type": types.get(video.type),
            "privacy": video.privacy_status or "",
            "publish_at": video.publish_at,
            "view_count": video.view_count or "-",
            "file_base": video.file_base or "",
        }
        for video in page_obj.object_list
    ]

    page_obj.object_list = videos_data

    ctx = {
        "computer_name": platform.node(),
        "videos": page_obj,
    }

    return render(request, "video/video.html", ctx)


def new_video(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            req = request.POST
            files = form.cleaned_data["file"]
            type = int(req.get("type") or 0)
            name = req.get("name")
            title = req.get("title")

            if type is Video.T_SOLARE_RANKED or type is Video.T_SOLARE_PRACTICE:
                last_date = (
                    Video.objects.filter(
                        Q(type=Video.T_SOLARE_RANKED) | Q(type=Video.T_SOLARE_PRACTICE)
                    )
                    .order_by("publish_at")
                    .last()
                    .publish_at
                )

                now = datetime.now(pytz.utc)
                if last_date < now:
                    last_date = now.replace(hour=19, minute=0, second=0) + timedelta(
                        days=2
                    )
                else:
                    last_date += timedelta(days=1)
            else:
                last_date = None

            for file in files:
                if type is Video.T_BACKUP:
                    name = f"Backup {file.name}"
                    title = file.name

                video = Video(
                    video=file,
                    name=name,
                    title=title,
                    description=req.get("description"),
                    keywords=req.get("keywords"),
                    file_base=file.name,
                    type=type,
                    publish_at=last_date,
                )

                video.save()
            return HttpResponseRedirect("/video/")
    else:
        form = UploadFileForm()

    class_options = [
        {"value": "Archer", "label": "Arqueiro"},
        {"value": "Berserker", "label": "Berserker"},
        {"value": "Witch", "label": "Bruxa"},
        {"value": "Dark Knight", "label": "Cavaleira das Trevas"},
        {"value": "Ranger", "label": "Caçadora"},
        {"value": "Corsair", "label": "Corsaria"},
        {"value": "Tamer", "label": "Domadora"},
        {"value": "Drakania", "label": "Drakania"},
        {"value": "Sorceress", "label": "Feiticeira"},
        {"value": "Guardian", "label": "Guardia"},
        {"value": "Warrior", "label": "Guerreiro"},
        {"value": "Hashashin", "label": "Hashashin"},
        {"value": "Kunoichi", "label": "Kunoichi"},
        {"value": "Lahn", "label": "Lahn"},
        {"value": "Striker", "label": "Lutador"},
        {"value": "Maehwa", "label": "Maehwa"},
        {"value": "Wizard", "label": "Mago"},
        {"value": "Maegu", "label": "Me-gu"},
        {"value": "Mystic", "label": "Mistica"},
        {"value": "Musa", "label": "Musa"},
        {"value": "Ninja", "label": "Ninja"},
        {"value": "Nova", "label": "Nova"},
        {"value": "Sage", "label": "Sage"},
        {"value": "Shai", "label": "Shai"},
        {"value": "Valkyrie", "label": "Valquiria"},
        {"value": "Woosa", "label": "Wu-sa"},
        {"value": "Scholar", "label": "Erudita"},
    ]

    video_types_options = [
        {"value": video_type[0], "label": video_type[1]} for video_type in Video.TYPES
    ]

    ctx = {
        "computer_name": platform.node(),
        "form": form,
        "class_options": class_options,
        "types_options": video_types_options,
    }

    return render(request, "video/new_video.html", ctx)
