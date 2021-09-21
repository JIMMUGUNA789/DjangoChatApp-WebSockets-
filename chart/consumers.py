from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
    #Building a connection 
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        #get group name for users in same chatroom
        self.room_group_name = 'chat_%s'%self.room_name
        #create a group
        await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name,
        )
        await self.accept()

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type':'tester_message',
        #         'tester':'Hello world'
        #     }
        # )
    # async def tester_message(self, event):
    #         tester = event['tester']
    #         await self.send(text_data = json.dumps({
    #             'tester':tester,
    #         }))
    
    


     #disconnect
    async def disconnect(self, close_code):
         await self.channel_layer.group_discard(
             self.room_group_name,
             self.channel_name
         )
         #receive
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': message,
                'username': username,
            }
        )
    async def chat_message(self, event):
        message = event['message']
        username = event['username']


        await self.send(text_data=json.dumps({
            'message': message, 
            'username': username,
        }))
    pass