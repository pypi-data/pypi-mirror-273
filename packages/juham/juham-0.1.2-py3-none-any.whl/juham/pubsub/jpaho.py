
from juham.base.jobject import JObject
from juham.base.jmqtt import JMqtt

import paho.mqtt.client as paho
import json
import os
import argparse

class JPaho(JMqtt):
    """! MQTT pub-sub implementation based on paho.mqtt Python package. 
    """
    JMqtt.host = '192.168.86.39'
    JMqtt.port = 1883
    configured = False
    paho_version = 1
    
    def __init__(self, name='paho'):
        super().__init__(name)
        if self.paho_version == 2:
            self.mqtt_client = paho.Client(paho.CallbackAPIVersion.VERSION1, name + str(os.getpid()))
        else:
            self.mqtt_client = paho.Client(name + str(os.getpid()))
    

    def connect(self):
        return self.mqtt_client.connect(self.host, self.port, 60)

    def subscribe(self, topic):
        self.mqtt_client.connected_flag = True
        self.mqtt_client.subscribe(topic)

    def publish(self, topic, msg, **kwargs):
        self.mqtt_client.publish(topic, msg, qos=1, retain=True)

    def on_message(self, mth):
        self.mqtt_client.on_message = mth

    def on_connect(self, mth):
        self.mqtt_client.on_connect = mth

    def on_disconnect(self, mth):
        self.mqtt_client.on_disconnect = mth

    def loop_start(self):
        self.mqtt_client.loop_start()

    def loop_forever(self):
        self.mqtt_client.loop_forever()

    @classmethod
    def register(cls):
        parser = argparse.ArgumentParser("kerttula")
        parser.add_argument("--paho_version", help="Version of Paho mqtt broker", type=int)
        args = parser.parse_args()
        cls.paho_version = args.paho_version
        JMqtt.register()
        if(cls.configured == False):
            JObject.registerClass(cls.get_class_id(), cls)
            cls.configure(cls.read_config(cls.__name__))
            cls.configured = True


