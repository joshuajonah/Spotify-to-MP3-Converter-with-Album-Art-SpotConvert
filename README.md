# SpotConvert

SpotConvert converts a Spotify Playlist, Album, or song, into a collection of corresponding MP3 files, with Album Artwork, and ZIPs it and sends to the user to download. It works through YouTube, YouTube-DL, Spotipy, FFMPEG, and Django in the backend, with Django-RQ running the process workers. 



How to use?

1. Clone with `git clone https://github.com/joshuajonah/Spotify-to-MP3-Converter-with-Album-Art-SpotConvert.git`.
2. Navigate to the cloned directory.
3. Start a new virtualenv with `virtualenv .` and activate it with `source bin/activate`.
4. Install the python requirements with `pip install -r requirements.txt` 
5. Install and configure redis-server.
6. Install ffmpeg with `sudo apt-get install ffmpeg`.
7. Run the `./manage.py runserver`.
8. Run a Django-RQ process with `python manage.py rqworker`.
9. Browse to Spotify online player and copy the url of the album or playlist you want to use.
10. Browse to your local server at `http://localhost:8000` and enter that url you got in the last step.


