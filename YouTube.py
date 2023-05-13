from turtle import delay
from pytube import YouTube
from tkinter import *
from tkinter import filedialog
import threading


# Set the theme color for the GUI
BACKGROUND_COLOR = "#333338"
FONT_COLOR = "#ffff99"

root = Tk()
root.title("YouTube Downloader")
root.geometry("600x380")
root.resizable(False, False)
root.config(bg=BACKGROUND_COLOR)

# Available file formats
formats = [("MP4 files", "*.mp4"), ("MP3 files", "*.mp3")]

# Available video quality options
video_quality_options = ["360p", "720p"]  #   "144p","240p","360p","480p","720p"


def browse():
    directory = filedialog.askdirectory(title="Save video")
    folderLink.delete(0, "end")
    folderLink.insert(0, directory)


def down_yt():
    status.config(text="Status : Downloading", fg="yellow")
    Link = ytLink.get()
    folder = folderLink.get()

    # Select the appropriate file format based on user choice
    file_format = format_var.get()

    streams = YouTube(Link, on_complete_callback=finish).streams

    if file_format == "mp4":
        # Filter for video streams only
        streams = streams.filter(progressive=True, file_extension="mp4")
    else:
        # Filter for audio-only streams first
        audio_streams = streams.filter(only_audio=True, file_extension="mp4")
        if audio_streams:
            streams = audio_streams
        else:
            # If no audio-only streams are available, fallback to video stream
            streams = streams.filter(progressive=True, file_extension="mp4")
            status.config(text="There is no mp3 file available for this link", fg="red")
            delay(delay=1000)
            status.config(text="Downloading mp4 instead", fg="#yellow")

    # Select the appropriate video quality based on user choice
    video_quality = quality_var.get()
    if video_quality:
        streams = streams.filter(res=video_quality)

    # Download the selected video if there are streams available
    if streams:
        try:
            streams.order_by("resolution").desc().first().download(folder)
        except:
            status.config(text="Error downloading video", fg="red")
    else:
        status.config(
            text="No streams available for the selected video, try changing the Quality",
            fg="red",
        )


def paste_url():
    # Get the text from the clipboard
    url = root.clipboard_get()
    # Insert the URL into the Entry field
    ytLink.delete(0, END)
    ytLink.insert(0, url)


def finish(stream=None, Chunk=None, file_handle=None, remaining=None):
    status.config(text="Status : Download completed", fg="#55ff55")


## Logo
yrLabel1 = Label(root, text="You", bg=BACKGROUND_COLOR, fg="red", font=("Arial", 20))
yrLabel1.place(relx=0.45, rely=0.33, anchor="center")
yrLabel2 = Label(root, text="Tube", bg=BACKGROUND_COLOR, fg="white", font=("Arial", 20))
yrLabel2.place(relx=0.55, rely=0.33, anchor="center")
# Logo
ytLogo = PhotoImage(file="D:\\images\\Logo.png").subsample(7)
ytTitle = Label(root, image=ytLogo, bg=BACKGROUND_COLOR)
ytTitle.place(relx=0.5, rely=0.15, anchor="center")

## YouTube link
ytLabel = Label(root, text="YouTube Link", bg=BACKGROUND_COLOR, fg=FONT_COLOR)
ytLabel.place(x=25, y=150)
ytLink = Entry(root, width=50)
ytLink.place(x=140, y=150)
# Paste button
pasteBtn = Button(root, text="  Paste  ", command=paste_url)
pasteBtn.place(x=455, y=148)

## Destination folder
folderLabel = Label(root, text="Destination", bg=BACKGROUND_COLOR, fg=FONT_COLOR)
folderLabel.place(x=25, y=190)
folderLink = Entry(root, width=50)
folderLink.place(x=140, y=190)
# browse button
browseBtn = Button(root, text="Browse", command=browse)
browseBtn.place(x=455, y=188)

# File format selection
formatLabel = Label(root, text="File Format", bg=BACKGROUND_COLOR, fg=FONT_COLOR)
formatLabel.place(x=25, y=225)
format_var = StringVar(value="mp4")
mp4Radio = Radiobutton(
    root,
    text="MP4",
    variable=format_var,
    value="mp4",
    bg=BACKGROUND_COLOR,
    fg="red",
)
mp4Radio.place(x=140, y=225)
# mp3Radio = Radiobutton(
#     root,
#     text="MP3",
#     variable=format_var,
#     value="mp3",
#     bg=BACKGROUND_COLOR,
#     fg="red",
# )
# mp3Radio.place(x=200, y=225)

# Video quality selection
qualityLabel = Label(root, text="Video Quality", bg=BACKGROUND_COLOR, fg=FONT_COLOR)
qualityLabel.place(x=25, y=260)
quality_var = StringVar()
quality_var.set(video_quality_options[0])
qualityDropdown = OptionMenu(root, quality_var, *video_quality_options)
qualityDropdown.config(width=8)
qualityDropdown.place(x=140, y=260)

# Download button
downloadBtn = Button(
    root,
    text="Download",
    command=lambda: threading.Thread(target=down_yt).start(),
    bg="#aa1111",
    fg="#ffffaa",
    font=("Arial", 18),
)
downloadBtn.place(relx=0.55, y=260)

# status
status = Label(
    root,
    text="Status : Ready",
    font="Calibre 10 italic",
    fg=FONT_COLOR,
    bg="#222226",
    anchor="center",
)
status.place(rely=0.98, anchor="sw", relwidth=1)


mainloop()
