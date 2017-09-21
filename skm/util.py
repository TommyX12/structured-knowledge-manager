import os, sys, codecs, glob, re, json, copy, bisect, pickle

HOME_PATH = os.path.expanduser('~')

def printi(string):
    print(string, flush=True, end='')

def list_dir(pattern):
    return glob.glob(pattern)   

def read_file(path, binary = False, encoding = 'utf-8-sig', default = ''):
    if not os.path.isfile(path):
        #  write_file(path, '')
        return default

    with open(path, 'rb' if binary else 'r', encoding = None if binary else encoding) as f:
        content = f.read()
    
    return content

def write_file(path, data, binary = False):
    # able to make containing path if not exist
    file = open(path, 'wb' if binary else 'w')
    file.write(data)
    file.close()

def read_json(path, default=None):
    try:
        result = json.loads(read_file(path))
        return result
    
    except:
        return default

PRETTY_JSON = False

def write_json(path, data):
    write_file(path, json.dumps(data, indent = '  ' if PRETTY_JSON else None, separators = (',', ':')))

def read_pickle(path, default=None):
    data = read_file(path, True, default = None)
    if data is None:
        return default
    
    try:
        result = pickle.loads(data)
        return result
    
    except:
        return default

def write_pickle(path, obj):
    write_file(path, pickle.dumps(obj), True)

def clamp(num, l, r):
    if num < l:
        return l

    if num > r:
        return r
    
    return num

def escape_script_string(str):
    str = re.sub(r'([\\\"\'])', r'\\\1', str)
    return str

def top(stack):
    return stack[len(stack) - 1]

def cut(string, i, j):
    return string[:i] + string[j:]

def insert(string, i, part):
    return string[:i] + part + string[i:]

def dict_overwrite(src, dest, deep_copy = True, in_place = True, nested = True):
    if not in_place:
        dest = copy.deepcopy(dest)
    
    for key in src:
        if nested and isinstance(dest[key], dict) and isinstance(src[key], dict):
            dict_concat(src[key], dest[key], deep_copy, True, True)
        
        else:
            dest[key] = copy.deepcopy(src[key])
    
    return dest

def get_indentation_len(line):
    ptr = 0
    while ptr < len(line):
        if line[ptr] != ' ' and line[ptr] != '\t':
            break
        
        ptr += 1
        
    return ptr

def get_indentation(line):
    return line[:get_indentation_len(line)]

def is_empty_line(line):
    return len(line.lstrip()) == 0

def skip(line, i, chars):
    while i < len(line) and line[i] in chars:
        i += 1
    
    return i

def skip_white_space(line, i):
    return skip(line, i, ' \t\n')

def skip_word_char(line, i):
    return skip(line, i, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')

def get_from(container, key, default = None, deep_copy = True):
    if deep_copy:
        return copy.deepcopy(container[key]) if key in container else copy.deepcopy(default)
    
    else:
        return container[key] if key in container else default

def extract_paren(line, i):
    if i >= len(line) or line[i] != '(':
        return i
    
    cnt = 1
    i += 1
    while i < len(line):
        if line[i] == '(':
            cnt += 1
        
        elif line[i] == ')':
            cnt -= 1
            if cnt == 0:
                return i + 1
        
        i += 1
    
    return len(line)

def align_indentation(lines, i = 0, j = -1, offset = ''):
    if j < 0:
        j = len(lines)
    
    min_indent_len = -1
    min_indent = ''
    for k in range(i, j):
        if is_empty_line(lines[k]):
            continue
        
        cur_indent = get_indentation_len(lines[k])
        if min_indent_len == -1 or cur_indent < min_indent_len:
            min_indent_len = cur_indent
            min_indent = lines[k][:cur_indent]
    
    if min_indent_len >= 0:
        for k in range(i, j):
            lines[k] = offset + lines[k][min_indent_len:]
    
    return min_indent

def add_indentation(lines, indent, i = 0, j = -1):
    if j < 0:
        j = len(lines)
    
    for k in range(i, j):
        lines[k] = indent + lines[k]

def indented_insert(line, part):
    return insert(line, get_indentation_len(line), part)

def has_stripped_suffix(string, suffix):
    if len(string) == 0 or len(suffix) == 0:
        return False
    
    i = len(string) - 1
    while i >= 0 and string[i] in ' \t\n':
        i -= 1
    
    j = len(suffix) - 1
    while i >= 0 and j >= 0 and string[i] == suffix[j]:
        i -= 1
        j -= 1
    
    return j < 0

# result[i] = index of the first line below i that has indentation <= get_indentation_len(lines(i))
def get_indent_match(lines):
    result = [0 for i in range(len(lines))]
    indent_stack = [] # element: (line index, indentation)
    j = 0
    for i in range(len(lines)):
        line = lines[i]
        if is_empty_line(line):
            continue
        
        cur_indent = get_indentation_len(line)
        while len(indent_stack) > 0 and top(indent_stack)[1] >= cur_indent:
            result[indent_stack.pop()[0]] = j + 1
        
        indent_stack.append((i, cur_indent))
        
        j = i

    for entry in indent_stack:
        result[entry[0]] = j + 1
            
    return result

MATCHING_BRACKET = {
    '(': ')',
    '[': ']',
    '{': '}',
    ')': '(',
    ']': '[',
    '}': '{',
}

def matching_bracket(c):
    return MATCHING_BRACKET[c]

# result[i] = index of the char that have matching bracket
# !!!WARNING: this has not been tested
def get_bracket_match(line):
    l = len(line)
    result = [0 for i in range(len(line))]
    stacks = {
        '(': [],
        '[': [],
        '{': [],
    }
    for i in range(len(line)):
        c = line[i]
        if c in '([{':
            stacks[c].append(i)
        
        elif c in ')]}':
            c = MATCHING_BRACKET[c]
            stack = stacks[c]
            if len(stack) > 0:
                j = stack.pop()
                result[i] = j
                result[j] = i
        
    for c in stacks:
        for i in stacks[c]:
            result[i] = l
            
    return result

def lower_bound(arr, x):
    return bisect.bisect_left(arr, x, lo = 0, hi = len(arr))

def upper_bound(arr, x):
    return bisect.bisect_right(arr, x, lo = 0, hi = len(arr))


class JSONProperty(object):
    
    def __init__(self,
        name,
        default        = None,
        object_type    = None,
        container_type = None,
        get_json       = None,
        set_json       = None):
        
        self.name           = name
        self.default        = default
        self.object_type    = object_type
        self.container_type = container_type
        self.get_json       = get_json if get_json is not None else JSONProperty.__default_get_json__
        self.set_json       = set_json if set_json is not None else JSONProperty.__default_set_json__
    
    def __default_get_json__(prop, obj, json_object, scope_dict):
        value = obj.__dict__[prop.name]
        if prop.object_type is not None:
            if prop.container_type == list:
                json_object[prop.name] = [item.get_json(scope_dict) if item is not None else None for item in value]
                
            elif prop.container_type == dict:
                result = {}
                for key in value:
                    result[str(key)] = value[key].get_json(scope_dict) if value[key] is not None else None
                    
                json_object[prop.name] = result
            
            else:
                json_object[prop.name] = value.get_json(scope_dict) if value is not None else None
            
        else:
            json_object[prop.name] = copy.deepcopy(value)
    
    def __default_set_json__(prop, obj, json_object, scope_dict):
        if prop.object_type is not None:
            if prop.container_type == list:
                container = get_from(json_object, prop.name, [])
                obj.__dict__[prop.name] = [JSONObject.__from_json__(prop.object_type, item, scope_dict) if item is not None else None for item in container]
                
            elif prop.container_type == dict:
                result = {}
                
                container = get_from(json_object, prop.name, {})
                for key in container:
                    result[key] = JSONObject.__from_json__(prop.object_type, value[key], scope_dict) if value[key] is not None else None
                    
                obj.__dict__[prop.name] = result
            
            else:
                if prop.name in json_object:
                    if json_object[prop.name] is None:
                        obj.__dict__[prop.name] = None
                        
                    else:
                        obj.__dict__[prop.name] = JSONObject.__from_json__(prop.object_type, json_object[prop.name], scope_dict)
                    
                else:
                    obj.__dict__[prop.name] = copy.deepcopy(prop.default)
            
        else:
            default = prop.default
            if prop.container_type == list:
                default = []
                
            if prop.container_type == dict:
                default = {}
                
            obj.__dict__[prop.name] = get_from(json_object, prop.name, default)
        
class JSONObject(object):
    
    __properties__ = [
        
    ]
    
    def __init__(self, json_object = {}, scope_dict = None):
        self.set_json(json_object, scope_dict)
        
    def get_json(self, scope_dict = None):
        self.__before_save__()
        
        if scope_dict is None:
            scope_dict = {}
        
        json_id = id(self)
        if json_id in scope_dict:
            return {
                '__json_id__': 0,
                '__json_ptr__': json_id,
            }
        
        scope_dict[json_id] = self
        
        result = {
            '__json_id__': json_id,
        }
        for prop in self.__class__.__properties__:
            prop.get_json(prop, self, result, scope_dict)
        
        return result
    
    def __before_save__(self):
        pass
    
    def __after_load__(self):
        pass
    
    def set_json(self, json_object, scope_dict = None):
        if scope_dict is None:
            scope_dict = {}
            JSONObject.__get_scope_dict__(json_object, scope_dict)
        
        json_id = get_from(json_object, '__json_id__', 0)
        
        scope_dict[json_id] = self
        
        for prop in self.__class__.__properties__:
            prop.set_json(prop, self, json_object, scope_dict)
            
        self.__after_load__()
    
    def __get_scope_dict__(json_object, scope_dict):
        if isinstance(json_object, dict):
            json_id = get_from(json_object, '__json_id__', 0)
            if json_id != 0:
                scope_dict[json_id] = json_object
            
            for key in json_object:
                JSONObject.__get_scope_dict__(json_object[key], scope_dict)
        
        elif isinstance(json_object, list):
            for item in json_object:
                JSONObject.__get_scope_dict__(item, scope_dict)
                
    def __from_json__(object_type, json_object, scope_dict):
        json_id = get_from(json_object, '__json_id__', 0)
        if json_id == 0:
            json_ptr = get_from(json_object, '__json_ptr__', 0)
            if isinstance(scope_dict[json_ptr], dict):
                scope_dict[json_ptr] = object_type(scope_dict[json_ptr], scope_dict)
                
            return scope_dict[json_ptr]
        
        elif isinstance(scope_dict[json_id], JSONObject):
            return scope_dict[json_id]
        
        scope_dict[json_id] = object_type(json_object, scope_dict)
        return scope_dict[json_id]

#  class A(JSONObject):
    
    #  __properties__ = [
        #  JSONProperty(
            #  name = 'asdf',
            #  default = 9),
        
        #  JSONProperty(
            #  name = 'hello',
            #  container_type = list,
            #  default = []),
    #  ]

#  class B(JSONObject):
    
    #  __properties__ = [
        #  JSONProperty(
            #  name = 'f',
            #  object_type = A,
            #  container_type = list),
        
        #  JSONProperty(
            #  name = 'asdv',
            #  object_type = A),
        
        #  JSONProperty(
            #  name = 'world',
            #  object_type = A,
            #  container_type = dict),
    #  ]

#  r = B()
#  r.asdv.hello += [2, 4, 5]
#  r.f += [A(), A()]
#  r.f[0].asdf = 1
#  r.f[1].asdf = 2
#  string = json.dumps(r.get_json())
#  print(string)
#  s = B(json.loads(string))
#  print(json.dumps(s.get_json()))
