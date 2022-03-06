#!/usr/bin/env python3

from quickdoc.domain import *
from quickdoc.commands import Print


def write_quick_doc(definition, doc, verbose=False, dry_run=False):

	print('Creating...')
	print()

	if not dry_run:

		create_path(doc.target_directory)
		change_directory(doc.target_directory)

	for command in definition.commands:

		if (verbose or dry_run) and not_print(command):
			print(command.description(doc))
			print()

		if not dry_run or is_print(command):
			command.apply(doc)

	print()
