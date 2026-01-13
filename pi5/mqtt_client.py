# mqtt_client.py
import paho.mqtt.client as mqtt
import json

class MqttClient:
    def __init__(self, broker_ip='192.168.4.1', broker_port=1883, topics=[]):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.topics = topics
        self.data = {}

    def on_connect(self, client, userdata, flags, rc):
        print("Connecté MQTT avec code", rc)
        for topic in self.topics:
            client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        try:
            self.data[msg.topic] = json.loads(msg.payload.decode())
        except:
            pass

    def start(self):
        self.client.connect(self.broker_ip, self.broker_port, 60)
        self.client.loop_start()
