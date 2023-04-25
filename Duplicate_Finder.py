from pathlib import Path
from tinytag import TinyTag
from tkinter import filedialog, messagebox

selected_path = filedialog.askdirectory()
folder_path = Path(selected_path)

supported_extensions = ["mp3", "ogg", "wav", "m4a", "flac"]
song_list = []
for song in folder_path.glob("*.*"):
    if song.suffix[1:] in supported_extensions:
        song_list.append(song)

# Check all songs and store duplicates in a list
duplicates = []
song_set = set()
for song in song_list:
    try:
        tag = TinyTag.get(str(song))
        title = tag.title
        artist = tag.artist
        album = tag.album

        if (title, artist, album) in song_set:
            duplicates.append(song)
        else:
            song_set.add((title, artist, album))
    except OSError as e:
        print(f"Error reading file {song}: {e}")
        continue

# Ask the user if they want to delete any of the duplicates found
if duplicates:
    answer_all = False
    if len(song_set) > 1:
        answer_all = messagebox.askyesno("Delete All Duplicates?", "Do you want to delete all duplicate songs in the selected folder?")

    for song in duplicates:
        tag = TinyTag.get(str(song))
        title = tag.title
        artist = tag.artist
        album = tag.album

        print(f"Duplicate song found: {title} - {artist} - {album}")
        if answer_all or messagebox.askyesno("Duplicate Song Found", f"Do you want to delete {song.name}?"):
            song.unlink()
            print(f"{song.name} deleted.")
        else:
            print(f"{song.name} not deleted.")
else:
    print("No duplicate songs found.")
