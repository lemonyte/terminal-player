import argparse
import pickle
import time
from sys import stdout

from pyco import cursor, terminal


def show_image(text: str):
    stdout.write(text)
    stdout.flush()


def play_video(frames: list[str], fps: int):
    cursor.hide()
    frame_height = len(frames[0].split("\n"))
    actual_frame_height = frame_height
    start_y, start_x = cursor.get_position()
    start_time = time.perf_counter()
    frame_num = 0
    frame_total = len(frames)
    try:
        while frame_num < frame_total:
            terminal_size = terminal.get_size()
            frame = frames[frame_num]
            if terminal_size.lines < frame_height:
                actual_frame_height = terminal_size.lines - start_y + 1
                frame = "\n".join(frame.split("\n")[:actual_frame_height])
            cursor.set_position(start_x, start_y)
            show_image(frame)
            time_diff = time.perf_counter() - start_time
            target_time = frame_num / fps
            time_offset = time_diff - target_time
            skip_frames = 0
            if time_offset > 0:
                skip_frames = int(time_offset * fps) + 1
                frame_num += skip_frames
            elif time_offset < -0.1:
                time.sleep(-time_offset - 0.1)
    except KeyboardInterrupt as exc:
        terminal.reset_all()
        cursor.set_position(start_x, start_y + actual_frame_height)
        raise SystemExit() from exc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("-f", "--fps", type=int, default=30)
    parser.add_argument("-l", "--loop", action="store_true")
    args = parser.parse_args()
    with open(args.file, "rb") as file:
        media = pickle.load(file)
    if media[0] == "image":
        show_image(media[1])
    elif media[0] == "video":
        while True:
            play_video(media[1], args.fps)
            if not args.loop:
                break


if __name__ == "__main__":
    main()
