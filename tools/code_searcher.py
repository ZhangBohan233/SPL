import os
import sys


EXTENSIONS = {'.txt', '.sp', '.py'}


def search_dir(target: str, dir_name: str, results: list):
    if os.path.isdir(dir_name):
        try:
            for file in os.listdir(dir_name):
                abs_path = os.path.join(dir_name, file)
                search_dir(target, abs_path, results)
        except PermissionError:
            pass
    else:
        search_in_file(target, dir_name, results)


def search_in_file(target: str, file_name: str, results: list):
    if "." in file_name:
        ind = file_name.rfind(".")
        if file_name[ind:] in EXTENSIONS:
            try:
                with open(file_name, "r") as f:
                    s = f.read()
                if target in s:
                    results.append(file_name)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) > 2:
        obj = argv[1]
        root_dir = argv[2]
        lst = []
        search_dir(obj, root_dir, lst)
        print(lst)
    else:
        print("Usage: TARGET DIR")
