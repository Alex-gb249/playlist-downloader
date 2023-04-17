import pytube
import os
import requests
import subprocess

def run():
    spotifyGetList("5f5gKwoGezADtAJZJMgUSH")

def spotifyGetList(playlist:str, limit:int=100):
    clientId = ""
    clientSecret = ""
    
    directory = "C:/Users/alexi/Music/Spotify"
    
    # Get access token
    url = "https://accounts.spotify.com/api/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {'grant_type': 'client_credentials', 'client_id': clientId, 'client_secret': clientSecret}
    result = requests.post(url=url, headers=headers, data=body).json()
    authorization = result['token_type'] + ' ' + result['access_token']
    
    # Get playlist info
    url2 = f"https://api.spotify.com/v1/playlists/{playlist}/tracks?limit={limit}"
    print(url2)
    headers2 = {'Authorization' : authorization}
    result2:dict = requests.get(url=url2, headers=headers2).json()
    
    songs:list = []
    for item in result2['items']:
        songs.append(str(item['track']['name']))
        
    for i, title in enumerate(songs):
        downloadYoutube(title, directory)
        print(f"{i+1}. {title} has been downloaded.")
    
def downloadYoutube(title:str, directory:str) -> str:
    try:
        # Search and download
        yt = pytube.Search(title).results[0]
        subprocess.run('cls', shell=True)
        out_file = yt.streams.filter(only_audio=True).first().download(directory)

        # Changing format
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    except FileExistsError:
        pass
    
if __name__ == "__main__":
    run()
