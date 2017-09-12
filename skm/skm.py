import sys
import json
from database import *
from parser import *
from util import *

MESSAGE_Y_N = ' (y/n)'

MESSAGE_CREATE_DEFAULT_CONFIG = 'creating default config at: {0}'
MESSAGE_PROMPT_NEW_DATABASE = 'please enter knowledge base path (empty for default: {0}):'
MESSAGE_CONFIRM_CREATE_DIR = 'directory does not exist. confirm creation?' + MESSAGE_Y_N
MESSAGE_CREATING_DIR = 'creating directory for knowledge base... '
MESSAGE_USING_DEFAULT_PATH = 'using default path: {0}'
MESSAGE_CURRENT_PATH = 'current knowledge base path: {0}'
MESSAGE_BAD_DATABASE_PATH = 'invalid path.'
MESSAGE_FAILED = 'failed.'
MESSAGE_DONE = 'done.'
MESSAGE_USAGE = 'arguments: operation ...'
MESSAGE_USAGE_ADD = 'arguments: add file_name'
MESSAGE_USAGE_GET = 'arguments: get topic_name'

CONFIG_FILENAME = os.path.join(HOME_PATH, '_skm')
CONFIG_PATH = os.path.join(HOME_PATH, CONFIG_FILENAME)

DEFAULT_DATABASE_PATH = os.path.join(HOME_PATH, 'knowledge')
EXTENSION = '.skm'
DATABASE_FILENAME = 'knowledge_base' + EXTENSION

CMD_NAME = ''
DATABASE_PATH = ''

CONFIG_DEFAULT = {
        'database_path': None,
    }

config = {}

database = None

if os.path.isfile(CONFIG_PATH):
    config = read_json(CONFIG_PATH, {})
    if not isinstance(config, dict):
        config = {}

else:
    print(MESSAGE_CREATE_DEFAULT_CONFIG.format(CONFIG_PATH))

dict_concat(CONFIG_DEFAULT, config)

def print_usage():
    print(MESSAGE_USAGE.format(CMD_NAME))

def set_path():
    if config['database_path'] is not None:
        print(MESSAGE_CURRENT_PATH.format(config['database_path']))
        
    dbpath = ''
    while True:
        print(MESSAGE_PROMPT_NEW_DATABASE.format(DEFAULT_DATABASE_PATH))
        dbpath = str(input())
        if is_empty_line(dbpath):
            print(MESSAGE_USING_DEFAULT_PATH.format(DEFAULT_DATABASE_PATH))
            dbpath = DEFAULT_DATABASE_PATH
        
        if not os.path.isabs(dbpath):
            print(MESSAGE_BAD_DATABASE_PATH)
            
        elif not os.path.exists(dbpath):
            print(MESSAGE_CONFIRM_CREATE_DIR)
            confirmation = str(input())
            if confirmation != 'y':
                continue
                
            printi(MESSAGE_CREATING_DIR)
            try:
                os.makedirs(dbpath)
                print(MESSAGE_DONE)
                break
            
            except:
                print(MESSAGE_FAILED)
            
        else:
            if os.path.isdir(dbpath):
                break
            
            else:
                print(MESSAGE_BAD_DATABASE_PATH)
    
    config['database_path'] = dbpath
    
def add(args):
    if len(args) <= 0:
        print(MESSAGE_USAGE_ADD)
        return 1

def get(args):
    if len(args) <= 0:
        print(MESSAGE_USAGE_GET)
        return 1

def debug(args):
    database.add_topic(Topic())
    return 0

def main(argc, argv):
    global CMD_NAME, DATABASE_PATH, database
    
    CMD_NAME = argv[0]
    
    if argc < 2:
        print(MESSAGE_USAGE)
        return 1
    
    operation = argv[1]

    if operation == 'set_path':
        set_path()

    if config['database_path'] is None or not os.path.isdir(config['database_path']):
        set_path()
    
    DATABASE_PATH = os.path.join(config['database_path'], DATABASE_FILENAME)
    
    database = Database(read_json(DATABASE_PATH, {}))
    
    if operation == 'add':
        return add(argv[2:])
    
    elif operation == 'get':
        return get(argv[2:])
    
    elif operation == 'debug':
        return debug(argv[2:])
    
    return 0

if __name__ == '__main__':
    if main(len(sys.argv), sys.argv) == 0:
        write_json(CONFIG_PATH, config)
        write_json(DATABASE_PATH, database.to_json())
