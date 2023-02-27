from pathlib import Path
import typing


def create_needed_dirs(dir_names: list[str]) -> bool:
    project_dir_object = Path(".")

    full_paths_list: list[str] = []
    for x in dir_names:
        full_path = project_dir_object.joinpath(str(x))
        full_paths_list.append(full_path)

    for x in full_paths_list:
        print(x)
        # with open(str(x)) as f:
        #     pass

    return True


create_needed_dirs(["a/d", "b", "c"])
