# SpotifyUpdater 
Script Python de Monitoramento de Lançamentos do Spotify
---
#### SpotifyUpdater é um script Python que monitora os últimos lançamentos de um artista e adiciona novas músicas automaticamente no topo de uma playlist do Spotify, evitando duplicatas por ID ou nome. Mantém sua playlist sempre atualizada e organizada de forma prática e automática.

## 1️⃣ Objetivo

O script tem como objetivo:

- Monitorar os últimos lançamentos de um artista no Spotify.
- Adicionar automaticamente músicas novas em uma playlist específica.
- Evitar duplicatas, considerando tanto o **ID** quanto o **nome** da música, para não subir músicas repetidas mesmo que o artista use estratégias de singles.

---

## 2️⃣ Requisitos

- **Python 3.10+** (testado no Python 3.13)  
- Bibliotecas Python:
  - `spotipy`
- Conta Spotify Premium (opcional, mas recomendado para evitar restrições)
- App registrado no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) com **Client ID**, **Client Secret** e **Redirect URI** configurados.
- **ngrok** (para HTTPS local, necessário se o Spotify exigir Redirect URI HTTPS)

---

## 3️⃣ Instalação

### 3.1 Python e Spotipy

```bash
pip install spotipy
```

#### 3.2 Instalar o ngrok

Acesse ngrok.com
.

Faça login (crie uma conta gratuita, se necessário).

Baixe a versão do ngrok para seu sistema operacional.

Extraia o arquivo e coloque o executável em uma pasta de fácil acesso ou adicione ao PATH do sistema.

## 4️⃣ Iniciar o ngrok e criar túnel HTTPS

Abra o terminal ou prompt de comando.

Para criar um túnel HTTPS para o seu servidor local (exemplo: Flask rodando na porta 5000), rode:

```bash
ngrok http 5000
```

### 4.1 O ngrok vai gerar um link público HTTPS, algo como:

```arduíno
https://abcd1234.ngrok-free.app
```

### 4.2 Use essa URL como Redirect URI no seu app do Spotify:
```bash
https://abcd1234.ngrok-free.app/callback
```
- Esse link vai redirecionar as requisições do Spotify para o seu servidor local.

- *Toda vez que reiniciar o ngrok free, a URL muda, então atualize o Redirect URI se necessário.*

## 5️⃣ Configuração do Spotify

Crie um app no Spotify Developer Dashboard.

Copie o Client ID e Client Secret.

Configure o Redirect URI (via ngrok ou outro HTTPS).

Anote o ID do artista e o ID da playlist:

ID do artista: link do Spotify → https://open.spotify.com/artist/<ARTIST_ID>

ID da playlist: link do Spotify → https://open.spotify.com/playlist/<PLAYLIST_ID>

## 6️⃣ Estrutura do Script
### Variáveis de Configuração

```python
CLIENT_ID = "seu_client_id"
CLIENT_SECRET = "seu_client_secret"
REDIRECT_URI = "https://abcd1234.ngrok-free.app/callback"
SCOPE = "playlist-modify-public playlist-modify-private user-library-read"
ARTIST_ID = "id_do_artista"
PLAYLIST_ID = "id_da_playlist"
```
- `SCOPE`: Define permissões para adicionar músicas em playlists e ler biblioteca do usuário.

#### Função principal: `get_playlist_tracks`

```python
def get_playlist_tracks(sp, playlist_id):
    tracks = []
    track_names = set()
    results = sp.playlist_items(playlist_id)
    while results:
        for item in results['items']:
            track = item['track']
            if track:
                tracks.append(track['id'])
                track_names.add(track['name'].lower())
        if results.get('next'):
            results = sp.next(results)
        else:
            results = None
    return tracks, track_names
```

- Retorna:

- Lista de IDs das músicas já presentes na playlist.

- Lista de nomes das músicas, em lowercase, para evitar duplicatas por nome.

## Processamento dos lançamentos

```python
results = sp.artist_albums(ARTIST_ID, album_type="single", limit=5)
if results['items']:
    for album in results['items']:
        tracks = sp.album_tracks(album['id'])
        for track in tracks['items']:
            track_name_lower = track['name'].lower()
            if track['id'] not in playlist_tracks and track_name_lower not in playlist_track_names:
                sp.playlist_add_items(PLAYLIST_ID, [track['uri']], position=0)
                playlist_tracks.append(track['id'])
                playlist_track_names.add(track_name_lower)
```

- Busca os últimos 5 lançamentos do artista.

- Para cada música:

  - Verifica se não está na playlist (ID e nome).
 
  - Se não estiver, adiciona no topo da playlist (position=0).

  - Atualiza listas para evitar duplicatas durante o mesmo loop.

  ## 7️⃣ Como rodar

1. Salve o script como spotify_playlist_bot.py.

2. Inicie seu servidor local (exemplo: Flask) se usar ngrok.

3. Inicie o ngrok na porta do servidor local:

```bash
ngrok http 5000
```

4. Rode o script Python:

```python
python spotify_playlist_bot.py
```
5. Na primeira execução:

   - Será aberto um navegador pedindo autorização do Spotify.

   - Autorize o app e você será redirecionado para o ngrok (ou redirect URI configurado).

   - O script pega o token de acesso e começa a rodar.

## 8️⃣ Boas práticas

- Evite nomear o arquivo como spotipy.py.

- ngrok Free: URL muda a cada execução, atualize Redirect URI se necessário.

- Duplicatas: checagem por ID e nome, evitando problemas com estratégias de singles.

- Automatização: use cron job (Linux/macOS) ou Task Scheduler (Windows) para rodar periodicamente.