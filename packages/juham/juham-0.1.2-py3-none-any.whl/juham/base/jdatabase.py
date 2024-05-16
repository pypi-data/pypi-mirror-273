"""@package jdatabase
Module defining abstraction to database on which the home automation data is written for inspection and 
recording. 


"""

from juham.base.jobject import JObject

class JDatabase(JObject):
    """@class JDatabase
    Class implementing abstract interface to time series databases for data recording.
    """

    token = None
    org = None
    host = None
    database=None
    configured = False

    
    def __init__(self, name):
        super().__init__(name)

    def write(self, table, key, record):
        """!
        Write record to database table
        
        @param string table: name of the table to be written
        @param key time series key (index) with associated value
        @param record  dict: Python dictionary object describing  the database fields to be written with their respected values
        
        """
        raise Exception('write not implemented')
        
    def read(self, table, key):
        """!
        Read record from database table. 
        @param record  dict: Python dictionary object describing  the database fields to be written with their respected values
        @return List of records matching the key
        @note Not supported by design 
        
        """
        raise Exception('read not implemented')

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


