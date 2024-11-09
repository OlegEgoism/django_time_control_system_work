import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from user_guide.models import CustomUser, Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.roomGroupName = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room_name = text_data_json["room_name"]

        created_message = await self.save_message(message, username, room_name)

        user = await sync_to_async(CustomUser.objects.get)(username=username)
        fio = user.fio
        photo = user.photo.url
        created = created_message.created.strftime("%Y-%m-%d %H:%M:%S")

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "fio": fio,
                "photo": photo,
                "created": created,
                "room_name": room_name,
            }
        )

    async def sendMessage(self, event):
        message = event["message"]
        fio = event["fio"]
        photo = event["photo"]
        created = event["created"]

        await self.send(text_data=json.dumps({
            "message": message,
            "fio": fio,
            "photo": photo,
            "created": created
        }))

    @sync_to_async
    def save_message(self, message, username, room_name):
        user = CustomUser.objects.get(username=username)
        room = Room.objects.get(name=room_name)
        return Message.objects.create(user=user, room=room, content=message)
