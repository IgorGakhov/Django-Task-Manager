from django.http import HttpResponse


def index(request):
    return HttpResponse('<h1>Welcome to future Task Manager!</h1>')
