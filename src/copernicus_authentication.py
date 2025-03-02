import os
import logging
from typing import Optional, Dict, Tuple
from sentinelsat import SentinelAPI
from datetime import date, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class CopernicusAuth:
    """
    Handles authentication with Copernicus Data Space API.
    """
    def __init__(self, username: str, password: str, api_url: str = "https://apihub.dataspace.copernicus.eu") -> None:
        self.username = username
        self.password = password
        self.api_url = api_url
        self.api: Optional[SentinelAPI] = None

    def authenticate(self) -> Optional[SentinelAPI]:
        """
        Authenticates with the Sentinel API and returns an API instance.
        """
        try:
            self.api = SentinelAPI(self.username, self.password, self.api_url)
            logging.info("Authentication successful!")
            return self.api
        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            return None