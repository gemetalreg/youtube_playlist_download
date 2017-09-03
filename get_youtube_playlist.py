#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import os
from pytube import YouTube
import threading
import sys

palylist_url = ""
path = ""
file_name = "video_list"

numberOfArgv = len(sys.argv)
if (numberOfArgv < 3):
    print("Usage: " + sys.argv[0] + " must have 2 or 3 args")
    sys.exit(1)

elif (numberOfArgv == 3):
    palylist_url = sys.argv[1]
    path = sys.argv[2]

else:
    palylist_url = sys.argv[1]
    path = sys.argv[2]
    file_name = sys.argv[3]

def get_file_of_urls(palylist_url, path, file_name = "video_list"):
    '''
    :param palylist_url: Write youtube palylist url, which You want to download
    :param path: Path, where videos will be download, for example "D:\\Users\\CrisisCore"
    :param file_name: Name of file, where links of all playlist video will be stored
    :return: pass
    '''

    play_list = requests.get(palylist_url)

    video_link_set = set()

    if play_list.ok:
        html_list = BeautifulSoup(play_list.text, 'html.parser')
        list_a = html_list.body.findAll("a")

        for link in list_a:
            temp = link["href"]
            if "index" in temp and temp not in video_link_set:
                video_link_set.add("https://www.youtube.com" + temp)

    with open(file_name, "wt") as op:
        for el in video_link_set:
            op.write(el)
            op.write("\n")

    path = path

    if not os.path.exists(path):
        os.mkdir(path)

    with open(file_name, "rt") as op:
        mas = op.readlines()

        for link in mas:

            yt = YouTube(link.rstrip())

            temp_dict = {}
            temp_dict["video_format"] = "mp4"

            if yt.filter(resolution = "720p"):
                temp_dict["fideo_q"] = "720p"

            elif yt.filter(resolution = "480p") and not yt.filter(resolution = "720p"):
                temp_dict["fideo_q"] = "480p"

            elif yt.filter(resolution = "360p") and not yt.filter(resolution = "480p") and \
                    not yt.filter(resolution = "720p"):
                temp_dict["fideo_q"] = "360p"

            else:
                temp_dict["fideo_q"] = "240p"

            video = yt.get(extension = temp_dict["video_format"], resolution = temp_dict["fideo_q"])

            # video.download(path)
            threading.Thread(target = video.download, args = [path]).start()


if __name__ == '__main__':
    get_file_of_urls(palylist_url, path, file_name)
