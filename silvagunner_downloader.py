import tkinter as tk
import re
import traceback
from io import BytesIO

import mock
import ffmpeg

# pytube patch
from pytube.cipher import get_throttling_function_code


def patched_throttling_plan(js: str):
    """Patch throttling plan, from https://github.com/pytube/pytube/issues/1498"""
    raw_code = get_throttling_function_code(js)

    transform_start = r"try{"
    plan_regex = re.compile(transform_start)
    match = plan_regex.search(raw_code)

    # transform_plan_raw = find_object_from_startpoint(raw_code, match.span()[1] - 1)
    transform_plan_raw = js

    # Steps are either c[x](c[y]) or c[x](c[y],c[z])
    step_start = r"c\[(\d+)\]\(c\[(\d+)\](,c(\[(\d+)\]))?\)"
    step_regex = re.compile(step_start)
    matches = step_regex.findall(transform_plan_raw)
    transform_steps = []
    for match in matches:
        if match[4] != "":
            transform_steps.append((match[0], match[1], match[4]))
        else:
            transform_steps.append((match[0], match[1]))

    return transform_steps


# create the window
window = tk.Tk()
window.title("SilvaGunner Downloader")
window.resizable(False, False)
window.geometry("450x200")
window.iconbitmap("icon.ico")

# make window appear in the center of the screen
window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry("{}x{}+{}+{}".format(width, height, x, y - 100))

# create the label
label = tk.Label(window, text="SilvaGunner Downloader", font=("Arial Black", 20), pady=10)
label.pack()

description = tk.Label(window, text="Enter the URL of the video you want to download and auto-format:")
description.pack()

warningtext = tk.Label(window, text="", fg="red")
warningtext.pack()

# create the entry
entry = tk.Entry(window, width=50, border=2)
entry.pack(fill=tk.X, padx=10)


# https://www.youtube.com/watch?v=CGvj-PrLNf8
def download():
    if entry.get() == "":
        warningtext.config(text="Please enter a URL", fg="red")
        return
    try:
        with mock.patch("pytube.cipher.get_throttling_plan", patched_throttling_plan):
            from pytube import YouTube

            v = YouTube(entry.get().strip())
            if v.channel_id != "UC9ecwl3FTG66jIKA9JRDtmg":
                warningtext.config(text="This is not a SilvaGunner video\nIf it is, retry", fg="red")
                return

            buffer = BytesIO()
            v.streams.get_highest_resolution().stream_to_buffer(buffer)
            buffer.seek(0)

            # ffmpeg buffer to mp3
            stream = ffmpeg.input("pipe:", format="mp4")
            stream = ffmpeg.output(
                stream,
                "{}.mp3".format(v.title),
                format="mp3",
                acodec="libmp3lame",
                ac=2, ar="44100",
                loglevel="quiet",
                **{
                    "metadata:g:0": "title={}".format(v.title.split(" - ")[0]),
                    "metadata:g:1": "artist=SilvaGunner",
                    "metadata:g:2": "album={}".format(v.title.split(" - ")[1]),
                    "metadata:g:3": "album_artist=SilvaGunner"
                }
            )
            ffmpeg.run(stream, input=buffer.read())

            warningtext.config(text="{}\nDownloaded successfully".format(v.title), fg="green")
    except Exception as e:
        if "ffmpeg" in str(e):
            warningtext.config(text="FFMPEG Error\nFile possibly already exists", fg="red")
        else:
            warningtext.config(text="Invalid URL\n{}".format(e), fg="red")
        traceback.print_exc()


# create the button
button = tk.Button(window, text="Download", command=download, height=1, width=10, font=("Arial", 15), bg="#F587D9", fg="white")
button.pack(pady=10, expand=True)

# run the application
window.mainloop()


def on_closing():
    window.destroy()
