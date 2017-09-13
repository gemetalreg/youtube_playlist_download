import requests
from bs4 import BeautifulSoup
import os
from pytube import YouTube
import argparse
from multiprocessing import Process, freeze_support

def get_links_from_youtube(palylist_url) -> set:
    video_link_set = set()

    play_list = requests.get(palylist_url)

    if play_list.ok:
        html_list = BeautifulSoup(play_list.text, 'html.parser')
        list_a = html_list.body.findAll("a")

        for link in list_a:
            temp = "https://www.youtube.com" + link["href"]
            if "index" in temp and temp not in video_link_set:
                video_link_set.add(temp)

    return video_link_set

def get_video_format() -> str:
    return "mp4"

def get_video_resolution(youtube: YouTube, video_format) -> str:
    resolutions = ["1080p", "720p", "480p", "360p", "240p"]
    for res in resolutions:
        if youtube.filter(video_format, resolution = res):
            return res
    raise TypeError("choose another video format")

def get_file_of_urls(palylist_url, path):
    '''
    :param palylist_url: Write youtube palylist url, which You want to download
    :param path: Path, where videos will be download, for example "D:\\Users\\CrisisCore"
    :return: None
    '''
    video_link_set = get_links_from_youtube(palylist_url)

    if not os.path.exists(path):
        os.mkdir(path)

    procs = []
    for link in video_link_set:
        yt = YouTube(link.rstrip())

        video_format = get_video_format()

        video_resolution = get_video_resolution(yt, video_format)

        video = yt.get(extension = video_format, resolution = video_resolution)

        video_download_process = Process(target = video.download, args = (path,))
        procs.append(video_download_process)

    for process in procs:
        process.start()

    for process_joinable in procs:
        process_joinable.join()

parser = argparse.ArgumentParser()

parser.add_argument("--palylist_url", "-p",
                    help = "palylist_url what you want to download",
                    nargs = 1)

parser.add_argument("--dest", "-d",
                    help = "destination, where are you want to download playlist",
                    nargs = 1)

args = parser.parse_args()

palylist_url = args.palylist_url[0]

dest = args.dest[0]

if __name__ == '__main__':
    freeze_support()
    get_file_of_urls(palylist_url, dest)
