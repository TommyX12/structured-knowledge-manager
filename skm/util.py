import os, sys, codecs, glob, re, json, copy

HOME_PATH = os.path.expanduser('~')

def printi(string):
    print(string, flush=True, end='')

def list_dir(pattern):
    return glob.glob(pattern)   

def read_file(path):
    if not os.path.isfile(path):
        #  write_file(path, '')
        return ''

    with open(path, encoding='utf-8-sig') as f:
        content = f.read()
    
    return content

def write_file(path, data):
    # able to make containing path if not exist
    file = open(path, 'w')
    file.write(data)
    file.close()

def read_json(path, default=None):
    try:
        result = json.loads(read_file(path))
        return result
    
    except:
        return default

def write_json(path, data):
    write_file(path, json.dumps(data))

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

def dict_concat(src, dest, only_add = False, deep_copy = False):
    for key in src:
        if not only_add or key not in dest:
            dest[key] = copy.deepcopy() if deep_copy else src[key]
    
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


