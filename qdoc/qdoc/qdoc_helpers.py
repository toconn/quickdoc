def read_file_to_dict (file_path):
    
    with open(file_path) as file_handle:    # 'r' is optional
        file_lines = [line.rstrip('\n') for line in file_handle.readlines()]
        
    content_dict = {}

    for line in file_lines:

        line = line.strip()
        
        if '\t' in line:
            name, value = line.split('\t', 1) 
            content_dict[name.strip()] = value.strip()
    
    return content_dict
