from datetime import datetime
import platform
from django.http import HttpResponseRedirect
import psutil

from django.shortcuts import render
from django.core.paginator import Paginator
import pytz

from home.forms import ApontamentoForm
from home.models import Apontamento, Disk, File


# Create your views here.
def home(request):

    video_list = File.objects.filter(format__in=['mp4', 'avi']).order_by('path')[0:5]

    ctx = {
        'computer_name': platform.node(),
        'total_video_files': video_list.count(),
        'video_list': [{
            'name': video.name,
            'path': f"{video.path}/{video.name}",
            'size': video.size,
            'updated_at': video.updated_at,
            'created_at': video.created_at
        } for video in video_list]
    }
    return render(request, 'home/home.html', ctx)


def files(request):

    files_count = File.objects.count()

    disk_list = Disk.objects.all()

    ctx = {
        'computer_name': platform.node(),
        'files_count': files_count,
        'disk_list': [{
            'name': disk.name,
            'mountpoint': disk.mountpoint
        } for disk in disk_list]
    }

    return render(request, 'media/files.html', ctx)


def documents(request):

    ctx = {
        'computer_name': platform.node(),
    }

    return render(request, 'media/documents.html', ctx)


def images(request):

    req = request.GET

    images_files = File.objects.filter(format__in=['jpg', 'png']).order_by('path')

    paginator = Paginator(images_files, req.get("per_page", 25))

    page_number = request.GET.get("page", 1)

    page_obj = paginator.get_page(page_number)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_obj.number)

    images_files_count = images_files.count()

    images_data = [
        {
            'name': image.name,
            'path': image.path,
            'size': image.size,
            'updated_at': image.updated_at,
            'created_at': image.created_at
        } for image in page_obj.object_list
    ]

    page_obj.object_list = images_data

    ctx = {
        'computer_name': platform.node(),
        'total_images_files': images_files_count,
        'images': page_obj
    }

    return render(request, 'media/images.html', ctx)


def video(request):

    ctx = {
        'computer_name': platform.node(),
    }

    return render(request, 'media/video.html', ctx)


def apontamento(request):
    req = request.GET

    apontamento_list = Apontamento.objects.all().order_by("-id")

    paginator = Paginator(apontamento_list, req.get("per_page", 25))

    page_number = request.GET.get("page", 1)

    page_obj = paginator.get_page(page_number)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_obj.number)

    apontamento_data = [
        {
            "id": apontamento.id,
            "name": apontamento.name,
            "observation": apontamento.observation,
            "created_at": apontamento.created_at
        }
        for apontamento in page_obj.object_list
    ]

    page_obj.object_list = apontamento_data

    ctx = {
        "computer_name": platform.node(),
        "apontamentos": page_obj,
    }

    return render(request, 'apontamento/apontamento.html', ctx)

def new_apontamento(request):
    if request.method == "POST":
        form = ApontamentoForm(request.POST, request.FILES)
        if form.is_valid():
            req = request.POST

            name = req.get("name")
            observation = req.get("observation")
            created_at = datetime.now(pytz.utc)

            apontamento = Apontamento(
                name=name,
                observation=observation,
                created_at=created_at
            )

            apontamento.save()
            return HttpResponseRedirect("/apontamento-hora/")
    else:
        form = ApontamentoForm()


    ctx = {
        "computer_name": platform.node(),
        "form": form,
    }

    return render(request, 'apontamento/new_apontamento.html', ctx)