from channels.generic.websocket import AsyncWebsocketConsumer
from user_guide.models import CustomUser, Room, Message
import base64
import json
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']  # Получаем название комнаты
        self.roomGroupName = f'chat_{self.room_name}'  # Инициализируем имя группы

        # Добавляем канал в группу, которая будет обрабатывать сообщения для этой комнаты
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
        file_data = text_data_json.get("file", None)

        if file_data:
            file_name = file_data["name"]
            file_content = base64.b64decode(file_data["content"])
            file = ContentFile(file_content, name=file_name)
            file_path = default_storage.save(f'chat_files/{file_name}', file)
            created_message = await self.save_message(message, username, room_name, file_path)
            user = await database_sync_to_async(CustomUser.objects.get)(username=username)
            fio = user.fio
            photo = user.photo.url
            created = created_message.created.strftime("%Y.%m.%d %H:%M:%S")
            await self.channel_layer.group_send(
                self.roomGroupName, {
                    "type": "sendMessage",
                    "message": message,
                    "fio": fio,
                    "photo": photo,
                    "created": created,
                    "room_name": room_name,
                    "file": file_path,  # Путь к файлу
                }
            )

        else:
            # Если файла нет, отправляем просто сообщение
            created_message = await self.save_message(message, username, room_name)

            user = await database_sync_to_async(CustomUser.objects.get)(username=username)
            fio = user.fio
            photo = user.photo.url
            created = created_message.created.strftime("%Y.%m.%d %H:%M:%S")

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
        room_name = event["room_name"]
        file = event.get("file", None)

        # Отправляем сообщение обратно в WebSocket клиент
        await self.send(text_data=json.dumps({
            "message": message,
            "fio": fio,
            "photo": photo,
            "created": created,
            "room_name": room_name,
            "file": file,  # Добавляем путь к файлу
        }))

    @database_sync_to_async
    def save_message(self, message, username, room_name, file_path=None):
        user = CustomUser.objects.get(username=username)
        room = Room.objects.get(name=room_name)

        # Сохраняем сообщение с файлом (если он есть)
        return Message.objects.create(user=user, room=room, content=message, file=file_path)

