
from juham.base.jbase import JBase
import json


class JShelly(JBase):
    """! Base class for shelly product family. 
    """
    
    def __init__(self, name):
        super().__init__(name)
        self.relay_started = 0


    def elapsed(self, secs):
        tsnow = self.timestamp()
        if tsnow - self.relay_started < secs:
            return False
        self.relay_started = tsnow;
        return True

    
    
    @classmethod
    def register(cls):
        JBase.register();

        
