# Assignment 7 - SimpleLanguage2
# Preston Tighe
# CSE 3342
# 9-19-16

from keyword import iskeyword
import json
import re

print('REPL: enter statement | expression | bye | mem')
var_dict = {}


def is_valid_variable_name(name):
    return name.isidentifier() and not iskeyword(name)


def is_int(s):
    try:
        temp = int(s)
        return True
    except:
        return False


def is_valid_var(s):
    return s in var_dict


def eval_statement(instr):
    tokens = instr.split('=')
    tokens = [tok.strip() for tok in tokens]

    # Parse RHS
    if len(tokens) == 2:  # assignment

        # Check valid variable name
        if is_valid_variable_name(tokens[0]):

            # Assigns value in dict
            var_dict[tokens[0]] = parse_rhs(tokens[1])
            return var_dict[tokens[0]]
        else:
            raise Exception('Invalid variable name: `' + tokens[0] + '`'
                            )
    elif len(tokens) == 1:

        # inline arithmetic
        if tokens[0]:
            return parse_rhs(tokens[0])
        else:
            raise Exception('Empty statement.')
    else:
        raise Exception('Invalid statement `' + instr + '`')


def parse_val(token):
    if is_int(token):
        return int(token)
    elif is_valid_variable_name(token):
        if token in var_dict and var_dict[token]:
            return var_dict[token]
        else:
            raise Exception('`' + token + '` not declared or defined.')
    else:
        raise Exception('Invalid value: `' + token + '`')


def parse_rhs(rhs):
    rhs = rhs.replace(' ', '')

    # Check if valid RHS
    test = re.match('^\-*(\d+|[A-Za-z]\w*)(?:([/+\-*])\-*(\d+|[A-Za-z]\w*))*$', rhs)
    if not test:
        raise Exception('Invalid statement: `' + rhs + '`')

    # Split RHS into a list
    groups = list(re.findall("\-*(\d+|[A-Za-z]\w*|[/+\-*])", rhs))

    # RHS only 1 item
    if len(groups) == 1:
        return parse_val(groups[0])

    # Multiply & Divide
    i = 1
    while i < len(groups) - 1:
        if groups[i] == '*' or groups[i] == '/':

            if groups[i] == '*':
                groups[i - 1] = parse_val(groups[i - 1]) * parse_val(groups[i + 1])

            if groups[i] == '/':
                groups[i - 1] = parse_val(groups[i - 1]) / parse_val(groups[i + 1])

            groups = groups[:i] + groups[i + 2:]
        else:
            i += 1

    # Add & Subtract
    i = 1
    while i < len(groups) - 1:
        if groups[i] == '+' or groups[i] == '-':

            if groups[i] == '+':
                groups[i - 1] = parse_val(groups[i - 1]) + parse_val(groups[i + 1])

            if groups[i] == '-':
                groups[i - 1] = parse_val(groups[i - 1]) - parse_val(groups[i + 1])

            groups = groups[:i] + groups[i + 2:]
        else:
            i += 1

    return groups[0]


def memory_json():
    return json.dumps(var_dict)


while True:
    try:
        instr = input('%')
        if instr == 'bye':
            print('The program will exit now.')
            break
        elif instr == 'mem':
            print(memory_json())
        else:
            print(eval_statement(instr))
    except Exception as error:
        print('Error: ' + str(error))