from django.shortcuts import render
import platform


# Create your views here.
def home(request):
    ctx = {
        'computer_name': platform.node()
    }
    return render(request, 'home.html', ctx)
