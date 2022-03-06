#!/usr/bin/env python3

from os.path import expandvars
from settings import *
from quickdocs.read import read_quick_docs
from quickdocs.data import QuickDoc
from quickdoc.read import read_quick_doc_definition
from quickdoc.write import *
from ui.quickdoc import *
from variables import *


TEST_DIRECTORY = expandvars('${USER_DEV_DIR}/Proj - QuickDoc/Source/Python/Current/QuickDoc/data')

print(TEST_DIRECTORY)
print()


# NAME = 'hello_world.qdef'
# NAME = 'hello_here.qdef'
# NAME = 'python.qdef'
NAME = 'python_app.qdef'
# NAME = 'test_all.qdef'

TEST_QDOC_PATH = absolute_path(join(TEST_DIRECTORY, NAME))
target_directory_override = None


change_directory('/Users/tadhg/Downloads/wip/quickdoc')


try:

	definitions = read_quick_docs(APP_SETTINGS)

	doc = QuickDoc(NAME, TEST_QDOC_PATH)
	definition = read_quick_doc_definition(doc)

	show_definition(definition)

	show_notices(definition)

	user_parameters = request_user_parameters(definition.parameters)
	updated_def = apply_defaults(definition, user_parameters, target_directory_override)

	show_definition(updated_def)

	doc = new_quick_doc_instance(updated_def)

	show_instance(updated_def, doc)

	write_quick_doc(updated_def, doc, verbose=True)

except KeyboardInterrupt:
	pass
