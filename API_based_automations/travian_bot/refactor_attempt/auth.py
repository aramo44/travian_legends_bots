import base64
import hashlib
import logging
import secrets
import requests
from typing import Tuple, Optional
from dataclasses import dataclass

@dataclass
class AuthCredentials:
    email: str
    password: str

class TravianAuth:
    def __init__(self, credentials: AuthCredentials):
        self.credentials = credentials
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self) -> None:
        """Setup default session headers."""
        self.session.headers.update({
            "Content-Type": "application/json",
            "Origin": "https://www.travian.com",
            "Referer": "https://www.travian.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        })

    @staticmethod
    def generate_code_pair() -> Tuple[str, str]:
        """Generate PKCE code verifier and challenge."""
        verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode()
        challenge = base64.urlsafe_b64encode(
            hashlib.sha256(verifier.encode()).digest()
        ).rstrip(b'=').decode()
        return verifier, challenge

    def login_to_lobby(self) -> Optional[requests.Session]:
        """Login to Travian Legends lobby."""
        try:
            code_verifier, code_challenge = self.generate_code_pair()
            
            # Step 1: Initial login request
            login_url = "https://identity.service.legends.travian.info/provider/login?client_id=HIaSfC2LNQ1yXOMuY7Pc2uIH3EqkAi26"
            login_payload = {
                "login": self.credentials.email,
                "password": self.credentials.password,
                "code_challenge": code_challenge,
                "code_challenge_method": "S256"
            }
            
            logging.debug("Attempting initial login...")
            login_resp = self.session.post(login_url, json=login_payload)
            logging.debug(f"Login response status: {login_resp.status_code}")
            
            if login_resp.status_code != 200:
                logging.error(f"Login failed with status: {login_resp.status_code}")
                login_resp.raise_for_status()
                
            login_data = login_resp.json()
            
            if "code" not in login_data:
                raise ValueError(f"No code found in login response: {login_data}")
                
            code = login_data["code"]

            # Step 2: Exchange code for session
            auth_url = "https://lobby.legends.travian.com/api/auth/code"
            auth_payload = {
                "locale": "en-EN",
                "code": code,
                "code_verifier": code_verifier
            }
            
            logging.debug("Attempting to exchange code for session...")
            auth_resp = self.session.post(auth_url, json=auth_payload)
            logging.debug(f"Auth response status: {auth_resp.status_code}")
            
            if auth_resp.status_code != 200:
                logging.error(f"Auth code exchange failed with status: {auth_resp.status_code}")
                auth_resp.raise_for_status()
                
            logging.info("Login successful!")
            return self.session
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during login: {str(e)}")
            return None 