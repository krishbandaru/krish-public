""" 
Script to copy all files referenced in an iTunes playlist to a new directory.  I used this to explicitly copy music files from my main library to my Plex server.
"""

import os
import re
from pathlib import Path

# Change these two to match your actual names
ITUNES_FILENAME="FullPathToExportedPlaylistFile.m3u8"
DST_ROOT_FOLDER="FullPathToDestinationDirectory"
song_list=[]

if not os.path.exists(ITUNES_FILENAME):
    print("**Source playlist file not found.")
    exit()

if not os.path.exists(DST_ROOT_FOLDER):
    print("**Destination not found.")
    exit()


def getSongList(filename):
    count=0
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("#"):
                pass
            else:
                song_list.append(line.strip())
                count += 1
    return count,song_list

# Helps not have to do a lot of 
# src_file_path = src_file_path.replace("'","\\'")"
def escape_non_alphanumeric_chars(string):
    escaped_string = re.sub(r'([^a-zA-Z0-9])', r'\\\1', string)
    return escaped_string


src_count,song_list = getSongList(ITUNES_FILENAME)

file_summary=f"{src_count} music files extracted from {ITUNES_FILENAME}"
file_summary_len=len(file_summary)
print(file_summary_len*'=')
print(file_summary)
print(file_summary_len*'=')


"""
Sample entry
/Users/user/Music/Music/Media.localized/Music/Artist/Album/01 Song.m4a
"""
good_count = 0
bad_count = 0
error_list = []
ret=1

for src_file_path in song_list:
    # Split on '/' so don't have to do successive os.path.split() to 
    # extract multiple pieces of the path
    head_tail = src_file_path.split("/")
    num_pieces = len(head_tail)
    song_name = head_tail[num_pieces-1]
    album_name = head_tail[num_pieces-2]
    artist_name = head_tail[num_pieces-3]

    # I really like to keep my existing full file paths so extract them from 
    # the source path instead of recreating them from the file tags, assuming 
    # they're there.
    dst_album_path = os.path.join(DST_ROOT_FOLDER,artist_name,album_name)
    dst_file_path = os.path.join(dst_album_path,song_name)

    path = Path(dst_album_path)
    if not path.exists():
        print(f"Creating dir: {dst_album_path}")
        path.mkdir(parents=True, exist_ok=True)

    src_file_path = escape_non_alphanumeric_chars(src_file_path)
    dst_file_path = escape_non_alphanumeric_chars(dst_file_path)
    
    copying_str = f"Copying {src_file_path} --> {dst_file_path}\n"
    print(copying_str)
    # Use rsync so that successive runs only process updates
    cmd=f"rsync -ahiH --delete --exclude '@eaDir' --exclude '.DS_Store' --no-perms --delete {src_file_path} {dst_file_path}"
    print(f"Executing {cmd}")

    ret = os.system(cmd)
    if ret==0:
        good_count += 1
    else:
        bad_count += 1
        error_list.append(cmd)

print(error_list)
print(f"Good count: {good_count}\nBad count: {bad_count}")

