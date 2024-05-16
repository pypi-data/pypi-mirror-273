
from juham.base.jobject import JObject

class JMqtt(JObject):
    host = '192.168.86.39'
    port = 1883
    configured = False
    
    def __init__(self, name):
        super().__init__(name)

    
    @classmethod
    def configure(self, conf):
        if conf != None:
            if 'host' in conf:
                self.host = conf['host']
            if 'port' in conf:
                self.port = conf['port']

    @classmethod
    def register(cls):
        JObject.register()
        if(cls.configured == False):
            cls.configure(cls.read_config(cls.__name__))
            cls.configured = True


