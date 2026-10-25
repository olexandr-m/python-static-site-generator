import os
import shutil


def clean_and_copy_directory(source_dir: str, dest_dir: str) -> None:
    if os.path.exists(dest_dir):
        print(f"Cleaning destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    os.mkdir(dest_dir)
    print(f"Created empty directory: {dest_dir}")

    _copy_recursive(source_dir, dest_dir)


def _copy_recursive(src: str, dest: str) -> None:
    items = os.listdir(src)

    for item in items:
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            _copy_recursive(src_path, dest_path)
