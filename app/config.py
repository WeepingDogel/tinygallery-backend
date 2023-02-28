# Authentication
SECRET_KEY = "0ee5776b64d0b51644cb60baef21d4f76ee97ec497abbae2f20f3dd18a665049"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# DATABASE
DATABASE_URL = "sqlite:///./database/database.sqlite"

# Image Directory
IMAGE_DIR = "./static/posts"

# Allow upload suffix
ALLOW_SUFFIX = ("jpg", "png", "bmp", "jpeg", "gif", "webp")