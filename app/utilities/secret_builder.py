from pathlib import Path

import secrets

secret_file_path = Path(".").joinpath("secret.txt")
secret_key = secrets.token_hex(32)


# Create secret if it doesn't exist.
def create_secret():
    if not secret_file_path.exists():
        with open(secret_file_path, "w") as c:
            c.write(secret_key)
