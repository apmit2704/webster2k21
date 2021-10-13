from django.shortcuts import render
from .models import *
# Create your views here.

def home(request):
    return render(request, 'templates/homepage.html')

def play(request, room_code):
    return render(request, 'templates/play.html')