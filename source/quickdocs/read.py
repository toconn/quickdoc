#!/usr/bin/env python3

from quickdocs.data import QuickDoc, QuickDocs
from shared.utils.files import *
from shared.utils.findfile import FindFile
from shared.errors import *

from settings import QUICKDOC_EXTENSION


def find_quick_doc_directories(settings):
    ''' Find the location of the definitions directory
        Raises InvalidConfiguration if not found.
    '''

    finder = FindFile(settings.os)
    directories = finder.find_all(settings.base_directory)
    
    if directories is None:
        raise InvalidConfiguration ("Configuration Error: Could not locate " + settings.base_directory + " settings directory.") 
    
    return [ join (directory, settings.base_directory) for directory in directories ]

def normalize_doc_name(name):
	return name.lower()

def read_quick_doc_file_names(directory):
	return read_files(directory, '*.' + QUICKDOC_EXTENSION)

def read_directory_quick_docs(directory):
	return [to_quick_doc(directory, file) for file in read_quick_doc_file_names(directory)]

def read_quick_docs(settings):

	docs = []

	for directory in find_quick_doc_directories(settings):
		docs.extend(read_directory_quick_docs(directory))

	return QuickDocs(docs)

def to_quick_doc(directory, file):
	return QuickDoc(normalize_doc_name(base_name(file)), join(directory, file))

