#!/usr/bin/env python3

from itertools import zip_longest
from quickdoc.commands import Set
from variables import *



def request_select_document(documents):
    pass

def request_user_parameter(name):
    return Set(
        name,
        input(name + ': '))

def request_user_parameters(parameters):
    data = [request_user_parameter(name) for name in parameters]
    print()
    return data

def show_definition(definition):

    print('Definition:')
    print()
    print('  Name:         ', definition.name)
    print('  Path:         ', definition.path)
    print()
    print('  Source:       ', definition.get_setting(SOURCE))
    print('  Target:       ', definition.get_setting(TARGET))
    print()

    for name in sorted(definition.setting_names()):
        if name not in [SOURCE, TARGET]:
            print(f'  {name + ":":12}  ', definition.get_setting(name))
    print()

    for setting in definition.settings:
        print(f'  S: {setting.name + ":":20}  ', setting.value)
    print()

    for command in definition.commands:
        print('  C:', command)
    print()

def show_instance(definition, instance):

    print('Definition / Instance:')
    print()
    print('  Name:              ', definition.name)
    print('  Path:              ', definition.path)
    print()
    print('  Source:            ', instance.source)
    print('  Target:            ', instance.target)
    print('  Target Directory:  ', instance.target_directory)
    print()
    print('  S Source:          ', instance.get(SOURCE))
    print('  S Target:          ', instance.get(TARGET))
    print()

    for setting in definition.settings:
        print(f'  S: {setting.name + ":":20}  ', setting.value)
    print()

    for command in definition.commands:
        print('  C:', command)
    print()

def show_notices(definition):
    if definition.notices:
        for notice in definition.notices:
            notice.apply(None)
        print()

