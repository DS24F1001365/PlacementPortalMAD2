from datetime import timedelta
import os


class Config:

    SQLALCHEMY_DATABASE_URI = "sqlite:///ppa.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "PPA_MAD2_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 60

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__),
        "uploads",
        "resumes"
    )