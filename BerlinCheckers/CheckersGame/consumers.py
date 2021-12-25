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

    # calculate and update ratings
    def calculate_rating_changes():
        game = Game.objects.get(room_code = self.room_name)
        k = 32
        game_creater_rating = game.game_creater
        game_opponent_rating = game.game_opponent
        
        expected_creater_score = 1/(1+ pow(10, (game_opponent_rating - game_creater_rating)/400))
        creator_score = 1
        
        expected_opponent_score = 1/(1+ pow(10, (game_creater_rating - game_opponent_rating)/400))
        opponent_score = 0
    
        game.creater_rating_change = game_creater_rating + k*(creator_score - expected_creater_score)
        game.opponent_rating_change = game_opponent_rating + k*(opponent_score - expected_opponent_score)
      
        game.save()



         

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

    def receive(self, text_data):
        data = json.loads(text_data)
        if data['data']['type'] == 'state':
            gameRoomId = self.room_group_name[5:]
            print(gameRoomId)
            game = Game.objects.get(room_code = gameRoomId)
            game.turn = data['data']['turn'] 
            game.red_score = data['data']['redScore']
            game.black_score = data['data']['blackScore']
            gameSquares = BoardSquare.objects.filter(game = game).order_by('square_no')
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
                board = minimax(board, 1, True)[1]
                for square in gameSquares:
                    square.square_value = board[square.square_no].square_value
                    square.isKing = board[square.square_no].isKing
                    square.save()
                list = []
                for square in board:
                    list.append(square.square_value)
                print(list)
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
                game_square_value_list = []
                game_isKing_list = []
                board = BoardSquare.objects.filter(game = game).order_by('square_no')
                for square in board:
                    game_square_value_list.append(square.square_value)
                    game_isKing_list.append(square.isKing)
                print(game_square_value_list)
                context = {
                    'type': 'botMove',
                    'game_squares_value': game_square_value_list,
                    'game_isKing': game_isKing_list,
                    'turn': game.turn,
                    'redScore': game.red_score,
                    'blackScore': game.black_score,
                    'is_over': game.is_over 
                }
                text_data = json.dumps({'data' : context})
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
    
    
