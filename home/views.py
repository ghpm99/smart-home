import platform
import psutil

from django.shortcuts import render

from home.models import Disk


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
