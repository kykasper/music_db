import os
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
import pandas as pd
import sqlite3
import normalize_title
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

class MusicDB():
    def __init__(self, db_path):
        print('music db. name is {}'.format(db_path))
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()
    
    def close(self):
        self.conn.close()
        print('db is closed')

    def count_db(self):
        self.c.execute('select count(*) from songs;')
        result = self.c.fetchall()
        #結果は リスト、タプル型で出力される => [(5,)]
        print (result[0][0])
        return result[0][0]

    # 最初にdbに情報を入れる時に使用
    def initialize(self):
        print('initialize db.')
        if self.count_db() > 0:
            print('db data exists')
            return 
        self.c.execute(
            'create table songs('
            'id integer,'
            'albumartist text,'
            'artist text,'
            'album text,'
            'songname text,'
            'path text,'
            'normalized_songname text)'
        )
        id = 0
        source_path = config.MUSIC_DIRECTORY
        for curdir, dirs, files in os.walk(source_path):
            for file in files:
                tags = getTagData(curdir, file)
                if tags is None: continue
                n_title = normalize_title.normalize(tags[3])
                data = [id, *tags, n_title]
                self.c.execute("INSERT INTO songs VALUES (?,?,?,?,?,?,?)", tuple(data) )
                id+=1
        self.conn.commit()
    
    # 曲の追加をしたときに使用
    def update(self):
        pass

    def make_playlist_by_title(self, name, title_filepath):
        print('make_playlist_by_title')
        with open(title_filepath, encoding = 'UTF-8') as f:
            title_list = list(f.read().splitlines())

        # df = pd.DataFrame(columns=['artist', 'songname'])
        df = pd.DataFrame(columns=['path'])
        for title in title_list:
            """
            # que = 'SELECT artist,songname FROM songs WHERE normalized_songname = "onestep"'
            que = 'SELECT artist,songname FROM songs WHERE normalized_songname = ?'
            print(que)
            print(title)
            self.c.execute(que, (title, ))
            result = self.c.fetchall()
            for d in result:
                print(d)
            """
            # que = 'SELECT artist,songname FROM songs WHERE normalized_songname = ? and album LIKE "%THE IDOLM@STER%"'
            que = 'SELECT path FROM songs WHERE normalized_songname = ? and album LIKE "%THE IDOLM@STER%"'
            res_df = pd.read_sql_query(que, self.conn, params=(title,))
            print(res_df)
            df = pd.concat([df, res_df])
        df.to_csv(name, header=False, index=False, sep='\t')
        print('end')

    def make_playlist_by_imas(self, name, title_filepath, cv_filepath):
        print('make_playlist_by_imas')
        with open(title_filepath, encoding = 'UTF-8') as f:
            title_list = list(f.read().splitlines())
        cv_list = pd.read_csv(cv_filepath, encoding = 'UTF-8')

        print('end')
        pass

    def make_playlist_by_que(self, name, que):
        print('make_playlist_by_que')
        df = pd.read_sql_query(que, self.conn)
        df.to_csv(name, header=False, index=False)
        print('end')

    def show_db_by_que(self, que):
        self.c.execute(que)
        data = self.c.fetchall()
        # 中身を全て取得するfetchall()を使って、printする。
        for d in data:
            print(d)

def main():
    db_path = 'music.sqlite3'
    db = MusicDB(db_path)
    name = 'test2.m3u8'
    # db.initialize()
    # que = 'SELECT normalized_songname FROM songs WHERE artist LIKE "%我那覇%"'
    # db.show_db_by_que(que)
    # db.make_playlist_by_que(name, que)
    title_filepath = 'normal_imas_radio_songs.csv'
    db.make_playlist_by_title(name, title_filepath)
    db.close()

if __name__=='__main__':
    main()