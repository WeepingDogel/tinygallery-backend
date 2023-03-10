# Authentication
SECRET_KEY = "0ee5776b64d0b51644cb60baef21d4f76ee97ec497abbae2f20f3dd18a665049"
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
# The maximum number of posts on a single page.
posts_limit = 20

# User avatar directory.
AVATAR_DIR = "./static/avatars"
# Avatar size
AVATAR_SIZE_PROFILE = 200, 200
AVATAR_SIZE_HOME = 40, 40
# User profile background images' directory.
BACKGROUND_DIR = "./static/backgrounds"

# Static resource server Url
POSTS_RESOURCE_SERVER_URL = "http://localhost:8755/static/posts/"
AVATARS_RESOURCE_SERVER_URL = "http://localhost:8755/static/avatar/"
BACKGROUND_RESOURCE_SERVER = "http://localhost:8755/static/backgrounds"
