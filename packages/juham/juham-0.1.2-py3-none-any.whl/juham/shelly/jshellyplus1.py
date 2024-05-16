
from juham.base.jbase import JBase
from juham.shelly.jshelly import JShelly
from influxdb_client_3 import Point
import json


class JShellyPlus1(JShelly):
    """! Interface to Shelly Plus 1 smart relay via MQTT with Shelly Plus Add-on 
    sensor module supporting up to five DS18B20 temperature sensors.
    TODO:  supports one moisture sensor
    """

    classId = 'JShellyPlus1'
    shelly_topic = "/events/rpc"
    temperature_topic = 'kukkila/temperature/'

    
    def __init__(self, name='shellyplus1-a0a3b3c309c4'):
        super().__init__(name)
        self.relay_started = 0
        
        
    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.name + self.shelly_topic)

        
    def on_message(self, client, userdata, msg):
        # optimize out excessive notifications
        tsnow = self.timestamp()
        if tsnow - self.relay_started < 60:
            return 0
        self.relay_started = tsnow;

        m = json.loads(msg.payload.decode())
        mth = m['method']
        if mth == 'NotifyStatus':
            params = m['params']
            self.on_sensor(params)
        else:
            self.warning('Unknown method ' + mth, str(m))

            
    def on_sensor(self, params):
        ts = params['ts']
        for key, value in params.items():
            if key.startswith("temperature:"):
                sensor_id = key.split(":")[1]
                temperature_reading = value
                temperature_id = temperature_reading['id']
                temperature_celsius = temperature_reading['tC']

                msg = {
                    'sensor' : sensor_id,
                    'timestamp' : ts,
                    'temperature' : temperature_celsius
                }
                self.mqtt_client.publish(self.temperature_topic + sensor_id, json.dumps(msg), 1, True)
                self.info(f"Temperature reading { self.temperature_topic + sensor_id} published")
                
                point = (
                    Point("boiler") 
                    .tag("sensor", sensor_id)
                    .field('s'+sensor_id, temperature_celsius)
                    .time(self.epoc2utc(ts))
                )
                self.write(point)
                self.info(f"Temperature { str(sensor_id)}  { str(temperature_celsius)} recorded", '')

    
    @classmethod
    def register(cls):
        JShelly.register();
        JBase.registerClass(cls.classId, cls)



def main():
    JShellyPlus1().run_forever()


if __name__ == "__main__":
    main()
    
