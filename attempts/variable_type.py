from code_tokenizer import *

# code = """
# posicao.Trigger == "DEACTIVATION" || posicao.Trigger == "POWER_LOSS"
# """

code = """
my_list = [1, 2, 3, 4, 5]
min = my_list[0]
for(i = 1;i < my_list.length; i++) {
    if(my_list[i] < min) {
        min = my_list[i]
    }
}
console.log(min)
"""

print(color_by_char_type(code))

parsed = math_layer(code)

variable_types = {
    'number': 'number',
    'string': 'string',
    'array_define': 'array',
    'dictionary_define': 'dictionary',
}
variables = {}
def get_value_type(value):
    if(value[0] in variable_types):
        var_type = variable_types[value[0]]
        if(var_type == 'array'):
            return ['array', get_value_type(value[1][0])]
        else:
            return [var_type]
    elif(value[0] == 'word'):
        child_type = variables[value[1]]
        for index in range(2,len(value)):
            if(value[index][0] == 'array_call'):
                child_type = child_type[1]
        return child_type
    else:
        return ['unknown']

def scan(data):
    if(type(data) == list and len(data) > 0):
        if(data[0] == 'assign'):
            variable_name = data[1][0][1]
            variable_value = data[1][1]
            variable_type = get_value_type(variable_value)
            variables[variable_name] = variable_type
            print(variable_name)
            print(variable_type)
            print(variable_value)
            print()
            return
        for item in data:
            scan(item)
scan(parsed)
print(parsed)