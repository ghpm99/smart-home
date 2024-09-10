import platform
import psutil

from django.shortcuts import render
from django.core.paginator import Paginator

from home.models import Disk, File


# Create your views here.
def home(request):

    disk_list = Disk.objects.all()

    ctx = {
        'computer_name': platform.node(),
        'cpu_times': psutil.cpu_times(),
        'cpu_percent': psutil.cpu_percent(),
        'cpu_status': psutil.cpu_stats(),
        'virtual_memory': psutil.virtual_memory(),
        'disk_partitions': [{
            'device': disk.name,
            'mountpoint': disk.mountpoint,
            'fstype': disk.fstype,
            'opts': disk.opts,
            'usage': psutil.disk_usage(disk.name)
        } for disk in disk_list]
    }
    cpu_free = 100 - ctx['cpu_percent']
    ctx['cpu_free'] = cpu_free
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
