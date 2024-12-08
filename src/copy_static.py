import os
import shutil

def copy_static_resources(static_dir, public_dir):
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    print("Copying static resources to public directory...")
    copy_dir_contents(static_dir, public_dir)

def copy_dir_contents(source, destination):
    if not os.path.exists(source):
        raise Exception("Invalid source path")
    
    if not os.path.exists(destination):
        os.mkdir(destination)

    for resource in os.listdir(path=source):
        source_path = os.path.join(source, resource)
        dest_path = os.path.join(destination, resource)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            copy_dir_contents(source_path, dest_path)