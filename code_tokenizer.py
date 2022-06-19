from operator import le
from colors import *
def differentiate(m):
    return ' ' if m < '!' else '#' if m < '0' else '0' if m < ':' else '#' if m < 'A' else 'A' if m < '[' else '#' if m < 'a' else 'a' if m < '{' else '#'

def group_by_char_type(text):
    previous_char = None
    group = ''
    result = []
    def commit():
        nonlocal result, group, previous_char, current_char
        result.append([previous_char, group])
        previous_char = current_char
        group = ''
    for char in text:
        current_char = differentiate(char)
        if current_char != previous_char:
            commit()
        group += char
    commit()
    return result[1:]

class_label = {
    '#': PINK,
    '0': BLUE,
    'A': GREEN,
    'a': CYAN,
    ' ': YELLOW,
}

def color_by_char_type(text):
    grouped = group_by_char_type(text)
    result = ''
    for char_type, chars in grouped:
        result += class_label[char_type] + ''.join(chars) + WHITE
    return result

def tokenize(code):
    grouped = group_by_char_type(code)
    index = -1
    sub_index = 0
    result = []
    current_item = ''
    def read_word():
        nonlocal index, grouped, sub_index, current_item
        current_item += grouped[index][1]
        index += 1
        while index < len(grouped):
            char_type, chars = grouped[index]
            if char_type in ['A','0','a']:
                current_item += chars
                index += 1
                continue
            if(char_type == '#'):
                if(chars[sub_index] == '_'):
                    while sub_index < len(chars):
                        if(chars[sub_index] == '_'):
                            current_item += chars[sub_index]
                            sub_index += 1
                        else:
                            result.append(['word', current_item])
                            current_item = ''
                            read_symbol()
                            return
                    sub_index = 0
                    index += 1
                    continue
                result.append(['word', current_item])
                current_item = ''
                read_symbol()
                return
            if(char_type == '0'):
                result.append(['word', current_item])
                current_item = ''
                read_number()
                return
            if(char_type == ' '):
                result.append(['word', current_item])
                current_item = ''
                read_whitespace()
                return
        result.append(['word', current_item])
    def read_symbol():
        nonlocal index, grouped, sub_index, current_item
        current_segment = grouped[index][1]
        while sub_index < len(current_segment):
            if(sub_index+1 < len(current_segment)):
                dual = current_segment[sub_index:sub_index+2]
                if(dual == '=='):
                    result.append(['symbol', '=='])
                    sub_index += 2
                    continue
                if(dual == '<='):
                    result.append(['symbol', '<='])
                    sub_index += 2
                    continue
                if(dual == '>='):
                    result.append(['symbol', '>='])
                    sub_index += 2
                    continue
                if(dual == '!='):
                    result.append(['symbol', '!='])
                    sub_index += 2
                    continue
                if(dual == '&&'):
                    result.append(['symbol', '&&'])
                    sub_index += 2
                    continue
                if(dual == '||'):
                    result.append(['symbol', '||'])
                    sub_index += 2
                    continue
                if(dual == '<>'):
                    result.append(['symbol', '<>'])
                    sub_index += 2
                    continue
                if(dual == '<<'):
                    result.append(['symbol', '<<'])
                    sub_index += 2
                    continue
                if(dual == '>>'):
                    result.append(['symbol', '>>'])
                    sub_index += 2
                    continue
                if(dual == '++'):
                    result.append(['symbol', '++'])
                    sub_index += 2
                    continue
                if(dual == '--'):
                    result.append(['symbol', '--'])
                    sub_index += 2
                    continue
                if(dual == '+='):
                    result.append(['symbol', '+='])
                    sub_index += 2
                    continue
                if(dual == '-='):
                    result.append(['symbol', '-='])
                    sub_index += 2
                    continue
                if(dual == '*='):
                    result.append(['symbol', '*='])
                    sub_index += 2
                    continue
                if(dual == '/='):
                    result.append(['symbol', '/='])
                    sub_index += 2
                    continue
                if(dual == '->'):
                    result.append(['symbol', '->'])
                    sub_index += 2
                    continue
                if(dual == '=>'):
                    result.append(['symbol', '=>'])
                    sub_index += 2
                    continue
            if(current_segment[sub_index] == '_'):
                read_word()
                return
            result.append(['symbol', current_segment[sub_index]])
            sub_index += 1
        sub_index = 0
        read_unknown()
    def read_number():
        nonlocal index, grouped, sub_index
        result.append(['number', grouped[index][1]])
        read_unknown()
    def read_whitespace():
        nonlocal index, grouped, sub_index
        result.append(['whitespace', grouped[index][1]])
        read_unknown()
    def read_unknown():
        nonlocal index, grouped, sub_index
        index += 1
        if index >= len(grouped):
            return
        char_type, chars = grouped[index]
        if(char_type == '#'):
            read_symbol()
        elif(char_type == '0'):
            read_number()
        elif(char_type == ' '):
            read_whitespace()
        elif(char_type in ['A','a']):
            read_word()
        
        index += 1
    read_unknown()
    return result

equivalent = {
    '[': ']',
    '{': '}',
    '(': ')',
    '"': '"',
    "'": "'",
}

def group(code):
    tokens = tokenize(code)
    index = 0
    stack = []
    data_stack = [['root',[]]]
    while index < len(tokens):
        token, value = tokens[index]
        if(token != 'symbol'):
            data_stack[-1][1].append([token,value])
        else:
            if(len(stack) > 0 and value == stack[-1]):
                stack.pop()
                data_stack[-2][1].append(data_stack.pop())
            elif value in ['"', '\"','[','(','{']:
                stack.append(equivalent[value])
                data_stack.append([value,[]])
            else:
                if(len(stack) > 0 and ('"' in stack or '\'' in stack) and index + 1 < len(tokens) and value == '\\'):
                    data_stack[-1][1].append(['symbol','\\' + tokens[index+1][1]])
                    index += 1
                else:
                    data_stack[-1][1].append([token,value])
        index += 1
    return data_stack[0][1]

# programming specific below

def parse_groups(code):
    code = group(code)
    result = [[]]
    cursor = [code]
    index_stack = [0]
    current = [result[-1]]
    while(1):
        if(index_stack[-1] >= len(cursor[-1])):
            index_stack.pop()
            cursor.pop()
            if(len(current) > 1):
                current.pop()
            if(len(index_stack) == 0):
                break
            index_stack[-1] += 1
            continue
        type, value = cursor[-1][index_stack[-1]]
        if(type in ('word','number','symbol')):
            current[-1].append([type,value])
        if(type in ('{','[','(', '"', '\'')):
            index_stack.append(0)
            cursor.append(value)
            if(type == '['):
                if(len(current[-1]) == 0 or current[-1][-1][0] != 'word'):
                    node = ['array_define',[]]
                    current[-1].append(node)
                    current.append(node[-1])
                else:
                    node = ['array_call',[]]
                    current[-1][-1].append(node)
                    current.append(node[-1])
            elif(type == '{'):
                if(len(current[-1]) == 0):
                    node = ['code_block',[]]
                    current[-1].append(node)
                    current.append(node[-1])
                elif(current[-1][-1][0] == 'word' or current[-1][-1][0] == 'attached_group'): # problematic
                    node = ['attached_block',[]]
                    current[-1][-1].append(node)
                    current.append(node[-1])
                else:
                    node = ['dictionary_define',[]]
                    current[-1].append(node)
                    current.append(node[-1])
            elif(type == '('):
                if(len(current[-1]) == 0):
                    current.append(['numeric_group'])
                elif(current[-1][-1][0] == 'word'):
                    node = ['attached_group',[]]
                    current[-1][-1].append(node)
                    current.append(node[-1])
                else:
                    node = ['numeric_group',[]]
                    current[-1].append(node)
                    current.append(node[-1])
            elif(type == '"' or type == '\''):
                node = ['string',[]]
                current[-1].append(node)
                current.append(node[-1])
            continue
        index_stack[-1] += 1
    return result[0]


def split_code(code):
    code = parse_groups(code)
    def split(code):
        cursor = []
        result = []
        previous = False
        current = False
        for i in code:
            current = False
            if(type(i[0]) == str and i[0] != 'symbol'):
                current = True
                if(previous):
                    result.append(cursor if len(cursor) > 1 else cursor[0])
                    cursor = []
            else:
                current = False
            if(i[1] in [',',';']):
                result.append(cursor if len(cursor) > 1 else cursor[0])
                cursor = []
                current = False
            else:
                cursor.append(i)
            previous = current
        result.append(cursor if len(cursor) > 1 else cursor[0] if len(cursor) == 1 else [])
        return result if len(result) > 1 else result[0] if len(result) == 1 else []
    def scan(value):
        for i in range(len(value)):
            if(type(value[i]) == list):
                scan(value[i])
            else:
                if(value[i] in ['array_define','array_call','code_block','attached_group','attached_block','dictionary_define','numeric_group','attached_group']):
                    value[i+1] = split(value[i+1])
    
    for i in code:
        scan(i)
    result = split(code)
    return result
assignment_type = {
    '=': 'assign',
    '+=': 'add_assign',
    '-=': 'subtract_assign',
    '*=': 'multiply_assign',
    '/=': 'divide_assign',
}

def dot_layer(code):
    split = split_code(code)
    def scan(value):
        i = 0
        while(i < len(value)):
            if(type(value[i]) == list):
                if(len(value[i]) == 2):
                    if(value[i][1] in ['.','->']):
                        scan(value[i+1])
                        if(value[i-1][0] == 'access_group'):
                            value[i-1][1] += value[i+1]
                        else:
                            value[i-1] = ['access_group',[value[i-1]]+[value[i+1]]]
                        value.pop(i)
                        value.pop(i)
                        if(len(value) == 1):
                            value[:] = value[0]
                        i -= 1
                        continue
                    elif(value[i][1] in ['=','+=','-=','*=','/=']):
                        mod = value[i+1:]
                        if(len(mod) == 1):
                            mod = mod[0]
                        value[i-1] = [assignment_type[value[i][1]],[value[i-1],mod]]
                        value[:] = value[:i]
                        if(len(value) == 1):
                            value[:] = value[0]
                        continue
                    elif(value[i][1] in ['++','--']):
                        value[i-1] = ['increment' if value[i][1] == '++' else 'decrement' ,value[i-1]]
                        value.pop(i)
                        continue
                scan(value[i])
            i += 1
    scan(split)
    def second_pass(value):
        i = 0
        while(i < len(value)):
            if(type(value[i]) == list):
                if(len(value[i]) == 2):
                    if(value[i][1] == '!'):
                        value[i+1] = ['not',value[i+1]]
                        value.pop(i)
                        continue
                second_pass(value[i])
            i += 1
    second_pass(split)
    return split

def build_math(code):
    variables = []
    for item in code:
        if(item[0] == 'symbol'):
            if(len(variables) > 0):
                a = variables.pop()
            if(len(variables) > 0):
                b = variables.pop()
            if(a != None):
                if(b != None):
                    operations = [b, a]
                else:
                    operations = [a]
            else:
                operations = []
            
            variables.append(['operation',item[1],operations])
        else:
            variables.append(item)
    return variables[0]

def parse_math(code):
    priority = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '>': -1,
        '<': -1,
        '==': -1,
        '!=': -1,
        '>=': -1,
        '<=': -1,
        '&&': -2,
        '||': -2,
    }
    operations = []
    variables = []
    result = []
    # create a binary tree from the operations using the priority
    for item in code:
        token = item[0]
        value = item[1]
        if(token == 'symbol'):
            if(value in priority.keys()):
                current_priority = priority[value]
            else:
                current_priority = 0
            while(len(operations) > 0 and current_priority <= operations[-1][0]):
                a = None
                b = None
                if(len(variables) > 0):
                    a = variables.pop()
                if(len(variables) > 0):
                    b = variables.pop()
                if(b):
                    result.append(b)
                if(a):
                    result.append(a)
                if(len(operations) > 0):
                    result.append(operations.pop()[1])
            operations.append([current_priority,item])
        else:
            variables.append(item)
    busy = True
    while(busy):
        busy = False
        a = None
        b = None
        if(len(variables) > 0):
            a = variables.pop()
        if(len(variables) > 0):
            b = variables.pop()
        if(b):
            result.append(b)
        if(a):
            result.append(a)
        if(len(operations) > 0):
            result.append(operations.pop()[1])
            busy = True
    return build_math(result)

def math_layer(code):
    dot = dot_layer(code)
    def scan(value):
        i = 0
        while(i < len(value)):
            if(type(value[i]) == list):
                if(len(value[i]) > 0 and value[i][0]) == 'symbol':
                    value[:] = parse_math(value)
                    return
                scan(value[i])
            i += 1
    scan(dot)
    return dot

def parse(code):
    def read(parsed):
        result = []
        if(type(parsed[0]) != list):
            parsed = [parsed]
        for item in parsed:
            if item[0] == 'word' :
                if item[1] in ['if', 'for', 'while','foreach']:
                    result.append([item[1],[item[2][1],read(item[3][1])]])
                    continue
                elif item[1] == 'else':
                    result.append(['else',read(item[2][1])])
                    continue
            elif item[0] == 'assign':
                result.append(['assign',[item[1][0],item[1][1]]])
                continue
            result.append(item)
        return result if len(result) > 1 else result[0]
    return read(math_layer(code))