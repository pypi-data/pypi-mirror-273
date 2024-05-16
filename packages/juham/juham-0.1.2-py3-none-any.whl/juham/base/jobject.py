
"""@package jobject
Module implementing the base class for everything


"""

import os
import json
import logging

class JObject():
    """Base class of everything. 
    Implements a named object supporting factory method parttern, logging, configuration, and 
    other common features needed to implement any software masterpiece.
    """
    
    log = None
    factory = {}

    @classmethod
    def is_abstract(cls):
        return False

  
    @classmethod
    def logger(cls, l):
        cls.log = l

    @classmethod
    def get_class_id(cls):
        return cls.__name__

    
    def __init_subclass__(cls, **kwargs):
        """Called when new sub-class is created."""
        super().__init_subclass__(**kwargs)
        cls.register()



    def __init__(self, name):
        self.name = name
        if self.log == None:
            self.log = self.init_log(name)

    def init_log(cls, name):
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)-0.140s")
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        fileHandler = logging.FileHandler(name)
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        logger.addHandler(consoleHandler)
        logger.info(f"Log {name} created")
        return logger


    @classmethod
    def read_config(self, name):
        filename = os.path.join('config', name + '.json')
        try:
            with open(filename) as f:
                data = json.load(f)
                return data
        except Exception as e:
            return None


    @classmethod
    def registerClass(cls, classId, ctor):
        cls.factory[classId] = ctor


    @classmethod
    def instantiate(cls, classId):
        return cls.factory[classId]()

    @classmethod
    def instantiate_with_param(cls, classId, param):
        return cls.factory[classId](param)

    @classmethod
    def register(cls):
        if not cls.is_abstract():
            cls.registerClass(cls.get_class_id(), cls)
