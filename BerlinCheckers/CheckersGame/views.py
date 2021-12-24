from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from accounts.models import *
from django.contrib.auth import logout
import string
import random
import math, json
# Create your views here.

def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')
    
def create_game(request):
    user = User.objects.get(id = request.user.id)
    if user.is_authenticated:
        game = Game(
            game_creater = user.id,
            game_opponent = None,
            is_over = False,
            turn = True,
            red_score = 12,
            black_score = 12
        )
        game.save()
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5)) + 'r' + str(game.id)
        game.room_code = room_code
        game.save()
        for i in range(0,64,1):
            sq = BoardSquare(
                square_no = i,
                square_value = None,
                isKing = False,
                game = game
            )
            if i%2 == 1 and (math.floor(i/8) == 0 or math.floor(i/8) == 2):
                sq.square_value = math.floor(i/2)
            elif i%2 == 0 and math.floor(i/8) == 1:
                sq.square_value = math.floor(i/2)
            elif i%2 == 0 and (math.floor(i/8) == 5 or math.floor(i/8) == 7):
                sq.square_value = math.floor((i-16)/2)
            elif i%2 == 1 and math.floor(i/8) == 6:
                sq.square_value = math.floor((i-16)/2)
            sq.save()
        
        return redirect('/play/'+room_code+"?username="+user.username)
    else:
        return redirect('accounts/login/')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponse("Logged out successfully")


def play(request, room_code):
    if request.user is None:
        return redirect('/')
    user = User.objects.get(id = request.user.id)
    game = Game.objects.get(room_code = room_code)
    if game is None:
        return HttpResponse('Game does not exist')
    if game.game_creater != user.id:
        if game.game_opponent:
            print(game.game_creater)
            print(game.game_opponent)
            print(user.id)
            if game.game_opponent != user.id and game.game_creater != user.id:
                return HttpResponse("Game is not open to you")
        else:
            game.game_opponent = user.id
            game.save()
    if game.is_over:
        return HttpResponse("Game is over")
    print(game.game_opponent)
    print(game.game_creater)
    print(user.id)
    if game.game_creater == user.id:
        player = 'game_creator'
    else:
        player = 'game_opponent'
    print(player)
    game_squares = BoardSquare.objects.filter(game = game).order_by('square_no')
    #print(game_squares)
    square_list = []
    for i in game_squares:
        square_list.append(i.square_value)
    print(square_list)
    context = {
        'username' :user.username,
        'room_code' : room_code,
        'player' : player,
        'turn' : game.turn,
        'redScore' : game.red_score,
        'blackScore' : game.black_score,
        'board': game_squares,
        'game_squares' : json.dumps(square_list)
    }
    return render(request, 'CheckersGame/play.html', context)

def play_with_bot(request):
    user = User.objects.get(id = request.user.id)
    if user.is_authenticated:
        game = Game(
            game_creater = user.id,
            game_opponent = None,   #create dummy account for bot
            is_over = False,
            turn = True,
            red_score = 12,
            black_score = 12
        )
        game.save()
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5)) + 'r' + str(game.id)
        game.room_code = room_code
        game.save()
        for i in range(0,64,1):
            sq = BoardSquare(
                square_no = i,
                square_value = None,
                isKing = False,
                game = game
            )
            if i%2 == 1 and (math.floor(i/8) == 0 or math.floor(i/8) == 2):
                sq.square_value = math.floor(i/2)
            elif i%2 == 0 and math.floor(i/8) == 1:
                sq.square_value = math.floor(i/2)
            elif i%2 == 0 and (math.floor(i/8) == 5 or math.floor(i/8) == 7):
                sq.square_value = math.floor((i-16)/2)
            elif i%2 == 1 and math.floor(i/8) == 6:
                sq.square_value = math.floor((i-16)/2)
            sq.save()
        return redirect('/playbot/'+room_code+"?username="+user.username)
    else:
        redirect('/login/')

def playbot(request, room_code):
    user = User.objects.get(id = request.user.id)
    if user.is_authenticated:
        game = Game.objects.get(room_code = room_code)
        if game:
            if game.game_opponent == None and game.game_creater == user.id:
                game_squares = BoardSquare.objects.filter(game = game).order_by('square_no')
                square_list = []
                for i in game_squares:
                    square_list.append(i.square_value)
                context = {
                    'username' :user.username,
                    'room_code' : room_code,
                    'turn' : game.turn,
                    'redScore' : game.red_score,
                    'blackScore' : game.black_score,
                    'board': game_squares,
                    'game_squares' : json.dumps(square_list),
                    'game': game,
                    'user': user
                }
                return render(request, 'CheckersGame/playbot.html', context)
            else:
                return HttpResponse("game is not open to you")
        else:
            return HttpResponse("game is not available")
    else:
        redirect('/login/')

def join_game(request):
    if request.user is None:
        return redirect('/')
    room_code = request.GET['room_code']
    user = User.objects.get(id = request.user.id)
    return redirect('/play/' + room_code + '?username=' + user.username)

def indexPage(request):
    context = {

    }
    return render(request,'CheckersGame/index.html',context)


def ProfilePage(request):
    if request.user.is_authenticated:
        return render(request,'CheckersGame/createprofile.html')
    else:
        return redirect('/login/')