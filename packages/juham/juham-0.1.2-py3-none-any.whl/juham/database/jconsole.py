from juham.base.jobject import JObject
from juham.base.jdatabase import JDatabase

class JConsole(JDatabase):
    """! Database interface that simply dumps the written records
    to stdout solely for testing and debugging purposes
    """

    JDatabase.token = ''
    JDatabase.org = "Realsoft"
    JDatabase.host = "localhost"
    JDatabase.database="stdout"
    configured = False

    
    def __init__(self, name='jconsole'):
        super().__init__(name)

    
    def write(self, point):
        print(f"Table:{self.database}:  {str(point)}")
        

    @classmethod
    def register(cls):
        JDatabase.register()
        if(cls.configured == False):
            JObject.registerClass(cls.get_class_id(), cls)
            cls.configure(cls.read_config(cls.__name__))
            cls.configured =True


