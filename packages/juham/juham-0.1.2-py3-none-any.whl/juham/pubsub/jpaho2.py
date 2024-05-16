
from juham.base.jobject import JObject
from juham.base.jmqtt import JMqtt

import paho.mqtt.client as paho
import json
import os
import argparse
import pdb

class JPaho2(paho.Client, JMqtt):
    host = '192.168.86.39'
    port = 1883
    configured = False
    paho_version = 1
    
    def __init__(self, name='paho'):
        pdb.set_trace()
        if self.paho_version == 2:
            super().__init__(paho.CallbackAPIVersion.VERSION1, name + str(os.getpid()))
        else:
            super().__init__(name + str(os.getpid()))
            
    def connect(self):
        return super().connect(self.host, self.port, 60)
        
    def on_message(self, mth):
        self.on_message = mth

    def on_connect(self, mth):
        self.on_connect = mth

    def on_disconnect(self, mth):
        self.on_disconnect = mth

    def configure(cls):
        pass

    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser("kerttula")
        parser.add_argument("--paho_version", help="Version of Paho mqtt broker", type=int)
        args = parser.parse_args()
        cls.paho_version = args.paho_version

        
    @classmethod
    def register(cls):
        cls.parse_args()
        JMqtt.register()
        if(cls.configured == False):
            JObject.registerClass(cls.get_class_id(), cls)
            cls.configure(cls.read_config(cls.__name__))
            cls.configured = True


