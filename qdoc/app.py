from ua_core.errors.errors import ItemAlreadyExists, ItemNotFound, UserRequestExit
from ua_core.utils import fileutils

class App:
    
    def __init__(self, qdocs, ua_os, list_picker):
        
        self._qdocs = qdocs
        self._ua_os = ua_os
        self._list_picker = list_picker

    def main (self, parsed_params):
        
        qdoc = None
        
        if self._qdocs.has_duplicates():
            
            print ("Duplicates definitions found:")
            
            for name in self._qdocs.duplicates_dict():
                print ("    " + name + ":")
                for qdoc_file in self._qdocs.duplicates_dict()[name]:
                    print ("        " + qdoc_file.path)
        
            print ()
        
        if parsed_params.list_docs_flag:
            
            print ('Available QDocs:')
            
            for def_name in self._qdocs.def_names() :
                print ('    ' + def_name)
                
            print()
        
        if parsed_params.qdoc_name:
            
            # Retrieve qdoc:
        
            try:
                
                qdoc = self._qdocs.retrieve_qdoc (parsed_params.qdoc_name)
                
            except ItemNotFound:
                
                matching_qdoc_names = self._qdocs.retrieve_matching_qdoc_names (parsed_params.qdoc_name)
                
                if len (matching_qdoc_names) == 1:
                    
                    qdoc_name = matching_qdoc_names[0]
                    qdoc = self._qdocs.retrieve_qdoc (qdoc_name)
                    
                elif len (matching_qdoc_names) > 0:
                    
                    try:

                        print ("Select one of these:")
                        print ()
                        
                        index = self._list_picker.pick_item (matching_qdoc_names)
                        
                        print ()
                        
                        qdoc_name = matching_qdoc_names[index]
                        qdoc = self._qdocs.retrieve_qdoc (qdoc_name)
                        
                        print ("Running '" + qdoc_name + "'...")
                        print()

                    except UserRequestExit:
                        
                        pass    # Handled by qdoc = None
                    
                else:
                    
                    print ("'" + parsed_params.qdoc_name + "' does not exist.")
        
        if qdoc:
               
            # Show User Notes:

            if parsed_params.new_doc_flag:
                
                user_notes = qdoc.user_notes()
            
                if user_notes:
                    print (user_notes)
                    print ()
            
            qdoc.set_params (parsed_params.parameters)
            
            if parsed_params.show_tags_flag:
                
                tag_dict = qdoc.tag_dict() 
                tags = [ tag for tag in tag_dict.keys() ]
                tags.sort()
                
                print ("Tags:")
                for tag in tags:
                    print ("   " + tag.ljust (20) + ": " + tag_dict[tag])
                
                print()
            
            # Create document:
            
            if parsed_params.new_doc_flag:
                
                try:
                    
                    if not parsed_params.show_tags_flag:
                        print ("Dir:  " + qdoc.target_file_dir())
                        print ("Name: " + qdoc.target_file_name())
                    
                    qdoc.create()
                    print ('Document created: \'' + qdoc.target_file_path() + '\'.')
                    
                except ItemAlreadyExists as e:
    
                    print ('File already exists: \'' + e.messages_as_string() + '\'.')
                    print ()
            
            # Open document if exists:
            
            target_file_path = qdoc.target_file_path()
            
            if target_file_path:
                
                if not parsed_params.new_doc_flag and not fileutils.is_file_exists (target_file_path):
                    
                    # If we are just trying to open the file (not create it) and a perfect match doesn't exist
                    #   find the most recent document.
                    
                    file_dir = fileutils.file_dir(target_file_path)
                    
                    if fileutils.is_dir_exists(file_dir):
                        
                        file_paths = fileutils.read_dir_file_paths (file_dir, "*")
                        file_paths.sort()
                        
                        if file_paths:
                            target_file_path = file_paths[-1]
                    
                
                if fileutils.is_file_exists (target_file_path):
                    
                    self._ua_os.open_document(target_file_path)
                    
                    print ("Done.")
                            
                else:
                    print ("Can not find '" + target_file_path + "'")
 
        print ()
