# app/core/config.py
from pydantic import BaseSettings, EmailStr
from typing import Optional


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    description: str = 'Благотворительный'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None


    class Config:
        env_file = '.env'


settings = Settings()