import argparse
import pickle
import time
from functools import partial
from multiprocessing import Pool

import cv2
import numpy


def pixelate(image: cv2.Mat, /, width: int):
    """Convert an image to a 2-dimensional array of RGB tuples.

    The image is split into tiles, where `width` is the number of tiles in a row.
    The average color of each tile is calculated and is used to represent a pixel.
    """
    image_height, image_width = image.shape[0], image.shape[1]
    tile_size = image_width // width
    pixels = []
    for lower_y in range(0, image_height, tile_size * 2):
        upper_y = lower_y + tile_size
        row = []
        for lower_x in range(0, image_width, tile_size):
            upper_x = lower_x + tile_size
            tile1 = image[lower_y:upper_y, lower_x:upper_x]
            pixel1 = numpy.average(tile1, axis=(1, 0)).astype(numpy.uint8)
            if upper_y < image_height:
                upper_y2 = upper_y + tile_size
                tile2 = image[lower_y:upper_y2, lower_x:upper_x]
                pixel2 = numpy.average(tile2, axis=(1, 0)).astype(numpy.uint8)
            else:
                pixel2 = (0, 0, 0)
            row.append((tuple(pixel1), tuple(pixel2)))
        pixels.append(row)
    return pixels


def pixels_to_text(pixels: list, /) -> str:
    pixel_template = (
        "\x1b[48;2;{background_red};{background_green};{background_blue}m"
        "\x1b[38;2;{foreground_red};{foreground_green};{foreground_blue}m▀\x1b[0m"
    )
    text = ""
    for row in pixels:
        for foreground, background in row:
            text += pixel_template.format(
                foreground_red=foreground[0],
                foreground_green=foreground[1],
                foreground_blue=foreground[2],
                background_red=background[0],
                background_green=background[1],
                background_blue=background[2],
            )
        text += "\n"
    return text


def process_image(image: cv2.Mat, /, width: int) -> str:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = pixelate(image, width)
    text = pixels_to_text(pixels)
    return text


def process_video(video: cv2.VideoCapture, /, width: int) -> list[str]:
    success, image = video.read()
    partial_process_image = partial(process_image, width=width)
    print("Processing video...")
    start_time = time.time()
    images = []
    while success:
        images.append(image)
        success, image = video.read()
    with Pool() as pool:
        frames = pool.map(partial_process_image, images)
    print(f"Finished processing in {time.time() - start_time} seconds.")
    return frames


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("output")
    parser.add_argument("-c", "--width", type=int, default=80)
    parser.add_argument("-v", "--video", action="store_true")
    args = parser.parse_args()
    if args.video:
        media = process_video(cv2.VideoCapture(args.file), width=args.width)
        media_type = "video"
    else:
        media = process_image(cv2.imread(args.file), width=args.width)
        media_type = "image"
    with open(args.output, "wb") as file:
        pickle.dump(
            {"media": media, "media_type": media_type},
            file,
        )


if __name__ == "__main__":
    main()
