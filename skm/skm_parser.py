from util import *
from database import *

class CommandOp(object):
    
    def __init__(self, topic_op, command, arg):
        self.topic_op = topic_op
        self.command  = command
        self.arg      = arg
    
    def apply(self):
        pass

    
class ConnectOp(object):
    
    def __init__(self, topic_op_from, topic_op_to, type_str):
        self.topic_op = topic_op
        self.type_str = type_str
    
    def apply(self):
        pass

class TopicOp(object):
    
    def __init__(self, rough_name, content):
        # this is the place to ask for search and store a reference of actual topic
        pass

def parse_skm(text, database):
    lines = text.split('\n')
    for line in lines:
        indent = get_indentation(line)
        indent_len = get_indentation_len(line)
        line = line[indent_len:]
        
        # make a dict that group all the command op with the same command to execute them all at once.
    
    # now process all the op you made

def edit_skm(text, database):
    # generate bunch of op
    # now process all the op into string
