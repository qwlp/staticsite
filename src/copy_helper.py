import os
import shutil


def copy_to_public():
    # delete public and create new one
    if os.path.exists("../public/"):
        shutil.rmtree("../public/")
    os.makedirs("./public", exist_ok=True)
    copy("./static/", "./public/")


def copy(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy(from_path, dest_path)
