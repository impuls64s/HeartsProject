import os
from pathlib import Path
from dataclasses import dataclass

import aioredis


BASE_DIR = Path(__file__).parent.parent


# DATABASE
DATABASE_URL = os.getenv("DATABASE_URL")


# SMTP MAIL
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


# TWILIO API
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


# REDIS
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', decode_responses=True)


# JWT
@dataclass
class JWTSettings:
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 10
    refresh_token_expire_minutes: int = 60 * 24 * 1
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'


