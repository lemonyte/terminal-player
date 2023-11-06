# Terminal Player

Play videos and render images in the terminal as text.
Written in pure Python, works on any platform.

https://github.com/lemonyte/terminal-player/assets/49930425/889c2489-9e40-4028-8e88-d7af4b34e785

## Requirements

- [Python 3.9](https://www.python.org/downloads/) or higher
- Packages listed in [`requirements.txt`](requirements.txt)

## Usage

First process a file.

```shell
# Image
python process.py path/to/image.png path/to/processed.dat
# Video
python process.py path/to/video.mp4 path/to/processed.dat --video
```

Use `--width` to set the frame width in columns, and `--video` to process videos.

Then render the file.

```shell
python render.py path/to/processed.dat
```

Use `--fps` to set the desired refresh rate for videos, and `--loop` to play a video on loop.

## License

[MIT License](license.txt)
