from typing import List

from chardet.universaldetector import UniversalDetector


def get_encode_info(file):
    with open(file, 'rb') as f:
        detector = UniversalDetector()
        for line in f.readlines():
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result['encoding']


def getSection(file_name: str) -> List[str]:
    # 获取txt文件编码
    # encode_info = get_encode_info(file_name)
    # print(encode_info)
    #
    # f = open(file_name, 'rb')
    # file_content = f.read()
    # file_decode = file_content.decode(encode_info,'ignore')
    # file_encode = file_decode.encode('GBK','ignore')
    # new_file_name = 'encodeCorpus .txt'
    # with open(new_file_name, 'wb') as f:
    #     f.write(file_encode)

    # 识别为GB2312的时候需要注意，编码识别只识别文件前100行
    # 后续文件可能存在GBK收录但GB2312未收录的字符
    # 所以手动向上把编码集扩大
    # if code_format == 'GB2312':
    #     code_format = 'GBK'

    # 以写入的编码重新打开文件
    f = open(file_name, "r",encoding='UTF-8-SIG',errors='ignore')

    sentence = []
    for line in f.readlines():
        line = line.replace(u'\n', u'').replace(u'\u3000', u'').replace(u'    ',u'')
        if line == '':
            continue
        # 用句号来划分太不合理了，应该用段落来进行划分
        # line_cut = line.split("。")
        # sentence += line_cut
        # print(line)
        # 段落分
        sentence.append(line)
    return sentence
