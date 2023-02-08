import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)
web_page = response.text
# print(web_page)

soup = BeautifulSoup(web_page, 'html.parser')
# print(soup.prettify())

list_items = soup.select("h3.c-title.a-no-trucate") 
song_list = [item.get_text().strip() for item in list_items]
# print(song_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="Your redirect url",
        client_id="Your Spotify App Client ID",
        client_secret="Your Spotify App Client Secret",
        show_dialog=True,
        cache_path="token.txt"   # path to location to save tokens so you don't need to re-authorize
    )
)

song_uris = []
year = date.split("-")[0]

for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except:
        print(f"{song} doesn't exist in Spotify. Skipped.")
    
user_id = sp.current_user()["id"]
playlist_name = f"{date} Billboard 100"

playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)