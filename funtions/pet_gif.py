from petpetgif_fix import petpet
from PIL import Image
import io

MIN_SPEED_MS = 20
def make_pet_gif(source, dest, speed_ms=20):
    speed_ms = max(speed_ms, MIN_SPEED_MS)

    temp = io.BytesIO()
    petpet.make(source, temp)
    temp.seek(0)

    img = Image.open(temp)
    frames = []
    try:
        while True:
            frames.append(img.copy())
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    frames[0].save(
        dest, format="GIF", save_all=True,
        append_images=frames[1:], duration=speed_ms, loop=0,disposal=2,
    )