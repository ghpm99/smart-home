import psutil

from django.shortcuts import render


# Create your views here.
def files(request):

    ctx = {
        'disk_partitions': [{
            'device': disk.device,
            'mountpoint': disk.mountpoint,
            'fstype': disk.fstype,
            'opts': disk.opts,
            'usage': psutil.disk_usage(disk.device)
        } for disk in psutil.disk_partitions()]
    }

    return render(request, 'home/home.html', ctx)
