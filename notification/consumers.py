import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from notification.utils import get_instances_data


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.user_notification_name = "notification_%s" % self.user_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.user_notification_name, self.channel_name
        )

        self.accept()

        # -----------------------------
        # Get data for specific instances
        instances_data = get_instances_data()  # Example function to get instances data
        instances_data_json = json.dumps(instances_data)
        print(instances_data_json)
        # Send data to WebSocket
        self.send(text_data=instances_data_json)
        # -----------------------------

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.user_notification_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.user_notification_name,
            {"type": "notification_message", "message": message},
        )

    # Receive message from room group
    def notification_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
