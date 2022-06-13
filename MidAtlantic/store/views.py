from django.shortcuts import render
from .models import Game

def index(request):
    return render(request, 'template.html')

def store(request):
    count = Game.objects.all().count()
    context = {
        'count': count,
    }
    return render(request, 'store.html', context)