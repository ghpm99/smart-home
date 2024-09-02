import platform
import psutil

from django.shortcuts import render


# Create your views here.
def home(request):

    ctx = {
        'computer_name': platform.node(),
        'cpu_times': psutil.cpu_times(),
        'cpu_percent': psutil.cpu_percent(),
        'cpu_status': psutil.cpu_stats(),
        'virtual_memory': psutil.virtual_memory(),
        'disk_partitions': [{
            'device': disk.device,
            'mountpoint': disk.mountpoint,
            'fstype': disk.fstype,
            'opts': disk.opts,
            'usage': psutil.disk_usage(disk.device)
        } for disk in psutil.disk_partitions()]
    }
    cpu_free = 100 - ctx['cpu_percent']
    ctx['cpu_free'] = cpu_free
    return render(request, 'home/home.html', ctx)
