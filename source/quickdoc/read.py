#!/usr/bin/env python3

from settings import QUICKDOC_EXTENSION
from quickdoc.domain import *
from quickdoc.commands import *
from shared.errors import *


@dataclass
class CommandDetails:
    name: str
    remainder: str
    _parameters: list = None

    @property
    def parameters(self):
        if not self._parameters:
            self._parameters = to_words(self.remainder)
        return self._parameters


# Utils ####################################################

WORD_PATTERN = r'((?<=\")(\\[^\n]|[^\n])+(?=\"))|((\\.|[^\"\s])(\\.|[^ \t\n])+)'
NAME_PATTERN = r'^\w\w*'


def first(items):
    if len(items) > 0:
        return items[0]
    return None


def second(items):
    if len(items) > 1:
        return items[1]
    return None


def remainder(items):
    if len(items) > 1:
        return items[1:]
    return []


def at_least_one(items):
    return len(items) >= 1


def is_one(items):
    return len(items) == 1


def is_two(items):
    return len(items) == 2


def to_quick_doc_file_name(name):
    return name + '.' + QUICKDOC_EXTENSION


def to_words(value):
    return find_all(value, WORD_PATTERN)


def validate_count(items, count):

    if count == 0:
        raise InvalidConfiguration(message=f'Missing parameters. Expected {count}.')

    if len(items) != count:
        raise InvalidConfiguration(message=f'Has the wrong number of parameters. Expected {count}. Found {len(items)}.')


def validate_count_range(items, minimum, maximum):

    count = len(items)

    if count == 0:
        raise InvalidConfiguration(message=f'Missing parameters. Expected {count}.')

    if count < minimum:
        raise InvalidConfiguration(message=f'Has too few parameters. '
                                           f'Expected {minimum} to {maximum}. Found {len(items)}.')

    if count > maximum:
        raise InvalidConfiguration(message=f'Has too many parameters. '
                                           f'Expected {minimum} to {maximum}. Found {len(items)}.')


def validate_one(items):
    validate_count(items, 1)


def validate_one_or_two(items):
    validate_count_range(items, 1, 2)


def validate_two(items):
    validate_count(items, 2)


# Command Factories ########################################

def new_change_directory(details):
    validate_one(details.parameters)
    return ChangeDirectory(first(details.parameters))


def new_copy(details):
    parameters = details.parameters
    validate_one_or_two(parameters)
    if is_one(parameters):
        return Copy(first(parameters), first(parameters))
    return Copy(first(parameters), second(parameters))


def new_create_directory(details):
    validate_one(details.parameters)
    return CreateDirectory(first(details.parameters))


def new_create_file(details):
    parameters = details.parameters
    validate_one(parameters)
    return CreateFile(first(parameters))


def new_generate(details):
    parameters = details.parameters
    validate_one_or_two(parameters)
    if is_one(parameters):
        return Generate(first(parameters), first(parameters))
    return Generate(first(parameters), second(parameters))


def new_notice(details):
    return Notice(' '.join(details.parameters))


def new_parameters(details):
    return Parameters([item.removesuffix(',') for item in details.parameters])


def new_print(details):
    return Print(' '.join(details.parameters))


def new_run(details):
    return Run(details.parameters)


def new_set(details):
    parameters = details.parameters
    validate_two(parameters)
    return Set(first(parameters), second(parameters))


def new_shell(details):
    return Shell(first(details.parameters), remainder(details.parameters))


# Main #####################################################

COMMAND_CHANGE_DIRECTORY = 'cd'
COMMAND_COPY_1 = 'copy'
COMMAND_COPY_2 = 'cp'
COMMAND_CREATE_DIRECTORY_1 = 'dir'
COMMAND_CREATE_DIRECTORY_2 = 'directory'
COMMAND_CREATE_DIRECTORY_3 = 'mkdir'
COMMAND_CREATE_FILE_1 = 'file'
COMMAND_CREATE_FILE_2 = 'touch'
COMMAND_GENERATE_1 = 'gen'
COMMAND_GENERATE_2 = 'generate'
COMMAND_NOTICE = 'notice'
COMMAND_PARAMETERS_1 = 'params'
COMMAND_PARAMETERS_2 = 'parameters'
COMMAND_PRINT = 'print'
COMMAND_RUN = 'run'
COMMAND_SET = 'set'
COMMAND_SHELL_1 = 'shell'
COMMAND_SHELL_2 = 'bash'
COMMAND_SHELL_3 = 'cmd'

COMMANDS = {
    COMMAND_CHANGE_DIRECTORY: new_change_directory,
    COMMAND_COPY_1: new_copy,
    COMMAND_COPY_2: new_copy,
    COMMAND_CREATE_DIRECTORY_1: new_create_directory,
    COMMAND_CREATE_DIRECTORY_2: new_create_directory,
    COMMAND_CREATE_DIRECTORY_3: new_create_directory,
    COMMAND_CREATE_FILE_1: new_create_file,
    COMMAND_CREATE_FILE_2: new_create_file,
    COMMAND_GENERATE_1: new_generate,
    COMMAND_GENERATE_2: new_generate,
    COMMAND_NOTICE: new_notice,
    COMMAND_PARAMETERS_1: new_parameters,
    COMMAND_PARAMETERS_2: new_parameters,
    COMMAND_PRINT: new_print,
    COMMAND_RUN: new_run,
    COMMAND_SET: new_set,
    COMMAND_SHELL_1: new_shell,
    COMMAND_SHELL_2: new_shell,
    COMMAND_SHELL_3: new_shell,
}


def get_new_command_function(details):
    return COMMANDS[details.name]


def is_command(details):
    return details.name in COMMANDS


def is_ignored(line):
    return is_comment(line) or is_blank(line)


def is_name(value):
    return not_empty(find(value, NAME_PATTERN))


def is_shorter(new, original):
    return len(new) < len(original)


def is_variable(definition):
    if is_one(definition.parameters):
        return is_name(definition.name)
    return False


def new_command(details):
    return get_new_command_function(details)(details)


def not_ignored(line):
    return not is_ignored(line)


def read_quick_doc_definition(doc):
    definition = DocDefinition(
        doc.name,
        absolute_path(doc.path))

    definition.add_commands(
        read_to_commands(doc.path))

    return definition


def read_to_command(commands, line):
    details = to_command_details(line)

    if is_blank(details.remainder):
        raise InvalidConfiguration(message="Not enough parameters")

    if is_command(details):
        commands.append(new_command(details))

    elif is_variable(details):
        commands.append(
            new_set(CommandDetails('set', line)))

    else:
        raise InvalidConfiguration(message="Unknown setting.")


def read_to_commands(path):
    commands = []
    counter = 1

    for line in read_lines(path):

        try:

            if not_ignored(line):
                read_to_command(commands, line)

        except InvalidConfiguration as error:

            print('Invalid Entry:')
            print()
            print('  Line', str(counter))
            print('  ' + line.strip())
            print()
            print('  ' + error.message)
            print()

        counter += 1

    return commands


def to_command_details(line):
    line = line.strip()
    name = to_name(line)

    return CommandDetails(
        name=name,
        remainder=to_parameters_part(line, name))


def to_parameters_part(line, name):
    if len(line) > len(name) + 1:
        return line[len(name) + 1:]

    return ''


def to_name(line):
    return find(line, NAME_PATTERN)
