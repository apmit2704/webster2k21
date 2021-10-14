from django.shortcuts import render
from .models import *
# Create your views here.

def register(request):
    pass
def login(request):
    pass

def home(request):
    return render(request, 'templates/profile.html')

def play(request, room_code):
    return render(request, 'templates/play.html')