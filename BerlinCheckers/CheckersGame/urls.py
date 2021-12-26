from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', home,name="home"),
    path('play/<str:room_code>', play),
    path('play/', join_game),
    path('playbot/<str:room_code>', playbot, name="playbot"),
    path('playbot/', play_with_bot, name="playwithbot"),
    path('creategame/', create_game),
    path('logout/', logout_view),
    path('index/',views.indexPage,name="index"),
    path('profile/',views.ProfilePage,name="profile"),
    path('send_friend_request/<int:userID>/',send_request,name='send_friend_request'),
    path('accept_friend_request/<int:requestID>/',accept_request,name='accept_friend_request'),
]