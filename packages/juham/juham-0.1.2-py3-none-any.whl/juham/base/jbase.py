

import json
from datetime import datetime, timezone, time
from time import strftime, localtime
from juham.base.jobject import JObject


class JBase(JObject):

  # class attributes
  database_class_id = 0
  pubsub_class_id = 0
  
  def __init__(self, name = ''):
    super().__init__(name)
    self.init_database(name)
    self.init_pubsub(name)
    self.info(name + ' instantiated')

    
  def init_database(self, name):
    if JBase.database_class_id != 0:
      self.database_client = JObject.instantiate(JBase.database_class_id)
      self.database_client.name = name
    else:
      self.warning("Suscpicious configuration: no database_class_id set")

      
  def init_pubsub(self, name):
    if JBase.pubsub_class_id != 0:
      self.mqtt_client = JObject.instantiate_with_param(JBase.pubsub_class_id, name)
      self.mqtt_client.on_message = self.on_message
      self.mqtt_client.on_connect = self.on_connect
      self.mqtt_client.on_disconnect = self.on_disconnect
      if self.mqtt_client.connect() != 0:
        self.error(self.mqtt_client, name, "Couldn't connect to the mqtt broker", str(self.mqtt))
    else:
      self.warning("Suscpicious configuration: no mqtt_class_id set")


  def subscribe(self, topic):
    self.mqtt_client.connected_flag = True
    self.mqtt_client.subscribe(topic)
    self.info(self.name + ' subscribed to ' + topic)


  def on_message(self, client, userdata, msg):
    # up to sub classes to handle
    return

  def on_connect(self, client, userdata, flags, rc):
    # connected to the broker
    # up to sub classes to subscribe on topics
    self.info(self.name + ' connected to the mqtt broker ')


  def on_disconnect(self, client, userdata, rc=0):
    client.loop_stop()
    self.info(self.name + ' disconnected from the mqtt broker ')
    
  def epoc2utc(self, epoch):
    return datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%dT%H:%M:%SZ')

  
  def timestampstr(self, ts):
    return str(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

  
  def timestamp(self):
    return datetime.now(timezone.utc).timestamp()

  
  def is_time_between(self, begin_time, end_time, check_time=None):
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
      return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
      return check_time >= begin_time or check_time <= end_time

    
  def write(self, point):
    try:
      self.database_client.write(point)
    except Exception as e:
      self.error("Writing to influx failed", str(e))


  def debug(self, msg, details=''):
    self.log.debug(self.name + ':' + str(msg) + ' - ' + str(details))
    self.log_message('Debug', msg, details='')

    
  def info(self, msg, details=''):
    self.log.info(self.name + ':' + str(msg) + ' - ' + str(details))
    self.log_message('Info', msg, details='')

    
  def warning(self, msg, details=''):
    self.log.warning(self.name + ':' + str(msg) + ' - ' + str(details))
    self.log_message('Warn', msg, details)

    
  def error(self, msg, details=''):
    self.log.error(self.name + ':' + str(msg) + ' - ' + str(details))
    self.log_message('Error', msg, details)

    
  def log_message(self, type, msg, details=''):
    try:
      msg = {
        'Timestamp' : self.timestamp(),
        'Class' : type,
        'Source' : self.name,
        'Msg' : msg,
        'Details' : str(details)
      }
      self.mqtt_client.publish("kukkila/log", json.dumps(msg), 1)
    except Exception as e:
      self.log.error(f"Publishing log event failed {str(e)}")


  def run(self):
    self.mqtt_client.loop_start()

    
  def run_forever(self):
    self.mqtt_client.loop_forever()

    


  

