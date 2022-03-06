#!/usr/bin/env python3

from copy import copy as create_copy

from quickdoc.commands import Generate, Print, Set, ACTION_COMMANDS
from quickdoc.data import DocDefinition, DocInstance
from shared.utils.strings import *
from shared.utils.files import *
from variables import *


# Utils ####################################################

def check_delete_if_exists(path):
    if is_file(path):
        delete_file(path)
    return True


def check_ignore_if_exists(path):
    return not exists(path)


# Doc ######################################################

def add_check(command, check):
    if is_action(command):
        new = create_copy(command)
        new.check = check
        return new

    return command


def add_checks(commands, check):
    return [add_check(command, check) for command in commands]


def apply_defaults(definition, user_settings, target_directory_override=None):

    new = copy_definition(definition)

    clear_source_and_target(new)
    apply_source_target(new, get_source_and_target(definition, target_directory_override))

    new.prepend_settings(user_settings)

    prepend_generate_if_no_create_commands(new)
    new.commands = add_checks(new.commands, check_ignore_if_exists)

    return new


def apply_source_target(definition, source_and_target):
    for key in sorted(source_and_target.keys()):
        definition.prepend_setting(Set(key, source_and_target[key]))


def clear_source_and_target(definition):
    for name in [SOURCE, TARGET]:
        definition.remove_setting(name)


def copy_definition(definition):

    return DocDefinition(
        definition.name,
        absolute_path(definition.path),
        list(definition.commands),
        list(definition.notices),
        list(definition.parameters),
        list(definition.settings))


def get_missing_parameters(definition, parameters):
    return definition.parameters[len(parameters):]


def get_provided_parameters(definition, parameters):
    if definition.has_parameters():
        return parameters[:definition.parameter_count()]
    return []


def get_source_and_target(definition, target_override):
    source = get_source(definition)
    return {
        SOURCE: source,
        TARGET: get_target(definition, source, target_override)}


def get_source(definition):

    if definition.missing_setting(SOURCE):
        return join_to_parent(definition.path, get_source_name(definition))

    return absolute_path_or_join_to_parent(
            definition.path,
            definition.get_setting_value(SOURCE))


def get_source_name(definition):
    name = ''
    for file in sorted(read_directory(directory(definition.path), strip_extension(definition.name) + '*')):
        if file != definition.name and (is_empty(name) or is_shorter(file, name)):
            name = file
    return name


def get_target(definition, source, override_directory):
    """
    Can't always get absolute path, especially if
    the target name contains {{ variables }}.
    """

    if not override_directory and definition.has_setting(TARGET):
        return definition.get_setting_value(TARGET)

    if override_directory:
        return get_target_actual(definition.get_setting_value(override_directory), source)

    return get_target_actual(getcwd(), source)


def get_target_actual(target_directory, source):
    """
    Returns the actual definition target directory for a definition.
    May not be an absolute path due to possible {{ variables }}
    """
    if is_directory(source):
        return join_path(target_directory, file_name(source))
    return target_directory


def get_target_instance(definition, instance):
    """
    Returns the absolute real path to the target.
    Used by the document instance as the target path.
    """
    target = instance.expand(definition.get_setting_value(TARGET))
    return absolute_path_or_join(current_directory(), target)


def get_target_instance_directory(instance):
    if is_file(instance.source):
        return directory(instance.target)
    else:
        return instance.target


def is_action(command):
    return type(command) in ACTION_COMMANDS


def is_date_variable(name):
    return name in [FIRST_DATE_1, FIRST_DATE_2]


def is_print(command):
    return type(command) is Print


def has_create_commands(definition):
    for command in definition.commands:
        if is_action(command):
            return True
    return False


def new_quick_doc_instance(definition):

    doc = DocInstance(default_variables())

    set_variables(definition, doc)
    set_variables(definition, doc)  # Apply twice to ensure variables evaluate.

    print()
    print('sauce', doc.get(SOURCE))
    print('target', doc.get(TARGET))
    print()

    doc.source = doc.get_expanded(SOURCE)
    doc.target = get_target_instance(definition, doc)
    doc.target_directory = get_target_instance_directory(doc)
    
    return doc

def no_create_commands(definition):
    return not has_create_commands(definition)


def not_print(command):
    return not is_print(command)


def prepend_generate_if_no_create_commands(definition):
    if no_create_commands(definition):
        definition.prepend_command(
                Generate(
                    definition.get_setting_value(SOURCE),
                    definition.get_setting_value(TARGET)))


def prepend_variables(definition, name_values):
    definition.commands = (
            [Set(name, value) for name, value in name_values.items()]
            + definition.commands)


def set_variables(definition, doc):
    for setting in definition.settings:
        setting.apply(doc)
