from PIL import Image

import os
import urllib
import argparse

ASCII_CHARS = ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']
ASCII_CHARS = ASCII_CHARS[::-1]


def resize(image, new_width=100, ar_multiplier=1.0):
    """
    Resizes an image to match new width and multiplies aspect ratio
    by ar_multiplier (to match line intervals)

    :param ar_multiplier: a float to multiply aspect ratio with
    :param image: image to convert
    :param new_width: new width of the image in chars
    :return:
    """
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height) / float(old_width)
    aspect_ratio *= ar_multiplier

    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)

    return new_image


def grayscalify(image):
    """
    Converts image to grayscale

    :param image: image to convert
    :return: grayscale image
    """
    return image.convert('L')


def modify(image):
    """
    Converts image to ascii art

    :param image: image to convert
    :return: string of ascii art
    """
    bucket_size = 255 // len(ASCII_CHARS) + bool(255 % len(ASCII_CHARS))
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value // bucket_size] for pixel_value in initial_pixels]
    return ''.join(new_pixels)


def do(image, new_width=100):
    """
    Converts to grayscale, then to ascii art

    :param image: image to convert
    :param new_width: new image width
    :return: a text with ascii art
    """
    image = resize(image, new_width=new_width)
    image = grayscalify(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    new_image = [pixels[index:index + new_width] for index in range(0, len_pixels, new_width)]

    return '\n'.join(new_image)


def convert(image_path, result_path, out_width):
    image = None
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Invalid image in path {image_path}, exception: {e}")
        exit(1)

    image = do(image, new_width=out_width)

    with open(result_path, 'w') as f:
        f.write(image)

    print('Done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert image to ASCII art')
    parser.add_argument(
        '-i', '--infile',
        type=str, metavar='PATH',
        help='Image to convert (path or url)',
        required=True,
    )
    parser.add_argument(
        '-o', '--outfile',
        type=str, metavar='PATH',
        help='File to write result in',
        required=True,
    )
    parser.add_argument(
        '-w', '--width',
        type=int, metavar='N',
        help='Width of output in chars',
        default=100,
    )
    args = parser.parse_args()

    infile = args.infile
    outfile = args.outfile
    width = args.width

    if infile.startswith('http://') or infile.startswith('https://'):
        infile, _ = urllib.request.urlretrieve(infile)
    else:
        if not os.path.isfile(infile):
            print('Infile does not exist')
            exit(1)

    convert(infile, outfile, width)
