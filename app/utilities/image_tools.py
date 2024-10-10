import shutil
from pathlib import Path
from PIL import Image
from .. import config

def generate_default_avatar(user_uuid: str):
    default_avatar = Path(config.AVATAR_DIR).joinpath('default').joinpath('default_avatar.jpg')
    user_avatar_dir = Path(config.AVATAR_DIR).joinpath(user_uuid)
    user_avatar_dir.mkdir(parents=True, exist_ok=True)
    
    avatar_sizes = [('full', None), ('200', (200, 200)), ('40', (40, 40))]
    
    for size_name, size in avatar_sizes:
        target_dir = user_avatar_dir if size_name == 'full' else user_avatar_dir.joinpath(size_name)
        target_dir.mkdir(exist_ok=True)
        target_file = target_dir.joinpath(f"{user_uuid}.jpg")
        
        if size:
            with Image.open(default_avatar) as img:
                img.thumbnail(size)
                img.save(target_file, "JPEG")
        else:
            shutil.copy(default_avatar, target_file)

    return True

def generate_user_avatar(user_uuid: str, image: Image.Image):
    user_avatar_dir = Path(config.AVATAR_DIR).joinpath(user_uuid)
    user_avatar_dir.mkdir(parents=True, exist_ok=True)
    
    avatar_sizes = [('full', None), ('200', (200, 200)), ('40', (40, 40))]
    
    for size_name, size in avatar_sizes:
        target_dir = user_avatar_dir if size_name == 'full' else user_avatar_dir.joinpath(size_name)
        target_dir.mkdir(exist_ok=True)
        target_file = target_dir.joinpath(f"{user_uuid}.jpg")
        
        if size:
            img_copy = image.copy()
            img_copy.thumbnail(size)
            img_copy.save(target_file, "JPEG")
        else:
            image.save(target_file, "JPEG")

    return True
