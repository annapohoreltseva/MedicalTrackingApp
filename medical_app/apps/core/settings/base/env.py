import os
from pathlib import Path

import environ

ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
BASE_DIR = ROOT_PATH / "medical_app"
APPS_DIR = BASE_DIR / "apps"

env = environ.Env(
    # type, default
    DEBUG=(bool, False),
    SECRET_KEY=(str, "django-insecure-change-me-in-production"),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
)

# Load .env file if present(local development without Docker)
env_file = ROOT_PATH / ".env"
if os.path.exists(env_file):
    env.read_env(env_file)

# Exported settings 
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")
