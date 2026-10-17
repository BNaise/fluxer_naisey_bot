from petpetgif_fix import petpet
from PIL import Image
import io
import math

def make_multi_pet_gif(avatar_byte_list, dest, speed_ms=20):
    individual_frames = []
    for avatar_bytes in avatar_byte_list:
        temp = io.BytesIO()
        petpet.make(avatar_bytes, temp)
        temp.seek(0)

        img = Image.open(temp)
        frames = []
        try:
            while True:
                frames.append(img.copy().convert("RGBA"))
                img.seek(img.tell() + 1)
        except EOFError:
            pass
        individual_frames.append(frames)

    frame_count = min(len(f) for f in individual_frames)

    cols = 3
    rows = math.ceil(len(individual_frames) / cols)

    cell_width = max(f[0].width for f in individual_frames)
    cell_height = max(f[0].height for f in individual_frames)

    canvas_width = cols * cell_width
    canvas_height = rows * cell_height

    combined_frames = []
    for i in range(frame_count):
        canvas = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))

        for user_index, frames in enumerate(individual_frames):
            frame = frames[i]
            row = user_index // cols
            col = user_index % cols

            x = col * cell_width
            y = row * cell_height
            canvas.paste(frame, (x, y), frame)

        combined_frames.append(canvas)

    combined_frames[0].save(
        dest, format="GIF", save_all=True,
        append_images=combined_frames[1:],
        duration=speed_ms, loop=0,
        disposal=2,
    )