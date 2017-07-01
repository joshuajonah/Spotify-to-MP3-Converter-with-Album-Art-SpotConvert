# SpotConvert

SpotConvert converts a Spotify Playlist, Album, or song, into a collection of corresponding MP3 files, with Album Artwork, and ZIPs it and sends to the user to download. It works through YouTube, YouTube-DL, Spotipy, FFMPEG, and Django in the backend, with Django-RQ running the process workers. 



How to use?

1. Run the manage.py runserver
2. Run a redis server with redis-server
3. Run one or a few worker processes with Django-RQ (* python manage.py rqworker)
4. Go onto the website and input a URI or URL


