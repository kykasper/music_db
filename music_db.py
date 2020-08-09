import os
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
import pandas as pd
import sqlite3
import config

# ['albumartist', 'artist', 'album', 'title', source_filepath]を返す
def getTagData(curdir, file):
    ext = file.rsplit(".", 1)[-1]
    source_filepath = os.path.join(curdir, file)
    res = ["", "", "", "", source_filepath]
    tags = None
    if ext == 'mp3':
        tags = EasyID3(source_filepath)
    elif ext == 'flac':
        tags = FLAC(source_filepath)
    else:
        print("ext : "+ext)
        print(source_filepath)
        print("*"*20)
        return tags
        
    #  'artist'があったら 'albumartist'タグ
    if ('artist' in tags):
        res[1] = tags['artist'][0]
    else:
        res[1] = tags['albumartist'][0]
        
    # 'albumartist' があったら 'artist'タグ
    if ('albumartist' in tags):
        res[0] = tags['albumartist'][0]
    else:
        res[0] = tags['artist'][0]
    res[2] = tags['album'][0]
    res[3] = tags['title'][0]
    
    return res


conn = sqlite3.connect('music.sqlite3')
c = conn.cursor()
# c.execute('create table songs(id integer, albumartist text, artist text, album text, songname text,  path text)')

id = 0
source_path = config.MUSIC_DIRECTORY
for curdir, dirs, files in os.walk(source_path):
    for file in files:
        # print(curdir, file)
        # ext = file.rsplit(".", 1)[-1]
        # source_filepath = os.path.join(curdir, file)
        tags = getTagData(curdir, file)
        if tags is None: continue
        data = [id, *tags]
        # for d in data:
        #     print(d)
        # print("="*20)
        c.execute("INSERT INTO songs VALUES (?,?,?,?,?,?)", tuple(data) )
        id+=1