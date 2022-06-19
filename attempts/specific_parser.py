if(type(parsed[0]) != list):
    parsed = [parsed]

for item in parsed:
    if(
        item[0] == 'if' and 
        item[1][0][0] == 'operation' and 
        item[1][1][0] == 'assign' and 
        item[1][0][2] == item[1][1][1]
    ):
        direction_dictionary = {
            '>': 'smaller',
            '<': 'bigger',
            '>=': 'smaller',
            '<=': 'bigger',
        }
        limit_direction = direction_dictionary[item[1][0][1]]
        variable, limit = item[1][1][1]

        print(f'make {variable} always {limit_direction} than {limit}')