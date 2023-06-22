from pathlib import Path
import secrets

# Authentication
secret_file = Path(".").joinpath("secret.txt")
with open(secret_file, "r") as c:
    secret_key_from_file = c.read()
    if secret_key_from_file == "":
        print("Secret error")
        exit()
    else:
        SECRET_KEY = secret_key_from_file
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# DATABASE
DATABASE_URL = "sqlite:///./database/database.sqlite"

# Image Directory.
POST_DIR = "./static/posts"
# Allow posts suffix.
ALLOW_SUFFIX = ("jpg", "png", "bmp", "jpeg", "gif", "webp")
# The size of compressed cover file.
size = 256, 256
# The quality of compressed cover file.
quality = 50
# The maximum amount posts on a single page.
posts_limit = 20

# User avatar directory.
AVATAR_DIR = "./static/avatars"
# Avatar size
AVATAR_SIZE_PROFILE = 200, 200
AVATAR_SIZE_HOME = 40, 40

# User profile background images' directory.
BACKGROUND_DIR = "./static/backgrounds"

# Static resource server Url
POSTS_RESOURCE_SERVER_URL = "http://127.0.0.1:8755/static/posts/"
AVATARS_RESOURCE_SERVER_URL = "http://127.0.0.1:8755/static/avatar/"
BACKGROUND_RESOURCE_SERVER = "http://127.0.0.1:8755/static/backgrounds"

# The maximum amount remarks on a single post.
remark_limit = 10

# The maximum amount replies on a single remark.
reply_limit = 300

ADMIN_LIST = './admin_list.json'
