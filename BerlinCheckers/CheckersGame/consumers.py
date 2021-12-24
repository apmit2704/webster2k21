from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import *
from .minimax.algorithm import *


class GameRoom(WebsocketConsumer):
    # connect to a paticular game on the server
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name
        print(self.scope['user'])
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        game = Game.objects.get(room_code = self.room_name)
        if game:
            if game.game_opponent:
                text_data = '{"data":{"type":"load"}}'
            else:
                text_data = '{"data" : {"type" : "wait"}}'
            async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,{
                        'type' : 'run_game',
                        'payload' : text_data
                    }
                )
            self.accept()

    # disconnect from the paticular game on the server 
    def disconnect(self, close_code):
        print("in disconnect")
        # gameRoomId = self.room_group_name[5:]
        # game = Game.objects.get(room_code = gameRoomId)
        # if game:
        #     if game.is_over == False:
        #         print("saving game results")
        #         game.won = 'T'
        #         game.is_over = True
        #         game.save()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # receive data from frontend    
    def receive(self , text_data):
        print(text_data)
        data_received = json.loads(text_data)
        if data_received['data']['type'] == 'move':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,{
                    'type' : 'run_game',
                    'payload' : text_data
                }
            )
        elif data_received['data']['type'] == 'endgame':
            gameRoomId = self.room_group_name[5:]
            print(gameRoomId)
            game = Game.objects.get(room_code = gameRoomId)
            if game:
                if data_received['data']['result'] == 'R':
                    game.won = 'R'
                elif data_received['data']['result'] == 'B':
                    game.won = 'B'
                elif data_received['data']['result'] == 'D':
                    game.won = 'D'
                game.is_over = True
                game.save()
                async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,{
                    'type' : 'run_game',
                    'payload' : text_data
                }
            )
            self.close()
        elif data_received['data']['type'] == 'state':
            gameRoomId = self.room_group_name[5:]
            print(gameRoomId)
            game = Game.objects.get(room_code = gameRoomId)
            game.turn = data_received['data']['turn'] 
            game.red_score = data_received['data']['redScore']
            game.black_score = data_received['data']['blackScore']
            gameSquares = BoardSquare.objects.filter(game = game)
            for square in gameSquares:
                square.square_value = data_received['data']['board'][square.square_no]
                square.save()
            game.save()
            #save board, turn, redscore, blackscore

    # sends data back to frontend
    def run_game(self , event):
        data = event['payload']
        data = json.loads(data)
        self.send(text_data = json.dumps({
            'payload' : data['data']
        }))    

class GameBotRoom(WebsocketConsumer):    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name
        # print(self.scope['user'])
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        game = Game.objects.get(room_code = self.room_name)
        if game:
            # async_to_sync(self.channel_layer.group_send)(
            #         self.room_group_name,{
            #             'type' : 'run_game',
            #             'payload' : text_data
            #         }
            #     )
            self.accept()

    def disconnect(self, close_code):
        print("in disconnect")
        gameRoomId = self.room_group_name[5:]
        game = Game.objects.get(room_code = gameRoomId)
        if game:
            if game.is_over == False:
                print("saving game results")
                game.won = 'T'
                game.is_over = True
                game.save()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        if data['data']['type'] == 'move':
            gameRoomId = self.room_group_name[5:]
            print(gameRoomId)
            game = Game.objects.get(room_code = gameRoomId)
            game.turn = data['data']['turn'] 
            game.red_score = data['data']['redScore']
            game.black_score = data['data']['blackScore']
            gameSquares = BoardSquare.objects.filter(game = game)
            board = []
            for square in gameSquares:
                square.square_value = data['data']['board'][square.square_no]
                square.save()
                board.append(square)
            game.save()   
            if game.red_score == 0:
                    game.is_over = True
                    game.won = game.game_opponent
            elif game.black_score == 0:
                game.is_over = True
                game.won = game.game_creater
            game.save()
            if game.is_over != True:
                board = minimax(board, 5, True)[0]
                for square in gameSquares:
                    square = board[square.square_no]
                    square.save()
                game.turn = True
                game.red_score = calc_score(board, 1)
                game.black_score = calc_score(board, 0)
                if game.red_score == 0:
                    game.is_over = True
                    game.won = game.game_opponent
                elif game.black_score == 0:
                    game.is_over = True
                    game.won = game.game_creater
                game.save()
                context = {
                    'type': 'botMove',
                    'game_squares': board,
                    'game': game
                }
                text_data = json.dumps(context)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,{
                        'type' : 'run_game',
                        'payload' : text_data
                    }
                )
            #call minimax here and send new board state back to frontend

    def run_game(self, event):
        data = event['payload']
        data = json.loads(data)
        self.send(text_data = json.dumps({
            'payload' : data['data']
        })) 
    
    