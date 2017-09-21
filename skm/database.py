from util import *
import copy

class Connection(JSONObject):

    RELATIONAL = 'rel'
    REQUIREMENT = 'req'
    
class Topic(JSONObject):
    
    __properties__ = [
        JSONProperty(
            name = 'id',
            default = 0),
        
        JSONProperty(
            name = 'name',
            default = ''),
        
        JSONProperty(
            name = 'alias',
            container_type = list),
        
        JSONProperty(
            name = 'content',
            default = ''),
        
        JSONProperty(
            name = 'parent',
            object_type = Connection),
        
        JSONProperty(
            name = 'connections',
            object_type = Connection,
            container_type = list),
        
    ]

    def add_connection(self, topic, type):
        connection = Connection()
        connection.topic = topic
        connection.type  = type
        self.connections.append(connection)
        
        return connection
    
    def remove_connection(self, index):
        self.connections.pop(index)
    
    def set_parent(self, parent):
        self.parent = parent
        if parent is None:
            pass
        
    def rename(self, name):
        self.name = name
    
    def set_content(self, content):
        self.content = content
    
    def add_alias(self, alias):
        self.alias.append(alias)
    
    def remove_alias(self, index):
        self.alias.pop(index)
    
    def clear_data(self):
        while len(self.alias) > 0:
            self.remove_alias(0)
        
        while len(self.connections) > 0:
            self.remove_connection(0)
        
        self.set_content('')
    
    def __str__(self):
        return self.name


Connection.__properties__ = [
    JSONProperty(
        name = 'topic',
        object_type = Topic,
        default = None),
    
    JSONProperty(
        name = 'type',
        default = 'rel'),
    
]

class Database(JSONObject):

    __properties__ = [
        JSONProperty(
            name = 'topics',
            object_type = Topic,
            container_type = list),
    ]

    def __after_load__(self):
        self.id_list = []
        for topic in self.topics:
            self.id_list.insert(upper_bound(self.id_list, topic.id), topic.id)

    def add_topic(self, name, content):
        topic = Topic()
        topic.id = self.get_new_id()
        topic.rename(name)
        topic.set_content(content)
        self.topics.append(topic)
        self.id_list.insert(upper_bound(self.id_list, topic.id), topic.id)
    
    def delete_topic(self, _topic):
        found = False
        for i in range(len(self.topics)):
            topic = self.topics[i]
            if _topic is topic:
                found = True
                self.topics.pop(i)
                break
        
        if not found:
            return
        
        _topic.set_parent(None)
        
        for topic in self.topics:
            i = 0
            while i < len(topic.connections):
                connection = topic.connections[i]
                if connection.topic is _topic:
                    topic.remove_connection(i)
                    i -= 1
                    
                i += 1
        
        for i in range(len(self.id_list)):
            id = self.id_list[i]
            if id == _topic.id:
                self.id_list.pop(i)
                break
    
    def __str__(self):
        return str([str(topic) for topic in self.topics])
    
    def get_new_id(self):
        old = 0
        for id in self.id_list:
            if old != id - 1:
                return old + 1
            
            old = id
        
        return old + 1

