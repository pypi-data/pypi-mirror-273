from juham.base.jobject import JObject
from juham.base.jdatabase import JDatabase
from influxdb_client_3 import InfluxDBClient3, Point

class JInflux(JDatabase):
    """! Database interface to Influx time series database version 3. 
    """

    JDatabase.token = 'uVsAcRgNhirRTseooX3Hn4BioA8Ecpj5aLERiQSM_M0C7y2T9Z8nsc-nv3_2pjSyFulXL3OwOJhfwziFUw3HWQ=='
    JDatabase.org = "Real3D"
    JDatabase.host = "https://eu-central-1-1.aws.cloud2.influxdata.com"
    JDatabase.database="spot"
    configured = False

    
    def __init__(self, name='influx'):
        super().__init__(name)
        self.influx_client = InfluxDBClient3(host=self.host, token=self.token, org=self.org)

        
    def write(self, point):
        self.influx_client.write(database=self.database, record=point)

      
    @classmethod
    def register(cls):
        JDatabase.register()
        if(cls.configured == False):
            JObject.registerClass(cls.get_class_id(), cls)
            cls.configure(cls.read_config(cls.__name__))
            cls.configured =True


