# youtube_playlist_download

## Allows to download all videos from youtube playlist.

Downloads are multiprosessing, used multiprocessing module.

This program is CLI and requeres two parametrs:

- playlist_url, for example https://www.youtube.com/some_playlist_name;
- dest, where are you download playlist videos.

## Examples
```sh
  python youtube_playlist_download --palylist_url https://www.youtube.com/some_playlist_name --dest /usr/video_folder
```
or
```sh
  python youtube_playlist_download -p https://www.youtube.com/some_playlist_name -d /usr/video_folder
```

For Window dest must be two-braces format: D:\\Users\\CrisisCore.
```sh
  python youtube_playlist_download -p https://www.youtube.com/some_playlist_name -d D:\\Users\\CrisisCore
```
