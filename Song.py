# server.py
from flask import Flask, render_template_string
from GetSpotifyAuth import get_spotify_token
import requests

ACCESS_TOKEN = get_spotify_token()
app = Flask(__name__)

def get_current_song_embed_url():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        song_url = data["item"]["external_urls"]["spotify"]
        # Extract track ID from the URL
        track_id = song_url.split("/")[-1].split("?")[0]
        embed_url = f"https://open.spotify.com/embed/track/{track_id}"
        return embed_url
    else:
        return None

@app.route('/')
def home():
    embed_url = get_current_song_embed_url()
    if embed_url:
        return render_template_string(f"""
            <html>
            <head><title>Now Playing</title></head>
            <meta http-equiv="refresh" content="30">

            <iframe src="{embed_url}" width="300" height="150" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
            
            
            </html>
        """)
    else:
        return "<h2></h2>"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1234)
