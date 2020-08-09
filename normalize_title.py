import re
import jaconv

def normalize(title):
    title = jaconv.normalize(title, 'NFKC')
    # title = jaconv.z2h(title, kana=False, digit=True, ascii=True)
    title = title.lower()
    title = "".join(re.findall(r'[a-z0-9ぁ-んァ-ヴ一-龥()!\?:@]', title))
    return title

def main():
    title = u'あアｱ行aａ１"”（）！＠?:～ー~-A9'
    title = normalize(title)
    print(title)

if __name__=='__main__':
    main()