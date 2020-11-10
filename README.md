# youtube_playlist_download

## Allows to download all videos from youtube playlist.

## Installations
```sh
git clone https://github.com/gemetalreg/youtube_playlist_download
cd youtube_playlist_download
```
## Usage
This program is CLI and requires two parameters (flags):

- playlist_url, for example https://www.youtube.com/some_playlist_name;
- dest, where are you download playlist videos.

```sh
python youtube_playlist_download.py --playlist_url https://www.youtube.com/some_playlist_name --dest /usr/video_folder
```
or
```sh
  python youtube_playlist_download.py -p https://www.youtube.com/some_playlist_name -d /usr/video_folder
```

For Window dest must be two-braces format:
```sh
  python youtube_playlist_download.py -p https://www.youtube.com/some_playlist_name -d D:\\Users\\CrisisCore
```
Downloads are multiprosessing, used [multiprocessing](https://docs.python.org/3.6/library/multiprocessing.html) module.

## License
youtube_playlist_download is released under the [MIT License](https://github.com/gemetalreg/youtube_playlist_download/blob/master/LICENSE).
