import random
import shutil
from PIL import Image
from pathlib import Path
from .. import config
from .dir_tool import compress_avatar


def generate_default_avatar(user_uuid: str):
    default_avatar = Path(config.AVATAR_DIR).joinpath('default').joinpath('default_avatar.jpg')
    avatar_user_path = Path(config.AVATAR_DIR).joinpath(user_uuid)
    compressed_avatar_200_path = avatar_user_path.joinpath('200')
    compressed_avatar_40_path = avatar_user_path.joinpath('40')

    if avatar_user_path.exists():
        shutil.rmtree(str(avatar_user_path))

    try:
        avatar_user_path.mkdir(exist_ok=True)
        compressed_avatar_200_path.mkdir(exist_ok=True)
        compressed_avatar_40_path.mkdir(exist_ok=True)
        file_default_avatar = open(default_avatar, 'rb')
        with open(str(avatar_user_path.joinpath(user_uuid + str(random.randint(0, 9999)) + ".jpg")), 'wb') as f:
            content = file_default_avatar.read()
            f.write(content)
        if not compress_avatar(
            avatar_size=config.AVATAR_SIZE_PROFILE,
            original_path=avatar_user_path,
            compressed_path=compressed_avatar_200_path,
            file_suffix='jpg',
            user_uuid=user_uuid
        ):
            return False
        if not compress_avatar(
            avatar_size=config.AVATAR_SIZE_HOME,
            original_path=avatar_user_path,
            compressed_path=compressed_avatar_40_path,
            file_suffix='.jpg',
            user_uuid=user_uuid
        ):
            return False
    except IOError:
        return False
