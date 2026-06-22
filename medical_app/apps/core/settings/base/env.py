import os
from pathlib import Path

import environ

ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent
BASE_DIR = ROOT_PATH
APPS_DIR = BASE_DIR / "apps"
print(ROOT_PATH)
print(APPS_DIR)
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)
env_file = ROOT_PATH / ".env"
if os.path.exists(env_file):
    env.read_env(env_file)

# SECRET_KEY = env("SECRET_KEY")
# print(SECRET_KEY)
DEBUG = env("DEBUG")
print(DEBUG)
