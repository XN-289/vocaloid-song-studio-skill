from __future__ import annotations

from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFilter


SIZE = 1254
ROOT = Path(__file__).resolve().parent


def vertical_gradient(size: int, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    base = Image.new("RGB", (1, size))
    for y in range(size):
        amount = y / (size - 1)
        color = tuple(round(top[i] + (bottom[i] - top[i]) * amount) for i in range(3))
        base.putpixel((0, y), color)
    return base.resize((size, size))


def add_grain(image: Image.Image, amount: int = 10) -> None:
    rng = random.Random(7301)
    noise = Image.effect_noise((image.width, image.height), amount).convert("L")
    image.paste(Image.blend(image, Image.merge("RGB", (noise, noise, noise)), 0.035), (0, 0))


def main() -> None:
    clinical = vertical_gradient(SIZE, (247, 250, 253), (215, 226, 237))
    fantasy = vertical_gradient(SIZE, (16, 23, 58), (67, 25, 91))
    cover = Image.new("RGB", (SIZE, SIZE))
    cover.paste(clinical, (0, 0))

    fracture = Image.new("L", (SIZE, SIZE), 0)
    fracture_draw = ImageDraw.Draw(fracture)
    fracture_draw.polygon(
        [(730, -60), (892, -60), (604, SIZE + 60), (438, SIZE + 60)],
        fill=255,
    )
    fracture = fracture.filter(ImageFilter.GaussianBlur(52))
    cover = Image.composite(fantasy, cover, fracture)

    draw = ImageDraw.Draw(cover, "RGBA")

    for x, y, radius, alpha in [
        (790, 220, 5, 205),
        (884, 339, 3, 175),
        (969, 458, 4, 190),
        (841, 571, 3, 165),
        (1019, 648, 5, 185),
        (919, 781, 3, 160),
        (1084, 868, 4, 175),
    ]:
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(216, 247, 255, alpha))

    for y in [188, 384, 580, 776, 972]:
        draw.ellipse((96, y - 26, 148, y + 26), fill=(232, 240, 247, 105))
        draw.ellipse((108, y - 18, 136, y + 18), fill=(252, 255, 255, 150))

    glow = Image.new("RGB", (SIZE, SIZE), (0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for width, color in [
        (70, (18, 66, 105)),
        (38, (33, 137, 184)),
        (18, (104, 233, 255)),
        (7, (237, 252, 255)),
    ]:
        glow_draw.line((817, -40, 532, SIZE + 40), fill=color, width=width)
    glow = glow.filter(ImageFilter.GaussianBlur(9))
    cover = Image.blend(cover, Image.composite(glow, cover, fracture), 0.92)

    draw = ImageDraw.Draw(cover, "RGBA")
    draw.arc((432, 760, 832, 1010), 205, 331, fill=(226, 73, 159, 185), width=17)
    draw.arc((444, 772, 820, 998), 205, 331, fill=(255, 149, 224, 110), width=6)
    draw.line((407, 922, 936, 748), fill=(226, 242, 250, 62), width=3)

    vignette = Image.new("L", (SIZE, SIZE), 0)
    vignette_draw = ImageDraw.Draw(vignette)
    vignette_draw.ellipse((-260, -260, SIZE + 260, SIZE + 260), fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(180))
    shadow = vertical_gradient(SIZE, (5, 9, 20), (18, 12, 28))
    cover = Image.composite(cover, Image.blend(cover, shadow, 0.42), vignette)

    add_grain(cover)
    cover.save(ROOT / "cover.png", optimize=True)


if __name__ == "__main__":
    main()
