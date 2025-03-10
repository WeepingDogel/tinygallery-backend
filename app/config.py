from pathlib import Path
import secrets

# Authentication
secret_file = Path(".").joinpath("secret.txt")
try:
    with open(secret_file, "r") as c:
        secret_key_from_file = c.read().strip()  # 添加 strip() 去除可能的空白字符
        if not secret_key_from_file:
            # 如果文件为空，生成新的密钥
            secret_key_from_file = secrets.token_hex(32)
            with open(secret_file, "w") as f:
                f.write(secret_key_from_file)
        SECRET_KEY = secret_key_from_file
except FileNotFoundError:
    # 如果文件不存在，创建新文件并生成密钥
    secret_key_from_file = secrets.token_hex(32)
    with open(secret_file, "w") as f:
        f.write(secret_key_from_file)
    SECRET_KEY = secret_key_from_file

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 增加到60分钟

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
POSTS_RESOURCE_SERVER_URL = "/static/posts/"
AVATARS_RESOURCE_SERVER_URL = "/static/avatar/"
BACKGROUND_RESOURCE_SERVER = "/static/backgrounds"

# The maximum amount remarks on a single post.
remark_limit = 10

# The maximum amount replies on a single remark.
reply_limit = 300

ADMIN_LIST = './admin_list.json'
