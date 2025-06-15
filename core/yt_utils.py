import requests

def get_channel_playlists(api_key, channel_id):
    url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={channel_id}&maxResults=50&key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    playlists = response.json().get("items", [])

    return playlists



def get_playlist_videos(api_key, playlist_id):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "snippet,contentDetails",  # 🔥 THIS IS CRITICAL
        "playlistId": playlist_id,
        "maxResults": 50,
        "key": api_key
    }
    response = requests.get(url, params=params)
    items = response.json().get("items", [])
    return items
