from ua.core.errors.errors import ItemExistsError
from ua.core.utils import fileutils

class App:
    
    def __init__(self, qdocs, ua_os):
        
        self._qdocs = qdocs
        self._ua_os = ua_os

    def main (self, parsed_params):
        
        if self._qdocs.has_duplicates():
            
            print ("Duplicates definitions found:")
            
            for name in self._qdocs.duplicates_dict():
                print ("    " + name + ":")
                for qdoc_file in self._qdocs.duplicates_dict()[name]:
                    print ("        " + qdoc_file.path)
        
            print ("")
        
        if parsed_params.list_docs_flag:
            
            print ('Available QDocs:')
            
            for def_name in self._qdocs.def_names() :
                print ('    ' + def_name)
                
            print()
        
        if parsed_params.qdoc_name:
        
            qdoc = self._qdocs.retrieve_qdoc (parsed_params.qdoc_name)
            
            # Show User Notes:

            if parsed_params.new_doc_flag:
                
                user_notes = qdoc.user_notes()
            
                if user_notes:
                    print (user_notes)
                    print ("")
            
            qdoc.set_params (parsed_params.parameters)
            
            if parsed_params.show_tags_flag:
                
                tag_dict = qdoc.tag_dict() 
                tags = [ tag for tag in tag_dict.keys() ]
                tags.sort()
                
                print ('Tags:')
                for tag in tags:
                    print ('    ' + tag.ljust (20) + ": " + tag_dict[tag])
                
                print('')
            
            # Create document:
            
            if parsed_params.new_doc_flag:
                
                try:
                    
                    if not parsed_params.show_tags_flag:
                        print ('Dir:  ' + qdoc.file_dir())
                        print ('Name: ' + qdoc.file_name())
                    
                    qdoc.create()
                    print ('Document created: \'' + qdoc.file_path() + '\'.')
                    
                except ItemExistsError as e:
    
                    print ('File already exists: \'' + e.messages_as_string() + '\'.')
                    print ()
            
            # Open document if exists:
            
            file_path = qdoc.file_path()
            
            if file_path:
                
                if not parsed_params.new_doc_flag and not fileutils.is_file_exists (file_path):
                    
                    # If we are just trying to open the file (not create it) and a perfect match doesn't exist
                    #   find the most recent document.
                    
                    file_dir = fileutils.file_dir(file_path)
                    
                    if fileutils.is_dir_exists(file_dir):
                        
                        file_paths = fileutils.read_dir_file_paths (file_dir, "*")
                        file_paths.sort()
                        
                        if file_paths:
                            file_path = file_paths[-1]
                    
                
                if fileutils.is_file_exists (file_path):
                    
                    self._ua_os.open_document(file_path)
                    
                    print ("Done.")
                            
                else:
                    print ('Can not find \'' + file_path + '\'')
 
            print ()

