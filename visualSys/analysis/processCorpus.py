from typing import List
import os
from chardet.universaldetector import UniversalDetector

# 获取文件的编码信息
def get_encode_info(file):
    with open(file, 'rb') as f:
        detector = UniversalDetector()
        for line in f.readlines():
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result['encoding']


def getSection(name:str ,file_name: str, replace_name:dict) -> List[str]:
    # 获取txt文件编码，
    # 若之前以及判断过该书籍的编码，则保存在一个txt文档中
    # 减少判断书籍编码所耗费的大量时间
    if os.path.isfile("./static/book/"+name+"/encode.txt"):
        encode_f = open("./static/book/"+name+"/encode.txt", "r")
        encode_info = encode_f.readlines()
        encode_f.close()
    else:
        encode_info = get_encode_info(file_name)
        new_encode_f = open("./static/book/"+name+"/encode.txt", "w")
        new_encode_f.write(encode_info)
        new_encode_f.close()

    print(encode_info)

    # 根据判断处的编码信息重新打开文件
    f = open(file_name, "r",encoding=str(encode_info),errors='ignore')

    sentence = []
    for line in f.readlines():
        line = line.replace(u'\n', u'').replace(u'\u3000', u'').replace(u'    ',u'')
        if line == '':
            continue
        # 将段落中的旧词替换为新词
        for oldc,newc in replace_name.items():
            line = line.replace(oldc, newc)
        # 用句号来划分不太合理，应使用段落来进行划分
        # line_cut = line.split("。")
        # sentence += line_cut
        # print(line)
        # 段落分
        sentence.append(line)
    return sentence
