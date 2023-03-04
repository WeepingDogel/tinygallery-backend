from pathlib import Path
from fastapi import UploadFile
from PIL import Image
import shutil

from .. import config


def get_files_url_as_dict(dir_uuid: str) -> dict:
    post_dir_object = Path(config.POST_DIR).joinpath(dir_uuid)
    image_files_list_object: list[Path] = list(post_dir_object.glob("*.*"))
    original_cover_path_obj: Path = list(post_dir_object.joinpath("cover").glob("*.*"))[0]
    compressed_cover_file_obj: Path = list(post_dir_object.joinpath("compressedCover").glob("*.*"))[0]

    # Convert each Path object in old list to string type for new list.
    image_files_path_list: list[str] = []
    for o in image_files_list_object:
        image_files_path_list.append(config.STATIC_RESOURCE_SERVER_URL + str(o.relative_to(config.POST_DIR)))
    original_cover_path_path: str = config.STATIC_RESOURCE_SERVER_URL + str(
        original_cover_path_obj.relative_to(config.POST_DIR))
    compressed_cover_file_path: str = config.STATIC_RESOURCE_SERVER_URL + str(
        compressed_cover_file_obj.relative_to(config.POST_DIR))

    dict_for_return = {
        "image_files_url": image_files_path_list,
        "original_cover_url": original_cover_path_path,
        "compressed_cover_url": compressed_cover_file_path
    }
    return dict_for_return


def get_cover_file_url(dir_uuid: str) -> str:
    post_dir_object = Path(config.POST_DIR).joinpath(dir_uuid)
    compressed_cover_file_obj: Path = list(post_dir_object.joinpath("compressedCover").glob("*.*"))[0]
    compressed_cover_file_path: str = config.STATIC_RESOURCE_SERVER_URL + str(
        compressed_cover_file_obj.relative_to(config.POST_DIR))

    return compressed_cover_file_path


def remove_post_folder_by_uuid(dir_uuid: str) -> bool:
    post_dir = Path(config.POST_DIR).joinpath(dir_uuid)
    try:
        shutil.rmtree(post_dir)
    except IOError:
        return False
    return True


def create_all_project_dir():
    post_path_obj = Path(config.POST_DIR)
    avatar_path = Path(config.AVATAR_DIR)
    database_dir = Path("./database")
    background_dir = Path(config.BACKGROUND_DIR)

    post_path_obj.mkdir(parents=True, exist_ok=True)
    avatar_path.mkdir(parents=True, exist_ok=True)
    database_dir.mkdir(exist_ok=True)
    background_dir.mkdir(exist_ok=True)


def save_post_images(
        post_uuid: str,
        uploaded_file: list[UploadFile],
        supplementary_mode: bool
) -> bool:
    current_post_path_obj = Path(config.POST_DIR).joinpath(post_uuid)

    i: int = 0
    files_list: list[Path] = list(current_post_path_obj.glob("*.*"))
    if supplementary_mode:
        files_num: int = files_list.__len__()
        i = files_num
    else:
        # delete all files if supplementary mode is True.
        for f in files_list:
            f.unlink()
    for x in uploaded_file:
        suffix: str = x.filename.split(".")[-1]
        current_loop_filename = str(i) + "." + suffix
        i = i + 1
        try:
            with open(str(current_post_path_obj.joinpath(current_loop_filename)), "wb") as f:
                content = x.file.read()
                f.write(content)
        except IOError:
            return False
    return True


def save_post_cover(
        cover_name: str,
        post_uuid: str,
        cover_exist: bool,
        cover: UploadFile,
        update_mode: bool
) -> bool:
    current_post_path_obj = Path(config.POST_DIR).joinpath(post_uuid)
    current_cover_path_obj = current_post_path_obj.joinpath("cover")

    # Delete old cover if update mode is True.
    if update_mode:
        try:
            list(current_cover_path_obj.glob("*.*"))[0].unlink()
        except IOError:
            return False

    if cover_exist:
        try:
            with open(str(current_cover_path_obj.joinpath(cover_name)), "wb") as f:
                content = cover.file.read()
                f.write(content)
        except IOError:
            return False
    # If user does not post a cover, the cover will auto select from uploaded image files.
    else:
        try:
            auto_cover_name: str = str(list(current_post_path_obj.glob("*.*"))[0].name)
            source_file: Path = current_post_path_obj.joinpath(auto_cover_name)
            target_file: Path = current_cover_path_obj.joinpath(auto_cover_name)
            shutil.copy2(source_file, target_file)
        except IOError:
            return False

    return True


def compress_cover(
        post_uuid: str,
        update_mode: bool
) -> bool:
    current_post_path_obj = Path(config.POST_DIR).joinpath(post_uuid)
    cover_path_obj = current_post_path_obj.joinpath("cover")
    compressed_cover_path_obj = current_post_path_obj.joinpath("compressedCover")

    original_cover_path: Path = list(cover_path_obj.glob("*.*"))[0]
    original_cover_filename = original_cover_path.name

    if update_mode:
        try:
            list(compressed_cover_path_obj.glob("*.*"))[0].unlink()
        except IOError:
            return False

    try:
        compressed_cover_path_obj.mkdir(exist_ok=True)
    except IOError:
        return False

    print(original_cover_path)

    try:
        with Image.open(original_cover_path) as f:
            if original_cover_filename.split(".")[-1] == "gif" or original_cover_filename.split(".")[-1] == "webp":
                f.info["duration"] = 100
            f.thumbnail(size=config.size)
            f.save(compressed_cover_path_obj.joinpath(original_cover_filename), optimize=True, quality=config.quality)
    except IOError:
        return False

    return True
