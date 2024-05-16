from juham.base.jbase import JBase
from juham.shelly.jshelly import JShelly
from influxdb_client_3 import Point
import json


class JShellyMotion(JShelly):

    """! Shelly Motion 2 - a wifi motion sensor with light and temperature metering. 
    """
    
    classId = 'JShellyMotion'
    topic = 'shellies/shellymotion2/info'
    
    def __init__(self, name='shellymotion'):
        super().__init__(name)
        self.topic = JShellyMotion.topic

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.topic)
            self.info('Topic ' + self.topic + ' subscribed')
            
    def on_message(self, client, userdata, msg):
        m = json.loads(msg.payload.decode())
        self.on_sensor(m)


    def on_sensor(self, m):
        tmp = m['tmp']
        roomtemperature = tmp['value']
        sensor = m['sensor']
        vibration = sensor['vibration']
        motion = sensor['motion']
        timestamp = sensor['timestamp']
            
        point = (
            Point("motion") 
            .tag("sensor", 'motion')
            .field('motion', motion)
            .field('vibration', vibration)
            .field('roomtemp', roomtemperature)
            .field('timestamp', timestamp)
            .time(self.epoc2utc(timestamp))
        )
        self.write(point)
        self.info('Motion detected', str(m))

                
    
    @classmethod
    def register(cls):
        JShelly.register();
        JBase.registerClass(cls.classId, cls)
        
def main():
    JShellyMotion().run_forever()


if __name__ == "__main__":
    main()
    
