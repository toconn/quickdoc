from dataclasses import dataclass, field
from subprocess import run
from typing import Callable

from shared.utils.files import change_directory, is_file, copy, join_path, read_all_recursively, create_path, write_empty_file, \
    is_directory, write_text, read_text
from shared.utils.strings import join


# Utils ####################################################

def directory_or_file(path):
    return 'file' if is_file(path) else 'directory'


# Commands #################################################

@dataclass
class ChangeDirectory:
    directory: str

    def apply(self, doc):
        change_directory(self._directory(doc))

    def description(self, doc):
        return f'Change directory to {self._directory(doc)}'

    def _directory(self, doc):
        return doc.target_path(self.directory)


@dataclass
class Copy:
    source: str
    target: str
    check: Callable = None

    def apply(self, doc):
        source = self._source(doc)
        target = self._target(doc)
        if is_file(source):
            self._copy(source, target)
        else:
            self._copy_directory(source, target)

    def description(self, doc):
        source = self._source(doc)
        target = self._target(doc)
        return (f'Copy {directory_or_file(source)}:\n\n'
                f'    {source} To {target}')

    def _copy(self, source, target):
        if self.check(target):
            copy(source, target)

    def _copy_directory(self, source, target):
        for file in sorted(read_all_recursively(source)):
            source_path = join_path(source, file)
            target_path = join_path(target, file)

            if self.check(target_path):
                copy(source_path, target_path)

    def _source(self, doc):
        return doc.source_path(self.source)

    def _target(self, doc):
        return doc.target_path(self.target)


@dataclass
class CreateDirectory:
    target: str
    check: Callable = None

    def apply(self, doc):
        target = self._target(doc)
        if self.check(target):
            create_path(self._target(doc))

    def description(self, doc):
        return (f'Create Directory:\n\n'
                f'    {self._target(doc)}')

    def _target(self, doc):
        return doc.target_path(self.target)


@dataclass
class CreateFile:
    target: str
    check: Callable = None

    def apply(self, doc):
        target = self._target(doc)
        if self.check(target):
            write_empty_file(target)

    def description(self, doc):
        return (f'Create File:\n\n'
                f'    {self._target(doc)}')

    def _target(self, doc):
        return doc.target_path(self.target)


@dataclass
class Generate:
    source: str
    target: str
    check: Callable = None

    def apply(self, doc):
        source = self._source(doc)
        target = self._target(doc)

        if is_file(source):
            self._generate(doc, source, target)
        else:
            self._copy_directory(doc, source, target)

    def description(self, doc):
        source = self._source(doc)
        target = self._target(doc)
        return (f'Generate {directory_or_file(source)}:\n\n'
                f'    {source} -> {target}')

    def _copy_directory(self, doc, source, target):
        for file in sorted(read_all_recursively(source)):
            source_path = join_path(source, file)
            target_path = join_path(target, file)

            if self.check(target_path):
                if is_directory(source_path):
                    create_path(target_path)
                else:
                    self._generate(doc, source_path, target_path)

    def _generate(self, doc, source, target):
        if self.check(self.target):
            write_text(
                target,
                doc.expand(read_text(source)))

    def _source(self, doc):
        return doc.source_path(self.source)

    def _target(self, doc):
        return doc.target_path(self.target)


@dataclass
class Notice:
    message: str

    def apply(self, doc):
        print(self.message)

    def description(self, doc):
        return None


@dataclass
class Parameters:
    parameters: list = field(default_factory=lambda: [])

    def apply(self, doc):
        pass

    def description(self, doc):
        return None


@dataclass
class Print:
    message: str

    def apply(self, doc):
        print(doc.expand(self.message))

    def description(self, doc):
        return None


@dataclass
class Run:
    command: str
    parameters: list = field(default_factory=lambda: [])

    def apply(self, doc):
        if self.parameters:
            run(self._command(doc), self._parameters(doc))
        else:
            run(self._command(doc))

    def description(self, doc):
        if self.parameters:
            return "Run {self._command(doc)} {' '.join(self._parameters(doc))}"
        return "Run {self._command(doc)}"

    def _command(self, doc):
        return doc.expand(self.command)

    def _parameters(self, doc):
        return doc.expand(self.parameters)


@dataclass
class Set:
    name: str
    value: str

    def apply(self, doc):
        # print(f'Set:   {self.name:<20} : {self.value}')
        doc.set(self.name, doc.expand(self.value))

    def description(self, doc):
        return f'Set {self.name} to {self.value}  ->  {doc.expand(self.value)}'


@dataclass
class Shell:
    command: str
    parameters: list = field(default_factory=lambda: [])

    def apply(self, doc):
        run(self._to_command(doc), shell=True)

    def description(self, doc):
        return f"Shell {self._to_command(doc)}"

    def _command(self, doc):
        return doc.expand(self.command)

    def _parameters(self, doc):
        return doc.expand(self.parameters)

    def _to_command(self, doc):
        if not self.parameters:
            return self._command(doc)
        return self._command(doc) + ' "' + '" "'.join(self._parameters(doc)) + '"'


ACTION_COMMANDS = [Copy, CreateDirectory, CreateFile, Generate]
