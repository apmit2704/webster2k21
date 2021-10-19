from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('play/<str:room_code>', play),
    path('play/', join_game),
    path('creategame/', create_game),
    path('logout/', logout_view),
    path('index/',views.indexPage,name="index"),
]