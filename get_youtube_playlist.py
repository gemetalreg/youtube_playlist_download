import requests
from bs4 import BeautifulSoup
import os
from pytube import YouTube
import argparse
import multiprocessing as mp

def get_links_from_youtube(playlist_url) -> set:
    video_link_set = set()

    play_list = requests.get(playlist_url)

    if play_list.ok:
        html_list = BeautifulSoup(play_list.text, 'html.parser')
        list_a = html_list.body.findAll("a")

        for link in list_a:
            full_link = "https://www.youtube.com" + link["href"]
            full_link_clear = full_link.rstrip()
            if "index" in full_link_clear and full_link_clear not in video_link_set:
                video_link_set.add(full_link_clear)

    return video_link_set

def get_video_format() -> str:
    return "mp4"

def get_video_resolution(youtube: YouTube, video_format) -> str:
    videos = youtube.filter(video_format)
    if len(videos) > 0:
        bes_res_videos = videos[-1]
        return bes_res_videos.resolution
    raise TypeError("choose another video format")

def worker(queue, path):
    while True:
        video = queue.get()

        if video is None:
            break

        video.download(path)

def get_file_of_urls(playlist_url, path):
    '''
    :param playlist_url: Write youtube palylist url, which You want to download
    :param path: Path, where videos will be download, for example "D:\\Users\\CrisisCore"
    :return: None
    '''
    video_link_set = get_links_from_youtube(playlist_url)

    if not os.path.exists(path):
        os.mkdir(path)

    number_of_procs = os.cpu_count() or 2

    queue = mp.Queue()

    for link in video_link_set:
        yt = YouTube(link)

        video_format = get_video_format()

        video_resolution = get_video_resolution(yt, video_format)

        video = yt.get(extension = video_format, resolution = video_resolution)

        queue.put(video)

    for _ in range(number_of_procs):
        queue.put(None)

    procs = []
    
    for _ in range(number_of_procs):
        video_download_process = mp.Process(target = worker, args = (queue, path))
        procs.append(video_download_process)

    for starting_proc in procs:
        starting_proc.start()

    for joining_proc in procs:
        joining_proc.join()

if __name__ == '__main__':
    mp.freeze_support()

    parser = argparse.ArgumentParser()

    parser.add_argument("--playlist_url", "-p",
                        help = "playlist_url what you want to download",
                        nargs = 1)

    parser.add_argument("--dest", "-d",
                        help = "destination, where are you want to download playlist",
                        nargs = 1)

    args = parser.parse_args()

    playlist_url = args.playlist_url[0]

    dest = args.dest[0]

    get_file_of_urls(playlist_url, dest)

    print(f"Downloads end successfully. Your videos in {dest}.")
