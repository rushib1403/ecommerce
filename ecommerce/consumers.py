#same like views
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import * 
from rest_framework import serializers
class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name=self.scope["url_route"]['kwargs']['order_id']
        print(self.room_name)
        self.room_group_name="order_%s" % self.room_name
        print(self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(
            
            self.room_group_name,
            self.channel_name,
        )
        #order=Order.objects.all().first()
        #order=order.status
        self.accept()
        

        #self.send(text_data=json.dumps({'dataname':order}))

    def receive(self,text_data):
        async_to_sync(self.channel_layer.group_send)(
            
            self.room_group_name,
            {
                'type':'order_status',
                'payload':text_data
            }
        )
    def disconnect(self):
        pass
    def send_notification(self, event):
        print('send notification')
        print(event)
    def order_status(self,event):
        print(event)
        order=json.loads(event['value'])
        self.send(text_data=json.dumps({'dataname':order}))

