from util import *
from database import *
import re

MARKER_STR = {
    '>>': 'req_f',
    '<<': 'req_b',
    '>':  'rel_f',
    '<':  'rel_b',
    '><':  'rel_fb',
    '-':  'child',
    '@':  'cmd',
}

MARKER_TYPE = {}
for key in MARKER_STR:
    MARKER_TYPE[MARKER_STR[key]] = key

class CommandOp(object):
    
    def __init__(self, topic_op, command, arg):
        self.topic_op = topic_op
        self.command  = command
        self.arg      = arg
    
    def apply(self):
        pass
    
class ConnectOp(object):
    
    def __init__(self, topic_op_from, topic_op_to, type_str, line):
        self.topic_op = topic_op
        self.type_str = type_str
        self.line     = line
    
    def apply(self):
        pass

class TopicOp(object):
    
    def __init__(self, rough_name, content):
        # this is the place to ask for search and store a reference of actual topic
        pass

class SKMParser(object):
    
    def __init__(self, database):
        self.database = database

    def _parse_topic(self, ops, lines, start_line, end_line):
        parse

    def parse_skm(self, text, database):
        lines = text.split('\n')
        indent_match = get_indent_match(lines)
        topic_stack
        for line in lines:
            indent = get_indentation(line)
            indent_len = get_indentation_len(line)
            line = line[indent_len:]
            
            marker = ''
            ind = regex_find(line, r'\s')
            if ind >= 0:
                marker = line[:ind]
            
            marker_type = None
            if marker in MARKER_STR:
                marker_type = MARKER_STR[marker]
            
            if marker_type not None:
                if marker_type == '>>':
                    
                    
                if marker_type == '>>':
                
                
                if marker_type == '<<':
                
                
                if marker_type == '>':
                
                
                if marker_type == '<':
                
                
                if marker_type == '><':
                
                
                if marker_type == '-':
                
                
                if marker_type == '@':
                
                

            # make a dict that group all the command op with the same command to execute them all at once.


        # now process all the op you made

    def edit_skm(text, database):
        # generate bunch of op
        # now process all the op into string
