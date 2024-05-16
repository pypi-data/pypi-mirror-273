from juham.base.jbase import JBase
from juham.shelly.jshelly import JShelly
from influxdb_client_3 import Point
import json


class JShellyPro3EM(JShelly):

    classId = 'JShellyPro3EM'
    topic = 'shellypro3em-powermeter/events/rpc'

    
    def __init__(self, name='rshellypro3em'):
        super().__init__(name)

        
    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(JShellyPro3EM.topic)

            
    def on_message(self, client, userdata, msg):
        super().on_message(client, userdata, msg)
        m = json.loads(msg.payload.decode())
        mth = m['method']
        if mth == 'NotifyStatus':
            params = m['params']
            ts = params['ts']
            if 'em:0' in params:
                self.on_em_0(ts, params['em:0'])
            elif 'emdata:0' in params:
                self.on_emdata_0(ts, params['emdata:0'])
            else:
                self.error('Unknown powermeter id', str(m))
        elif mth == 'NotifyEvent':
            self.warning('NotifyEvent not implemented yet', str(m))
        else:
            self.error('UNKNOWN POWERMETER METHOD {mth}', str(m))

            
    def on_em_0(self, ts, em):
        point = (
            Point("powermeter") 
            .tag("sensor", 'em0')
            .field('real_A', em['a_act_power'])
            .field('real_B', em['b_act_power'])
            .field('real_C', em['c_act_power'])
            .field('total_real_power', em['total_act_power'])
            .field('total_apparent_power', em['total_aprt_power'])
            .field('apparent_a', em['a_aprt_power'])
            .field('apparent_b', em['b_aprt_power'])
            .field('apparent_c', em['c_aprt_power'])
            .field('current_a', em['a_current'])
            .field('current_b', em['b_current'])
            .field('current_c', em['c_current'])
            .field('current_n', em['n_current'])
            .field('current_total', em['total_current'])
            .field('voltage_a', em['a_voltage'])
            .field('voltage_b', em['b_voltage'])
            .field('voltage_c', em['c_voltage'])
            .field('freq_a', em['a_freq'])
            .field('freq_b', em['b_freq'])
            .field('freq_c', em['c_freq'])
            .time(self.epoc2utc(ts))
        )
        self.write(point)
        self.info('Power meter written', str(point))


    def on_emdata_0(self, ts, em):
        point = (
            Point("powermeter") 
            .tag("sensor", 'emdata0')
            .field('total_act_energy_A', em['a_total_act_energy'])
            .field('total_act_energy_B', em['b_total_act_energy'])
            .field('total_act_energy_C', em['c_total_act_energy'])
            .field('total_act_ret_energy_A', em['a_total_act_ret_energy'])
            .field('total_act_ret_energy_B', em['b_total_act_ret_energy'])
            .field('total_act_ret_energy_C', em['c_total_act_ret_energy'])
            .field('total_act', em['total_act'])
            .field('total_act_ret', em['total_act_ret'])
            .time(self.epoc2utc(ts))
        )
        self.write(point)
        self.info('Total energy consumed ' + str(em['total_act']) + ' exported ' + str(em['total_act_ret']))


    @classmethod
    def register(cls):
        JShelly.register()
        JBase.registerClass(cls.classId, cls)


        
def main():
    JShellyPro3EM().run_forever()


if __name__ == "__main__":
    main()
    

