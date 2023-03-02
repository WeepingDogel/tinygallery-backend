from pathlib import Path

from .. import config


def get_files_url_as_dict(dir_uuid: str) -> dict:
    post_dir_object = Path(config.POST_DIR).joinpath(dir_uuid)
    image_files_list_object: list[Path] = list(post_dir_object.glob("*.*"))
    original_cover_file_obj: Path = list(post_dir_object.joinpath("cover").glob("*.*"))[0]
    compressed_cover_file_obj: Path = list(post_dir_object.joinpath("compressedCover").glob("*.*"))[0]

    # Convert each Path object in old list to string type for new list.
    image_files_path_list: list[str] = []
    for o in image_files_list_object:
        image_files_path_list.append(config.STATIC_RESOURCE_SERVER_URL + str(o.relative_to(config.POST_DIR)))
    original_cover_file_path: str = config.STATIC_RESOURCE_SERVER_URL + str(
        original_cover_file_obj.relative_to(config.POST_DIR))
    compressed_cover_file_path: str = config.STATIC_RESOURCE_SERVER_URL + str(
        compressed_cover_file_obj.relative_to(config.POST_DIR))

    dict_for_return = {
        "image_files_url": image_files_path_list,
        "original_cover_url": original_cover_file_path,
        "compressed_cover_url": compressed_cover_file_path
    }
    return dict_for_return


def get_cover_file_url(dir_uuid: str) -> str:
    post_dir_object = Path(config.POST_DIR).joinpath(dir_uuid)
    compressed_cover_file_obj: Path = list(post_dir_object.joinpath("compressedCover").glob("*.*"))[0]
    compressed_cover_file_path: str = config.STATIC_RESOURCE_SERVER_URL + str(
        compressed_cover_file_obj.relative_to(config.POST_DIR))

    return compressed_cover_file_path


def create_all_project_dir():
    post_path_obj = Path(config.POST_DIR)
    avatar_path = Path(config.AVATAR_DIR)
    database_dir = Path("./database")
    background_dir = Path(config.BACKGROUND_DIR)

    post_path_obj.mkdir(parents=True, exist_ok=True)
    avatar_path.mkdir(parents=True, exist_ok=True)
    database_dir.mkdir(exist_ok=True)
    background_dir.mkdir(exist_ok=True)
