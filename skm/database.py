from util import *
import copy

class Picklable:
    def __getstate__(self):
        result = self.__dict__.copy()
        for key in result:
            if key.startswith('_'):
                del result[key]
            
        return result;
    
    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

class Connection(Picklable):

    RELATIONAL = 'rel'
    REQUIREMENT = 'req'

    def __init__(self):
        self.dest = None
        self.type = Connection.RELATIONAL

class Topic(Picklable):
    
    def __init__(self):
        self.id          = 0
        self.name        = ''
        self.alias       = []
        self.content     = ''
        self.parent      = None
        self.children    = []
        self.connections = []
    
    def add_connection(self, topic):
        self.connections.append(topic)
    
    def __str__(self):
        return self.name

class Database(Picklable):

    def __init__(self):
        self.topics = []

    def add_topic(self, topic):
        self.topics.append(topic)
    
    def __str__(self):
        return str([str(topic) for topic in self.topics])
    
#  class Connection:
    
    #  RELATIONAL = 'rel'
    #  REQUIREMENT = 'req'
    
    #  def __init__(self, json_object = {}):
        #  self._dest_id = get_from(json_object, 'dest_id', 0)
        #  self.type    = get_from(json_object, 'type', Connection.RELATIONAL)
        
        #  self.dest = None
    
    #  def to_json(self):
        #  json_object = {}
        
        #  json_object['dest_id'] = self.dest.id
        #  json_object['type']    = self.type
        
        #  return json_object

#  class Topic:
    
    #  def __init__(self, json_object = {}):
        #  self.id         = get_from(json_object, 'id', 0)
        #  self.name       = get_from(json_object, 'name', '')
        #  self.alias      = get_from(json_object, 'alias', [])
        #  self.content    = get_from(json_object, 'content', '')
        #  self._parent_id = get_from(json_object, 'parent_id', 0)
        
        #  self.connections    = get_from(json_object, 'forward_ids', [])
        
        #  self.parent   = None
        #  self.children = []
    
    #  def to_json(self):
        #  json_object = {}
        
        #  json_object['id']      = self.id
        #  json_object['name']    = self.name
        #  json_object['alias']   = self.alias
        #  json_object['content'] = self.content
        #  json_object['parent_id']  = self.parent.id
        #  json_object['connections'] = [con.to_json() for con in self.connections]
        
        #  return json_object

#  class Database:
    
    #  def __init__(self, json_object):
        #  self.id_list      = []
        #  self.topics_by_id = {}
        
        #  topic_objs = get_from(json_object, 'topics', [])
        
        #  for obj in topic_objs:
            #  self.add_topic(Topic(obj))
        
        #  for id_ in self.topics_by_id:
            #  topic = self.topics_by_id[id_]
            #  for forward_id in topic._forward_ids:
                
    
    #  def add_topic(self, topic):
        #  if topic.id == 0:
            #  topic.id = self.get_new_id()
        
        #  if topic.id in self.topics_by_id:
            #  return False
        
        #  self.topics_by_id[topic.id] = topic
        #  self.id_list.insert(upper_bound(self.id_list, topic.id), topic.id)
        #  print(self.id_list)
        
        #  return True
    
    #  def add_connection():
        
    
    #  def to_json(self):
        #  json_object = {}
        #  json_object['topics'] = [self.topics_by_id[id].to_json() for id in self.topics_by_id]
        #  return json_object
    
    #  def get_new_id(self):
        #  old = 0
        #  for id in self.id_list:
            #  if old != id - 1:
                #  return old + 1
            
            #  old = id
        
        #  return old + 1

