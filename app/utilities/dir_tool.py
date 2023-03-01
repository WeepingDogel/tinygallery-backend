from pathlib import Path

from .. import config


def get_files_url_as_dict(dir_uuid: str):
    post_dir_object = Path(config.IMAGE_DIR).joinpath(dir_uuid)
    image_files_list_object: list[Path] = list(post_dir_object.glob("*.*"))
    original_cover_file_obj: Path = list(post_dir_object.joinpath("cover").glob("*.*"))[0]
    compressed_cover_file_obj: Path = list(post_dir_object.joinpath("compressedCover").glob("*.*"))[0]

    # Convert each Path object in old list to string type for new list.
    image_files_path_list: list[str] = []
    for o in image_files_list_object:
        image_files_path_list.append(config.STATIC_RESOURCE_SERVER_URL + str(o.relative_to(config.IMAGE_DIR)))
    original_cover_file_path: str = config.STATIC_RESOURCE_SERVER_URL + str(original_cover_file_obj.relative_to(config.IMAGE_DIR))
    compressed_cover_file_path: str = config.STATIC_RESOURCE_SERVER_URL + str(compressed_cover_file_obj.relative_to(config.IMAGE_DIR))

    dict_for_return = {
        "image_files_url": image_files_path_list,
        "original_cover_url": original_cover_file_path,
        "compressed_cover_url": compressed_cover_file_path
    }
    return dict_for_return
