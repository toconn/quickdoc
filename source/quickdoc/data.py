from dataclasses import dataclass, field

from jinja2 import Template

from quickdoc.commands import Notice, Parameters, Set
from shared.utils.files import directory, file_name, exists, is_directory, is_absolute_path, join_path, is_file
from shared.utils.strings import not_empty
from variables import add_variable


@dataclass
class DocDefinition:
	name: str
	path: str
	commands: list = field(default_factory = lambda: [])
	notices: list = field(default_factory = lambda: [])
	parameters: list = field(default_factory = lambda: [])
	settings: list = field(default_factory = lambda: [])
	settings_by_name: dict = field(default_factory = lambda: {})

	def __repr__(self):

		return ("DocDefinition {\n\n"
				"\tname       = " + (self.name if (self.name is not None) else "[None]") + "\n"
				"\tpath       = " + (self.path if (self.path is not None) else "[None]") + "\n"
				"\tcommands   = [" + self._to_list_string(self.commands) + "\t]\n\n"
				"\tnotices    = [" + self._to_list_string(self.notices) + "\t]\n"
				"\tparameters = [" + self._to_list_string(self.parameters) + "\t]\n"
				"\tsettings   = [" + self._to_list_string(self.settings) + "\t]\n")

	def add_command(self, command):

		if type(command) is Notice:
			self.notices.append(command)

		elif type(command) is Parameters:
			self.add_parameters(command)

		elif type(command) is Set:
			self.add_set(command)

		else:
			self.commands.append(command)

	def add_commands(self, commands):
		for command in commands:
			self.add_command(command)

	def add_parameters(self, command):
		for parameter in command.parameters:
			if parameter not in self.parameters:
				self.parameters.append(parameter)

	def add_set(self, command):
		self.settings.append(command)
		self.settings_by_name[command.name] = command

	def get_setting(self, name):
		return self.settings_by_name.get(name)

	def get_setting_value(self, name):
		return self.settings_by_name.get(name).value

	def has_parameters(self):
		return self.parameter_count() != 0

	def has_setting(self, name):
		return name in self.settings_by_name

	def missing_setting(self, name):
		return not self.has_setting(name)

	def parameter_count(self):
		return len(self.parameters)

	def prepend_command(self, command):
		self.commands.insert(0, command)

	def prepend_setting(self, setting):
		self.settings.insert(0, setting)
		self.settings_by_name[setting.name] = setting

	def prepend_settings(self, settings):
		for setting in settings:
			self.prepend_setting(setting)

	def remove_setting(self, name):

		for setting in self.settings:
			if setting.name == name:
				self.settings.remove(setting)

		if name in self.settings_by_name:
			del self.settings[name]

	def setting_names(self):
		return set(self.parameters) | set(self.settings_by_name.keys())

	def _update_set(self, command):
		self.settings_by_name[command.name].value = command.value

	def _to_list_string(self, commands):
		"""
		Creates a printable list on commands for __repr__.
		"""
		if commands:
			return '\n\t\t' + '\n\t\t'.join([str(command) for command in commands]) + '\n'
		return ''


@dataclass
class DocInstance:
	variables: dict
	source: str = ''
	target: str = ''
	target_directory: str = ''

	def expand(self, value):
		if type(value) == list:
			return [self._expand(item) for item in value]
		return self._expand(value)

	def get(self, value):
		return self.variables[value]

	def get_expanded(self, value):
		return self._expand(self.get(value))

	def set(self, name, value):
		# if is_date(name):
		# 	add_date_variable(name, value)
		# else:
		add_variable(self.variables, name, self._expand(value))

	def source_path(self, path):
		return self._expand_and_join(self.source, path)

	def target_exists(self):
		if not_empty(self.target):
			return exists(self.target_path(self.target))
		return exists(self.target_directory)

	def target_path(self, path):
		return self._expand_and_join(self.target_directory, path)

	def _expand(self, value):
		return Template(value).render(self.variables)

	def _expand_and_join(self, root, path):
		expanded = self._expand(path)
		if is_absolute_path(expanded):
			return expanded
		return join_path(root, expanded)


