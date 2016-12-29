import requests
from bs4 import BeautifulSoup
import os
from pytube import YouTube

def get_file_of_urls(palylist_url, path, file_name = "video_list"):
    '''
    :param palylist_url: Write youtube palylist url
    :param path: Write path, where videos will be download, for example "D:\\Users\\CrisisCore"
    :param file_name: Name of file? where links of all playlist video will be stored
    :return:
    '''

    play_list = requests.get(palylist_url)

    video_link_massive = set()

    if play_list.ok:
        html_list = BeautifulSoup(play_list.text, 'html.parser')
        list_a = html_list.body.findAll("a")

        for link in list_a:
            temp = link["href"]
            if "index" in temp:
                if temp not in video_link_massive:
                    video_link_massive.add("https://www.youtube.com" + temp)

    with open(file_name, "wt") as op:
        for el in video_link_massive:
            op.write(el)
            op.write("\n")

    path = path

    if not os.path.exists(path):
        os.mkdir(path)

    with open(file_name, "rt") as op:
        mas = op.readlines()
        for link in mas:
            yt = YouTube(link.rstrip())
            print(yt.get_videos())
            temp_dict = {}
            temp_dict["video_format"] = "mp4"
            if yt.filter(resolution = "720p"):
                temp_dict["fideo_q"] = "720p"
            elif yt.filter(resolution = "480p") and not yt.filter(resolution = "720p"):
                temp_dict["fideo_q"] = "480p"
            elif yt.filter(resolution = "360p") and not yt.filter(resolution = "480p") and not yt.filter(
                    resolution = "720p"):
                temp_dict["fideo_q"] = "360p"
            else:
                temp_dict["fideo_q"] = "240p"
            video = yt.get(extension = temp_dict["video_format"], resolution = temp_dict["fideo_q"])
            video.download(path)
