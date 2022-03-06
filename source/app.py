from shared.errors import *
from shared.utils.files import *
from shared.utils.first import *
from quickdocs.read import read_quick_docs
from quickdoc.domain import *
from quickdoc.read import read_quick_doc_definition
from quickdoc.write import write_quick_doc
from ui.quickdoc import *
from typing import Callable


def create_document(definition, parameters):

    show_notices(definition)

    user_parameters = get_user_parameters(definition, parameters.parameters)
    def_with_defaults = apply_defaults(definition, user_parameters, None)
    instance = new_quick_doc_instance(def_with_defaults)

    # show_instance(def_with_defaults, instance)

    # write_quick_doc(def_with_defaults, instance, verbose = parameters.verbose)
    write_quick_doc(def_with_defaults, instance, verbose = True)

    print('Document created: \'' + instance.target + '\'.')

    return instance


def find_closest_matching_file(path):

    directory = file_dir(path)
    
    if is_dir_exists(directory):
        
        file_paths = sorted (read_dir_file_paths (directory, "*"))  # Sorted so we pick the first appropriate match.
        
        if file_paths:
            return file_paths[-1]

    return None


def get_definition(definitions, name):
    if name:
        return read_quick_doc_definition(definitions.get(name))
    return None


def get_user_parameters(definition, parameters):
    provided = get_provided_parameters(definition, parameters)
    user = request_user_parameters(
                    get_missing_parameters(definition, parameters))
    return provided + user


def has_exact_match(matches):
    return len(matches) == 1


def has_no_matches(matches):
    return len(matches) == 0


def is_show_target_files(parameters):
    return parameters.new_doc and not parameters.show_tags


def open_doc(path: str, new_doc: bool, open: Callable):
        
    if new_doc and not exists (path):
        path = find_closest_matching_file (path)

    if exists(path):
        open(path)
        print("Done.")
    else:
        print("Can not find '" + path + "'")


def request_choose_document(picker, names):

    print("Select one of these:")
    print()
    
    index = picker.pick_item (names)
    name = names[index]
    
    print()
    print("Running '" + name + "'...")
    print()
  
    return name


def retrieve_qdoc(qdocs, name):
            
    # Retrieve qdoc:

    if qdocs.has(name):
        return qdocs.retrieve_qdoc(name)

    return retrieve_match(qdocs, name)


def retrieve_match(qdocs, name):

    matches = qdocs.retrieve_matches(name)

    if has_no_match(matches):
        print(f"'{name}' does not exist.")
        return None

    if has_exact_match(matches):
        return qdocs.retrieve_qdoc (matches[0])
        
    # Multiple Matches:
    return qdocs.retrieve_qdoc (
            request_choose_document(self._list_picker, matching))


def show_quick_docs(docs):
    print('Available Quick Docs:')
    for doc in docs :
        print('    ' + name)
    print()


def show_duplicates(definitions):

    if not definitions.duplicates.no_duplicates():
        return

    print('Duplicates definitions found:')

    for duplicate in definitions.duplicates.duplicates():

        first = IsFirst()

        for doc in duplicate.values():
            if first.is_first():
                print('    ' + doc.name + ':')
            print('        ' + doc.directory)

    print()    


def show_file_exists(qdoc):
    print(f'File already exists: \'{qdoc.target_file_path()}\'.')
    print()


def main(settings, parameters, os):

    definitions = read_quick_docs(settings)

    show_duplicates(definitions)
    
    if parameters.list_docs:
        show_quick_docs(definitions)

    definition = get_definition(definitions, parameters.name)
    
    if definition:

        show_definition(definition)

        # if definition.exists():
        #     show_file_exists(definition)
        # else:
        #   create_document(definition, parameters)
        
        instance = create_document(definition, parameters)

        if instance.target_exists():
            open_doc(instance.target, parameters.new_doc, os.open_document)
 
        print()

