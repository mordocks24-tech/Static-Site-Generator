import os, shutil

def copy_to(source, destination):
    s_path = os.path.abspath(source)
    d_path = os.path.abspath(destination)
    
    if not os.path.exists(destination):
        os.mkdir(d_path)
        


    dir_items = os.listdir(s_path)
    
    for item in dir_items:
        i_path = os.path.join(s_path, item)
        if os.path.isfile(i_path):
            shutil.copy(i_path, os.path.join(d_path, item))
        else:
            copy_to(i_path, os.path.join(d_path, item))
