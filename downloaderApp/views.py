#!/usr/bin/env python3
from __future__ import absolute_import, unicode_literals

import json

from downloaderApp.SpotifyURL import getSongs
from downloaderApp.YouTubeMusic import Song
from downloaderApp.forms import submitURLForm

import django_rq
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rq import get_current_job
from .addMetaData import turnToZip


# Create your views here.


def index(request):
    if request.method == "POST":
        form = submitURLForm(request.POST)

        if form.is_valid():
            uri = form.cleaned_data['uri']

            """
            worker = django_rq.get_worker()
            worker.work()
            """

            t = django_rq.enqueue(download, uri, timeout=600)

            return redirect('status_page', job_id=t.get_id())
    else:
        form = submitURLForm()

    return render(request, "urlsub.html")


def status_page(request, job_id):
    return render(request, "progress.html", {'job_id': job_id})


def progress(request, job_id):
    job = django_rq.get_queue().fetch_job(job_id)
    if job:
        if job.status == "finished":
            resp = json.dumps(
                {"status": job.status, "progress": job.meta.get('progress'), "zip": job.meta.get('path'),
                 "job_id": job_id, "songsNotDownloaded": job.meta.get('songsNotDownloaded')})
        else:
            resp = json.dumps(
                {"status": job.status, "progress": job.meta.get('progress'), "zip": "ZIP AVAILABLE WHEN FINISHED",
                 "job_id": job_id, "songsNotDownloaded": job.meta.get('songsNotDownloaded')})

    else:
        resp = json.dumps(
            {"status": "NO SUCH JOB", "progress": "NO SUCH JOB", "zip": "NO SUCH JOB", "job_id": "NO SUCH JOB",
             "songsNotDownloaded": "NO SUCH JOB"})

    return HttpResponse(resp)


def cleanqueue(request):
    q = django_rq.get_failed_queue()
    while True:
        job = q.dequeue()
        if not job:
            break
        job.delete()
    return redirect('index')


def fileAndReturnIndex(request, zipFile):
    return render(request, "finished.html", {"zipFile": zipFile})


def serveFile(request, path):
    fileName = path

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename={}'.format(fileName)
    response['X-Accel-Redirect'] = "/protected/{}".format(fileName)
    # os.system('rm -f /home/urban/keefmusic/{}'.format(fileName))
    return response


def download(url):
    # gets list of tracks from spotify playlist
    tracks = getSongs(url)

    tracksNotDownloaded = []

    whatTrackAmIOn = 1

    job = get_current_job(connection=None)

    # for every song in it, download it and print some shit
    for song, info in tracks.items():
        track = Song(info[4], song, info[0], info[1], info[2], info[3])

        # send the folder info with the following line
        if whatTrackAmIOn == 1:
            job.meta['path'] = (track.playlistName + ".zip")
            job.save()

        albumCover = info[3]

        try:
            # update progress

            if whatTrackAmIOn == 1:
                job.meta['progress'] = {"titleAndArtist": track.getTitleAndArtist(), "currentTrack": 0,
                                        "totalTracks": len(tracks), "albumCover": albumCover,
                                        "errorDownloadingSong": "None"}
                job.save()

            else:
                job.meta['progress'] = {"titleAndArtist": track.getTitleAndArtist(), "currentTrack": whatTrackAmIOn,
                                        "totalTracks": len(tracks), "albumCover": albumCover,
                                        "errorDownloadingSong": "None"}
                job.save()

            # sometimes finds back https://www.youtube.com/

            youtubeURL = track.search()
            track.download(youtubeURL)
            track.completeMP3()

            whatTrackAmIOn += 1

        except Exception as e:
            print(str(e))
            job.meta['progress'] = {"titleAndArtist": track.getTitleAndArtist(), "currentTrack": whatTrackAmIOn,
                                    "totalTracks": len(tracks), "albumCover": albumCover,
                                    "errorDownloadingSong": str(e)}
            job.save()
            tracksNotDownloaded.append(song)
            whatTrackAmIOn += 1
            pass

    if len(tracksNotDownloaded) > 0:
        job.meta['songsNotDownloaded'] = tracksNotDownloaded
        job.save()

    turnToZip(output_name=track.playlistName, dir_name=track.playlistName, delete=True)

    print("\nfinished this album/playlist ")
