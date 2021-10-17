from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import *



class GameRoom(WebsocketConsumer):
    
    # connect to a paticular game on the server
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()

    # disconnect from the paticular game on the server 
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

    # receive data from frontend    
    def receive(self , text_data):
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
            self.close()
            
                
        
        
    # sends data back to frontend
    def run_game(self , event):
        data = event['payload']
        data = json.loads(data)
        self.send(text_data = json.dumps({
            'payload' : data['data']
        }))        