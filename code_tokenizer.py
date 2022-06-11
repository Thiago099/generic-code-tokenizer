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
            if token != 'whitespace': # or "'" in stack or '"' in stack:
                data_stack[-1][1].append([token,value])
        else:
            if(len(stack) > 0 and value == stack[-1]):
                stack.pop()
                data_stack[-2][1].append(data_stack.pop())
            elif value in ['"', '\"','[','(','{']:
                stack.append(equivalent[value])
                data_stack.append([value,[]])
            else:
                if(len(stack) > 0 and '"' in stack or '\'' in stack and index + 1 < len(tokens) and value == '\\'):
                    data_stack[-1][1].append(['symbol','\\' + tokens[index+1][1]])
                    index += 1
                else:
                    data_stack[-1][1].append([token,value])
        index += 1
    return data_stack[0][1]