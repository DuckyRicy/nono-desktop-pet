from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets"

# (output name, source image, crop box)
SPRITES = [
    ("idle.png", "微信图片_20260728153304_1478_145.jpg", (320, 40, 720, 440)),
    ("happy.png", "微信图片_20260728153303_1477_145.jpg", (0, 315, 355, 665)),
    ("surprised.png", "微信图片_20260728153303_1477_145.jpg", (335, 0, 735, 335)),
    ("zoom.png", "微信图片_20260728153303_1477_145.jpg", (350, 320, 730, 605)),
    ("tired.png", "微信图片_20260728153304_1478_145.jpg", (350, 1120, 715, 1440)),
    ("curious.png", "微信图片_20260728153304_1478_145.jpg", (0, 390, 360, 770)),
    ("box.png", "微信图片_20260728153304_1478_145.jpg", (320, 370, 730, 790)),
    ("nervous.png", "微信图片_20260728153304_1478_145.jpg", (700, 720, 1080, 1115)),
    ("lotus.png", "微信图片_20260728153304_1478_145.jpg", (0, 1080, 370, 1440)),
    (
        "wave.png",
        "Camera_1040g3k0321jjcnecna005pm7vj57e2i3c13ljg0_CocoAI_20260719_173028_2.png",
        (0, 0, 500, 509),
    ),
    (
        "tilted.png",
        "Camera_1040g3k0321jjcnecna005pm7vj57e2i3c13ljg0_CocoAI_20260719_173029_3.png",
        (0, 0, 606, 500),
    ),
    (
        "measure.png",
        "Camera_1040g3k0321jjcnecna005pm7vj57e2i3c13ljg0_CocoAI_20260719_173030_8.png",
        (0, 0, 500, 561),
    ),
    (
        "pout.png",
        "Camera_1040g3k0321jjcnecna005pm7vj57e2i3c13ljg0_CocoAI_20260719_173032_12.png",
        (0, 0, 515, 500),
    ),
]

# White source-background islands enclosed by an arm/handle. Coordinates refer
# to the normalized 280x280 output, after resizing.
ENCLOSED_BACKGROUND_SEEDS = {
    "nervous.png": [(50, 75)],
    "surprised.png": [(242, 136)],
    "tired.png": [(242, 164)],
}


def is_background(pixel):
    r, g, b, _ = pixel
    # The source is JPEG, so its white backdrop contains slightly grey and
    # coloured compression pixels around the inked outline.
    return r > 205 and g > 205 and b > 205 and max(r, g, b) - min(r, g, b) < 38


def remove_edge_background(image):
    image = image.convert("RGBA")
    width, height = image.size
    pixels = image.load()
    queue = deque()
    seen = set()

    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))

    while queue:
        x, y = queue.popleft()
        if (x, y) in seen or not is_background(pixels[x, y]):
            continue
        seen.add((x, y))
        pixels[x, y] = (255, 255, 255, 0)
        if x:
            queue.append((x - 1, y))
        if x + 1 < width:
            queue.append((x + 1, y))
        if y:
            queue.append((x, y - 1))
        if y + 1 < height:
            queue.append((x, y + 1))

    # Sprite sheets sometimes leave a small piece of a neighboring pose in the
    # crop. Keep only the largest connected opaque shape: the character.
    opaque = {(x, y) for y in range(height) for x in range(width) if pixels[x, y][3]}
    components = []
    while opaque:
        seed = opaque.pop()
        component = {seed}
        queue = deque([seed])
        while queue:
            x, y = queue.popleft()
            for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if neighbor in opaque:
                    opaque.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        components.append(component)
    largest = max(components, key=len)
    for component in components:
        if component is not largest:
            for x, y in component:
                pixels[x, y] = (255, 255, 255, 0)

    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox:
        image = image.crop(bbox)
    image.thumbnail((255, 255), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (280, 280), (0, 0, 0, 0))
    x = (280 - image.width) // 2
    y = 280 - image.height
    canvas.alpha_composite(image, (x, y))

    # Tk's Windows transparent-color window blends semi-transparent PNG edge
    # pixels with its magenta key color before removing the background. That
    # creates a bright purple fringe. Use a binary alpha edge for this renderer.
    alpha = canvas.getchannel("A").point(lambda value: 255 if value >= 96 else 0)
    canvas.putalpha(alpha)

    # Clean again after resizing: a nearby pose may have survived the loose
    # JPEG-background flood but will now be a clearly separate island.
    pixels = canvas.load()
    opaque = {
        (x, y)
        for y in range(canvas.height)
        for x in range(canvas.width)
        if pixels[x, y][3]
    }
    components = []
    while opaque:
        seed = opaque.pop()
        component = {seed}
        queue = deque([seed])
        while queue:
            px, py = queue.popleft()
            for neighbor in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                if neighbor in opaque:
                    opaque.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        components.append(component)
    largest = max(components, key=len)
    for component in components:
        if component is not largest:
            for px, py in component:
                pixels[px, py] = (255, 255, 255, 0)

    # Add a deliberate, even 2 px white keyline so nono stays readable on dark
    # desktops. Binary alpha avoids reintroducing the magenta key-color fringe.
    subject_alpha = canvas.getchannel("A")
    expanded_alpha = subject_alpha.filter(ImageFilter.MaxFilter(5))
    outline_alpha = ImageChops.subtract(expanded_alpha, subject_alpha)

    # Only outline the outside silhouette. Transparent gaps enclosed by an arm
    # or handle stay transparent instead of receiving a white inner rim.
    external = Image.new("L", canvas.size, 0)
    external_pixels = external.load()
    alpha_pixels = subject_alpha.load()
    queue = deque()
    for px in range(canvas.width):
        queue.append((px, 0))
        queue.append((px, canvas.height - 1))
    for py in range(canvas.height):
        queue.append((0, py))
        queue.append((canvas.width - 1, py))
    while queue:
        px, py = queue.popleft()
        if external_pixels[px, py] or alpha_pixels[px, py]:
            continue
        external_pixels[px, py] = 255
        if px:
            queue.append((px - 1, py))
        if px + 1 < canvas.width:
            queue.append((px + 1, py))
        if py:
            queue.append((px, py - 1))
        if py + 1 < canvas.height:
            queue.append((px, py + 1))
    outline_alpha = ImageChops.multiply(outline_alpha, external)

    outlined = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    outlined.putalpha(outline_alpha)
    outlined.alpha_composite(canvas)
    canvas = outlined
    return canvas


def clear_enclosed_background(image, seeds):
    pixels = image.load()
    width, height = image.size
    for seed in seeds:
        queue = deque([seed])
        seen = set()
        while queue:
            x, y = queue.popleft()
            if (x, y) in seen or not (0 <= x < width and 0 <= y < height):
                continue
            seen.add((x, y))
            r, g, b, alpha = pixels[x, y]
            if not alpha or min(r, g, b) < 180 or max(r, g, b) - min(r, g, b) > 45:
                continue
            pixels[x, y] = (255, 255, 255, 0)
            queue.extend(((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))
    return image


def add_inner_outline(image):
    """Add a white keyline only around enclosed transparent holes."""
    subject_alpha = image.getchannel("A")
    alpha_pixels = subject_alpha.load()
    width, height = image.size

    external = Image.new("L", image.size, 0)
    external_pixels = external.load()
    queue = deque()
    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))
    while queue:
        x, y = queue.popleft()
        if external_pixels[x, y] or alpha_pixels[x, y]:
            continue
        external_pixels[x, y] = 255
        if x:
            queue.append((x - 1, y))
        if x + 1 < width:
            queue.append((x + 1, y))
        if y:
            queue.append((x, y - 1))
        if y + 1 < height:
            queue.append((x, y + 1))

    transparent = ImageChops.invert(subject_alpha)
    enclosed = ImageChops.subtract(transparent, external)
    expanded = subject_alpha.filter(ImageFilter.MaxFilter(5))
    inner_outline_alpha = ImageChops.multiply(
        ImageChops.subtract(expanded, subject_alpha), enclosed
    )
    inner_outline = Image.new("RGBA", image.size, (255, 255, 255, 0))
    inner_outline.putalpha(inner_outline_alpha)
    image.alpha_composite(inner_outline)
    return image


def main():
    OUT.mkdir(exist_ok=True)
    for output_name, source_name, crop_box in SPRITES:
        source = Image.open(ROOT / source_name)
        sprite = remove_edge_background(source.crop(crop_box))
        sprite = clear_enclosed_background(
            sprite, ENCLOSED_BACKGROUND_SEEDS.get(output_name, ())
        )
        sprite = add_inner_outline(sprite)
        if output_name == "zoom.png":
            # The next-row bee touches this pose at the very bottom of the
            # source sheet. Remove its remaining yellow tip.
            sprite.paste((255, 255, 255, 0), (0, 273, sprite.width, sprite.height))
        sprite.save(OUT / output_name)
        print(f"created {output_name}")


if __name__ == "__main__":
    main()
