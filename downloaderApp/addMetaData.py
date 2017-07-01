import requests
import shutil
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import os


def addMetaData(playlistName, url, title, artist, album, track):
    response = requests.get(url, stream=True)
    dir = playlistName

    with open(dir + '/img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    filename = dir + "/" + title + ".mp3"

    audio = MP3(filename=filename, ID3=EasyID3)
    audio['artist'] = artist
    audio['title'] = title
    audio['tracknumber'] = track
    audio['album'] = album
    audio.save()

    audio = MP3(filename=filename, ID3=ID3)

    # audio.tags.delete(filename=filename, delete_v1=True, delete_v2=True)
    audio.tags.add(
        APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc=u'Cover',
            data=open(dir + "/img.jpg", 'rb').read()
        )
    )
    audio.save(filename, v2_version=3, v1=2)
    try:
        os.remove(dir + "/img.jpg")
    except:
        pass


def turnToZip(output_name, dir_name, delete=True):
    shutil.make_archive(output_name, 'zip', dir_name)

    if delete == True:
        shutil.rmtree(dir_name)
