import logging
import requests
from typing import List, Optional
from models import Avatar, GameWorld, Coordinates, OasisInfo

class TravianAPI:
    def __init__(self, session: requests.Session):
        self.session = session

    def get_avatars(self) -> List[Avatar]:
        """Get list of available avatars (game worlds) for the user."""
        graphql_url = "https://lobby.legends.travian.com/api/graphql"
        graphql_payload = {
            "variables": {},
            "query": """
            {
              avatars {
                uuid
                name
                gameworld {
                  metadata {
                    url
                    name
                  }
                }
              }
            }
            """
        }
        
        response = self.session.post(graphql_url, json=graphql_payload)
        response.raise_for_status()
        data = response.json()["data"]["avatars"]

        return [
            Avatar(
                uuid=a["uuid"],
                name=a["name"],
                world=GameWorld(
                    name=a["gameworld"]["metadata"]["name"],
                    url=a["gameworld"]["metadata"]["url"]
                )
            )
            for a in data
        ]

    def login_to_server(self, avatar: Avatar) -> requests.Session:
        """Login to a specific game world."""
        try:
            play_url = f"https://lobby.legends.travian.com/api/avatar/play/{avatar.uuid}"
            logging.debug(f"Attempting to play avatar: {avatar.name}")
            
            play_resp = self.session.post(play_url)
            logging.debug(f"Play response status: {play_resp.status_code}")
            
            if play_resp.status_code != 200:
                logging.error(f"Play request failed with status: {play_resp.status_code}")
                play_resp.raise_for_status()
                
            play_data = play_resp.json()
            
            if "code" not in play_data:
                raise ValueError("No code found in play response")
                
            code = play_data["code"]

            server_session = requests.Session()
            server_session.cookies.update(self.session.cookies.get_dict())
            
            server_auth_url = f"{avatar.world.url.rstrip('/')}/api/v1/auth?code={code}&response_type=redirect"
            logging.debug(f"Authenticating with game server...")
            
            auth_resp = server_session.get(server_auth_url, allow_redirects=True)
            
            if auth_resp.status_code != 200:
                logging.error(f"Server auth failed with status: {auth_resp.status_code}")
                auth_resp.raise_for_status()

            return server_session
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise

    def get_oasis_info(self, server_session: requests.Session, world_url: str, coords: Coordinates) -> Optional[OasisInfo]:
        """Get information about an oasis at specific coordinates."""
        oasis_url = f"{world_url}/ajax.php"
        params = {"cmd": "mapDetails", "x": coords.x, "y": coords.y}
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
            "Referer": f"{world_url}/karte.php?x={coords.x}&y={coords.y}"
        }

        response = server_session.get(oasis_url, headers=headers, params=params)
        response.raise_for_status()
        
        # Parse response and return OasisInfo object
        # Note: You'll need to implement the actual parsing logic based on the response format
        data = response.json()
        return OasisInfo(
            coordinates=coords,
            type=data.get("type", ""),
            owner=data.get("owner"),
            troops=data.get("troops"),
            resources=data.get("resources")
        ) 