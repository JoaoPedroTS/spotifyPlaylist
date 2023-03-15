import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from consts import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

URL = "https://www.billboard.com/charts/hot-100"

dateInput = input("Which date do you want to travel to? Type the date in this format YYYY-MM-DD ")
response = requests.get(f"{URL}/{dateInput}")

billboardHTML = response.text
soup = BeautifulSoup(billboardHTML, "html.parser")

firstSong = soup.find(
    name="h3",
    class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet",
    id="title-of-a-story"
)

songsTags = soup.find_all(
    name="h3",
    class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only",
    id="title-of-a-story"
)

titlesList = [song.getText().strip() for song in songsTags]
titlesList.insert(0, firstSong.getText().strip())

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt"
    )
)

userId = sp.current_user()["id"]
print(userId)

songUris = []
year = dateInput.split("-")[0]

for song in titlesList:
    result = sp.search(
        q=f"track:{song} year:{year}",
        type="track"
    )
    print(result)

    try:
        uri = result["tracks"]["items"][0]["uri"]
        songUris.append(uri)
    except IndexError:
        print(f"{song} doesm't exist in spotify. skipped.")

playlist = sp.user_playlist_create(
    user=userId,
    name=f"{dateInput} Billboard 100",
    public=False
)

print(playlist)

sp.playlist_add_items(
    playlist_id=playlist["id"],
    items=songUris
)