from util import *
import copy

class Topic:
    
    def __init__(self, json_object = {}):
        self.id         = get_from(json_object, 'id', 0)
        self.name       = get_from(json_object, 'name', '')
        self.alias      = get_from(json_object, 'alias', [])
        self.content    = get_from(json_object, 'content', '')
        self.parent_id  = get_from(json_object, 'parent_id', 0)
        self.forward_id = get_from(json_object, 'forward_id', [])
        
        self.parent   = None
        self.children = []
        self.forward  = []
        self.backward = []
    
    def to_json(self):
        json_object = {}
        
        json_object['id']      = self.id
        json_object['name']    = self.name
        json_object['alias']   = self.alias
        json_object['content'] = self.content
        #  json_object['parent']  = self.parent
        #  json_object['forward'] = self.forward
        
        return json_object

class Database:
    
    def __init__(self, json_object):
        self.id_list      = []
        self.topics_by_id = {}
        
        topics = get_from(json_object, 'topics', [])
        
        for obj in topics:
            self.add_topic(Topic(obj))
    
    def add_topic(self, topic):
        if topic.id == 0:
            topic.id = self.get_new_id()
        
        if topic.id in self.topics_by_id:
            return False
        
        self.topics_by_id[topic.id] = topic
        self.id_list.insert(upper_bound(self.id_list, topic.id), topic.id)
        print(self.id_list)
        
        return True
    
    def to_json(self):
        json_object = {}
        json_object['topics'] = [self.topics_by_id[id].to_json() for id in self.topics_by_id]
        return json_object
    
    def get_new_id(self):
        old = 0
        for id in self.id_list:
            if old != id - 1:
                return old + 1
            
            old = id
        
        return old + 1
