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
        'disk_partitions': psutil.disk_partitions()
    }
    return render(request, 'home/home.html', ctx)
