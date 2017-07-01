import spotipy
import random
from spotipy import util
from spotipy.oauth2 import SpotifyClientCredentials


def getSongs(uri):
    print('STARTING: {}'.format(uri))
    client_credentials_manager = SpotifyClientCredentials(client_id="314da63cc8b046bb8d0d925c1412a93b",
                                                          client_secret="b50ef127af6846a4b45c296f5fa7717b")

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    uri = uri

    """https://open.spotify.com/user/spotify/playlist/5l9VJBBC9wRsN7vTHYao7S
    https://open.spotify.com/user/dyablade/playlist/7y4yicwfvdgDCMGJeLUYM1
    spotify:user:spotify:playlist:5l9VJBBC9wRsN7vTHYao7S

    spotify:album:3CCnGldVQ90c26aFATC1PW
    https://open.spotify.com/album/3CCnGldVQ90c26aFATC1PW
    """

    #this method converts URL into URI
    if uri.startswith("https://"):
        almostURI = uri.replace("https://", "")
        almostURI = almostURI.split('/')
        #if its album
        if almostURI[1] == "user":
            uri = "{}:{}:{}:{}:{}".format("spotify", almostURI[1], almostURI[2], almostURI[3], almostURI[4])
        elif almostURI[1] == "album":
            uri = "{}:{}:{}".format("spotify", almostURI[1], almostURI[2])
    
    elif uri.startswith("http://"):
        almostURI = uri.replace("http://", "")
        almostURI = almostURI.split('/')
        if almostURI[1] == "user":
            uri = "{}:{}:{}:{}:{}".format("spotify", almostURI[1], almostURI[2], almostURI[3], almostURI[4])
        elif almostURI[1] == "album":
            uri = "{}:{}:{}".format("spotify", almostURI[1], almostURI[2])

    elif (not uri.startswith("spotify")):
        print(uri)
        almostURI = uri.split('/')

        if almostURI[1] == "user":
            uri = "{}:{}:{}:{}:{}".format("spotify", almostURI[1], almostURI[2], almostURI[3], almostURI[4])
        elif almostURI[1] == "album":
            uri = "{}:{}:{}".format("spotify", almostURI[1], almostURI[2])


    songs = {}
    # if album do this


    if uri.split(':')[1] == 'album':

        randomlyGeneratedFolderName = 'album{}'.format(random.randint(100,1000000))
        # use this one to get individual songs
        tracks = sp.album_tracks(uri.split(':')[2])
        for song in tracks['items']:
            try:
                t = sp.track(song['id'])
                title = song['name']
                title = title.replace("/","-")
                artist = song['artists'][0]['name']
                album = t['album']['name']
                track = song['track_number']
                image = t['album']['images'][0]['url']

                folderSavedName = randomlyGeneratedFolderName

                # use this one to get full info on song
                # saves to dictionary Song Name : Artist Name, Album Name, Track Number, Album Art URL
                songs.update({title: [artist, album, track, image,
                                      folderSavedName]})  # saves to dictionary Song Name : Artist Name, Album Name, Track Number, Album Art URL
            except:
                pass

    elif uri.split(':')[3] == 'playlist':
        # its a playlist
        randomlyGeneratedFolderName = 'playlist{}'.format(random.randint(100, 1000000))

        username = uri.split(':')[2]
        playlist_id = uri.split(':')[4]

        def get_playlist_tracks(username, playlist_id):
            results = sp.user_playlist_tracks(username, playlist_id)
            tracks = results['items']
            while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])
            return tracks
        #change this to get over +100 tracks, use this method but its a little weird, FIGURE IT OUR NIGGA


        tracks = get_playlist_tracks(username, playlist_id)
        if len(tracks) < 500:
            for song in tracks:
                try:
                    title = song['track']['name']
                    title = title.replace("/", "-")
                    artist = song['track']['album']['artists'][0]['name']
                    album = song['track']['album']['name']
                    track = song['track']['track_number']
                    # could be 0 if 1 doesnt work
                    image = song['track']['album']['images'][0]['url']
                    folderSavedName = randomlyGeneratedFolderName
                    songs.update({title: [artist, album, track, image,
                                          folderSavedName]})  # saves to dictionary Song Name : Artist Name, Album Name, Track Number, Album Art URL
                except:
                    pass
        else:
            for song in tracks[0:500]:
                try:
                    title = song['track']['name']
                    title = title.replace("/", "-")
                    artist = song['track']['album']['artists'][0]['name']
                    album = song['track']['album']['name']
                    track = song['track']['track_number']
                    # could be 0 if 1 doesnt work
                    image = song['track']['album']['images'][0]['url']
                    folderSavedName = randomlyGeneratedFolderName
                    songs.update({title: [artist, album, track, image,
                                          folderSavedName]})  # saves to dictionary Song Name : Artist Name, Album Name, Track Number, Album Art URL
                except:
                    pass
    return songs