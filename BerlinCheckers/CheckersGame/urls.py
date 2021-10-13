from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('play/<int:room_code>', play)
]