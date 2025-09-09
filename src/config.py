"""Configuration management for Yandex to Google Calendar sync."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the sync application."""
    
    # Yandex Calendar settings
    YANDEX_CALDAV_URL: str = os.getenv('YANDEX_CALDAV_URL', 'https://caldav.yandex.ru')
    YANDEX_USERNAME: Optional[str] = os.getenv('YANDEX_USERNAME')
    YANDEX_PASSWORD: Optional[str] = os.getenv('YANDEX_PASSWORD')
    
    # Google Calendar settings
    GOOGLE_CREDENTIALS_FILE: str = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    GOOGLE_TOKEN_FILE: str = os.getenv('GOOGLE_TOKEN_FILE', 'token.json')
    GOOGLE_CALENDAR_ID: str = os.getenv('GOOGLE_CALENDAR_ID', 'primary')
    
    # Sync settings
    SYNC_INTERVAL_MINUTES: int = int(os.getenv('SYNC_INTERVAL_MINUTES', '30'))
    DAYS_AHEAD: int = int(os.getenv('DAYS_AHEAD', '30'))
    DAYS_BEHIND: int = int(os.getenv('DAYS_BEHIND', '7'))
    
    # State management
    STATE_FILE: str = os.getenv('STATE_FILE', 'sync_state.json')
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present."""
        if not cls.YANDEX_USERNAME:
            raise ValueError("YANDEX_USERNAME environment variable is required")
        if not cls.YANDEX_PASSWORD:
            raise ValueError("YANDEX_PASSWORD environment variable is required")
        if not os.path.exists(cls.GOOGLE_CREDENTIALS_FILE):
            raise ValueError(f"Google credentials file not found: {cls.GOOGLE_CREDENTIALS_FILE}")