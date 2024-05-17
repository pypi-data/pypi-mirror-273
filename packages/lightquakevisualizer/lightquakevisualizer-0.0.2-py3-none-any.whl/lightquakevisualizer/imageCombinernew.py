#!/usr/bin/env python3
from PIL import Image
import argparse
import numpy as np


def white_to_transparency(img: Image.Image) -> Image.Image:
    """Convert white pixels to transparent in an image."""
    x = np.asarray(img.convert("RGBA")).copy()
    x[:, :, 3] = (255 * (x[:, :, :3] != 255).any(axis=2)).astype(np.uint8)
    return Image.fromarray(x)


def compute_j0(i: int, j: int, nrows: int, ncol_per_component: int) -> int:
    """Compute the offset for an image in the combined image."""
    return j * ncol_per_component + i // nrows


def main() -> None:
    """Combine multiple images into a single image with specified columns and relative offset."""
    parser = argparse.ArgumentParser(
        description="Combine multiple images into a single image, with the ability to specify the number of columns and the relative offset (shift ratio) between images"
    )
    parser.add_argument(
        "--inputs", nargs="+", help="filenames to combine", required=True
    )
    parser.add_argument(
        "--relative_offset",
        nargs=2,
        default=[1.0, 1.0],
        help="shift ratio between images (first between rows, second between columns)",
        type=float,
    )
    parser.add_argument(
        "--columns",
        nargs=1,
        default=[1],
        help="number of columns in figure",
        type=int,
    )
    parser.add_argument(
        "--output", nargs=1, help="if not set will be args.filenames[0]", required=True
    )
    parser.add_argument(
        "--keep_white",
        dest="keep_white",
        action="store_true",
        help="do not change white to transparent",
    )

    args = parser.parse_args()

    images: list[Image.Image] = []
    for filename in args.inputs:
        img = Image.open(filename)
        if not args.keep_white:
            img = white_to_transparency(img)
        images.append(img)

    widths, heights = zip(*(img.size for img in images))

    max_width = max(widths)

    width = int(max_width * (1 + args.relative_offset[1] * (args.columns[0] - 1)))
    height = heights[0] + int(
        args.relative_offset[0] * sum(heights[1:]) / args.columns[0]
    )

    new_im = Image.new("RGBA", (width, height))

    nrows = int(np.ceil(len(images) / args.columns[0]))
    offset = int(heights[-1] * args.relative_offset[0])

    for i, im in enumerate(images):
        i0 = i % nrows
        j0 = i // nrows
        offseted_image = Image.new("RGBA", (width, height))
        offseted_image.paste(
            im, (int(max_width * args.relative_offset[1] * j0), offset * i0)
        )
        new_im = Image.alpha_composite(new_im, offseted_image)

    output_filename = args.output[0]
    new_im.save(output_filename)
    print(f"done writing {output_filename}")


if __name__ == "__main__":
    main()
