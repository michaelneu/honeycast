from pychromecast import Chromecast
from pychromecast.controllers.spotify import SpotifyController
import spotify_token

username = input("Spotify username: ")
password = input("Spotify password: ")
cast_address = input("Honeycast url: ") or "localhost"

session = spotify_token.start_session(username, password)
token = session[0]

cast = Chromecast(cast_address)
controller = SpotifyController(token)
cast.register_handler(controller)
controller.launch_app()
