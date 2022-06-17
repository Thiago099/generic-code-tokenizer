variable_types = {
    'number': 'number',
    'string': 'string',
    'array_define': 'array',
    'dictionary_define': 'dictionary',
    'word':'unknown'
}

def read_access_group(code):
    for item in code[1]:
        yield item
modifier_type = {
    'increment': 'add',
    'decrement': 'subtract',
    'add_assign': 'add',
    'subtract_assign': 'subtract',
    'multiply_assign': 'multiply',
    'divide_assign': 'divide'
}
def read_modifier(code):
    if code[0] in ['increment', 'decrement']:
        value = ['number','1']
        modifier_variable = code[1][1]
    elif code[0] in ['add_assign', 'subtract_assign', 'multiply_assign', 'divide_assign']:
        value = code[1][1]
        modifier_variable = code[1][0][1]
    modifier = modifier_type[code[0]]
    return modifier_variable, modifier, value
equivalent = {
    '>' : '<=',
    '<' : '>=',
    '>=' : '<',
    '<=' : '>',
    '==' : '==',
    '!=' : '!='
}

variables = {}
def scan(item):
    i = 0
    while(i < len(item)):
        if(type(item[i]) == list):
            if(item[i][0] == 'word' and (item[i][1] in ['for','if','while'])):
                command = item[i][1]
                parameters = item[i][2][1]
                block = item[i][3][1]

                if(type(block[0]) != list):
                    block = [block]

                print('action: ', command)

                if(command == 'for'):

                    variable, value, variable_type = read_assignment(parameters[0][0])


                    condition_instruction = parameters[1]
                    if(condition_instruction[0] == 'operation'):
                        limiter = condition_instruction[1]
                        a = condition_instruction[2][0]
                        b = condition_instruction[2][1]

                        if(a[0] == 'word' or b[0] == 'word'):
                            if(a[1] == variable):
                                end = b
                            elif(b[1] == variable):
                                end = a
                                limiter = equivalent[limiter]
                            else:
                                raise Exception('incongruent stop')
                            
                    step_instruction = parameters[2][0]
                    modifier_iterator, modifier, step = read_modifier(step_instruction)
                    if(modifier_iterator != variable):
                        raise Exception('incongruent step')
                    
                    print('iterator: ',variable)
                    print()
                    print('modifier type: ',modifier)
                    print('limiter: ', limiter)
                    print()
                    print('start: ',value)
                    print('end: ', end)
                    print('step: ',step)
                else:
                    print(parameters)

                print()

                scan(block)
                
                i += 1
                continue
            elif(item[i][0] == 'assign'):
                print('action: assign')
                variable, value, variable_type = read_assignment(item[i])
                print('variable: ',variable)
                print('type: ',variable_type)
                print('value: ',value)
                print()
                i += 1
                continue
            elif(item[i][0] in ['increment', 'decrement', 'add_assign', 'subtract_assign', 'multiply_assign', 'divide_assign']):
                print('action> modify')
                modifier_iterator, modifier, value = read_modifier(item[i])
                print('variable: ',modifier_iterator)
                print('modifier type: ',modifier)
                print('modifier value: ',value)
                print()
                i += 1
                continue
            elif(item[i][0] == 'word'):
                print(item[i][1])
                print()
                i += 1
                continue
            elif(item[i][0] == 'access_group'):
                print('access_group')
                for sub_item in read_access_group(item[i]):
                    print(sub_item)
                print()
                i += 1
                continue
            scan(item[i])
        i += 1
scan(parsed)

def read_assignment(code):
    assign = code[1]
    variable = assign[0][1]
    value = assign[1]
    if len(value) == 1:
        value = value[0]
    variable_type = variable_types[value[0]]
    return variable, value, variable_type
