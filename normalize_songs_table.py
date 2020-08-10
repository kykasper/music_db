import pandas as pd
import normalize_title

def normalize_songs_table(filepath):
    names = None
    with open(filepath, encoding = 'UTF-8') as f:
        # 確認用
        """
        for s in f.readlines():
            print(s, normalize_title.normalize(s))
        """
        # 改行を除いて特定文字だけ抽出
        l_strip = [normalize_title.normalize(s) for s in f.readlines() if (s != '\n')]
        # ～曲の行を削除
        l_strip = [s for s in l_strip if s[-1] != '曲']
        # oo oo(oo_oo)となっている曲の後半のカッコを削除
        l_strip = [s.split('(')[0] if s[-1] == ')' else s for s in l_strip]
        names = pd.DataFrame(l_strip)
        
    names.to_csv("normal_" + filepath, header=False, index=False)
    
if __name__ == '__main__':
    import os

    path = os.getcwd()

    print(path)
    # filepath = r"C:\Users\Yuto\Documents\PythonScripts\getPlaylist\imas_songs.csv"
    filepath = r"imas_radio_songs.csv"
    normalize_songs_table(filepath)