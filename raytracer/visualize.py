import struct
import zlib
from typing import List

from raytracer.linalg import Vec3


def save_ppm(img: List[List[Vec3]], filename: str):
    f = open(filename, "w")
    f.write(f"P3 {len(img[0])} {len(img)} 255\n")
    # f.write("# Generated by raytracer\n")
    for i in range(len(img)):
        for j in range(len(img[0])):
            f.write(
                f"{int(img[i][j].x * 255)} {int(img[i][j].y * 255)} {int(img[i][j].z * 255)}\n"
            )
    f.close()


def write_png(buf: bytes, width: int, height: int) -> bytes:
    # https://stackoverflow.com/a/19174800/14277568

    width_byte_4 = width * 4
    raw_data = b"".join(
        b"\x00" + buf[span : span + width_byte_4]
        for span in range((height - 1) * width_byte_4, -1, -width_byte_4)
    )

    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return (
            struct.pack("!I", len(data))
            + chunk_head
            + struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head))
        )

    return b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            png_pack(b"IHDR", struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
            png_pack(b"IDAT", zlib.compress(raw_data, 9)),
            png_pack(b"IEND", b""),
        ]
    )


def save_png(img: List[List[Vec3]], filename: str):
    flat = []
    for row in reversed(img):
        flat.extend([c.to_abgr() for c in row])

    buf = b"".join([struct.pack("<I", i32) for i32 in flat])
    data = write_png(buf, len(img[0]), len(img))
    with open(filename, "wb") as f:
        f.write(data)
