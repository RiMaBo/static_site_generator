import os
import shutil


def copy_site_contents(src, dest, contents=None):
    if contents is None:
        contents = []
        if not os.path.exists(dest):
            os.mkdir(dest)
    
        if os.path.exists(src):
            for root, dirs, files in os.walk(src):
                for file in files:
                    filepath = os.path.join(root, file)
                    contents.append(filepath.replace(src, ""))
        else:
            raise ValueError("invalid source folder")
        
        copy_site_contents(src, dest, contents)
    else:
        filepath = contents.pop(0)
        split_filepath = filepath.split("/")
        current_filepath = ""
        for i in range(1, len(split_filepath)):
            current_filepath = os.path.join(current_filepath, split_filepath[i])
            if os.path.isfile(os.path.join(src, current_filepath)):
                shutil.copy(os.path.join(src, current_filepath), os.path.join(dest, current_filepath))
            else:
                if not os.path.exists(os.path.join(dest, current_filepath)):
                    os.mkdir(os.path.join(dest, current_filepath))
        
        if len(contents):
            copy_site_contents(src, dest, contents)

    # if not os.path.exists(dest):
    #     os.mkdir(dest)

    # for filename in os.listdir(src):
    #     from_path = os.path.join(src, filename)
    #     dest_path = os.path.join(dest, filename)
    #     print(f" * {from_path} -> {dest_path}")
    #     if os.path.isfile(from_path):
    #         shutil.copy(from_path, dest_path)
    #     else:
    #         copy_site_contents(from_path, dest_path)
