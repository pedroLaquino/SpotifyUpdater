import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configurações
CLIENT_ID = "30bbe4b3db114195b431c32ad2a330ef"
CLIENT_SECRET = "a1884591e9824ce8ba442e09ce5b2ccf"
REDIRECT_URI = "https://99b32b619269.ngrok-free.app/callback"

SCOPE = "playlist-modify-public playlist-modify-private user-library-read"
ARTIST_ID = "4W4NkfM4A1sX2S2bfYlV07"
PLAYLIST_ID = "2q4QwyB0Nk4qt87CcYyl0K"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Função para pegar todas as tracks da playlist
def get_playlist_tracks(sp, playlist_id):
    tracks = []
    track_names = set()
    results = sp.playlist_items(playlist_id)
    while results:
        for item in results['items']:
            track = item['track']
            if track:  # evita itens nulos
                tracks.append(track['id'])
                track_names.add(track['name'].lower())  # salvar em lowercase pra evitar duplicidade de case
        if results.get('next'):
            results = sp.next(results)
        else:
            results = None
    return tracks, track_names

# Pega músicas já na playlist
playlist_tracks, playlist_track_names = get_playlist_tracks(sp, PLAYLIST_ID)

# Últimos lançamentos do artista
results = sp.artist_albums(ARTIST_ID, album_type="single", limit=50)
if results['items']:
    for album in results['items']:
        tracks = sp.album_tracks(album['id'])
        for track in tracks['items']:
            track_name_lower = track['name'].lower()
            if track['id'] not in playlist_tracks and track_name_lower not in playlist_track_names:
                print(f"Adicionando {track['name']} na playlist...")
                sp.playlist_add_items(PLAYLIST_ID, [track['uri']], position=0)
                # Atualiza as listas para não adicionar novamente se houver mais de uma música igual
                playlist_tracks.append(track['id'])
                playlist_track_names.add(track_name_lower)
            else:
                print(f"{track['name']} já está na playlist, pulando...")
