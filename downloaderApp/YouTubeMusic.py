from __future__ import unicode_literals
import youtube_dl

from downloaderApp.addMetaData import addMetaData

from googleapiclient.discovery import build
from django.conf import settings


class Song():
    id = "http://www.youtube.com/watch?v="

    # initialize a Song with the title, artist and spotifyPlaylist
    def __init__(self, playlistName, title, artist, album, track_num, albumcover):
        self.playlistName = playlistName
        self.title = title
        self.artist = artist
        self.album = album
        self.track_num = track_num
        self.albumcover = albumcover

    def completeMP3(self):
        addMetaData(self.playlistName, self.albumcover, self.title, self.artist, self.album, str(self.track_num))

    def getInfo(self):
        return "Title: {}, Artist: {}, Album: {}, Track: {}, Cover: {}".format(self.title, self.artist, self.album,
                                                                               self.track_num, self.albumcover)

    def getTitleAndArtist(self):
        return "{} by {}".format(self.title, self.artist)

    def search(self):

        DEVELOPER_KEY = "AIzaSyCfnOUz1nzmMrkLG86_EUQn0lzqbmTC0oQ"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        search_response = youtube.search().list(
            q="{} by {} audio".format(self.title, self.artist),
            part="id, snippet",
            maxResults=1,
        ).execute()

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                self.id = self.id + search_result["id"]["videoId"]
        return self.id

    def download(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': settings.FFMPEG_PATH,
            'prefer_ffmpeg': "True",
            'no_warnings': "True",
            'quiet': "True",
            'outtmpl': r"{}/{}.%(ext)s".format(self.playlistName, self.title),
            'postprocessors': [
                # {'key': 'FFmpegMetadata'},
                {'key': 'FFmpegExtractAudio',
                 'preferredcodec': 'mp3',
                 'preferredquality': '1'}]

        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
