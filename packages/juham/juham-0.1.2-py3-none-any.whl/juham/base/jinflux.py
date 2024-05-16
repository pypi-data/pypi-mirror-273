
from juham.base.jobject import JObject

class JInflux(JObject):
    token = 'uVsAcRgNhirRTseooX3Hn4BioA8Ecpj5aLERiQSM_M0C7y2T9Z8nsc-nv3_2pjSyFulXL3OwOJhfwziFUw3HWQ=='
    org = "Real3D"
    host = "https://eu-central-1-1.aws.cloud2.influxdata.com"
    database="spot"
    configured = False


    
    def __init__(self, name):
        super().__init__(name)


    @classmethod
    def configure(self, conf):
        if conf != None:
            if 'organization' in conf:
                cls.organization = conf['organization']
            if 'hostname' in conf:
                cls.hostname = conf['hostname']
            if 'database' in conf:
                cls.database = conf['database']
            if 'token' in conf:
                cls.token = conf['token']

    @classmethod
    def register(cls):
        JObject.register()
        if(cls.configured == False):
            cls.configure(cls.read_config(cls.__name__))
            cls.configured =True


