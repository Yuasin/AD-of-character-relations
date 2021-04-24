import os
import jieba

print(os.getcwd())

# 原始编码，GBK
f = open("../corpus.txt", "r", encoding="GBK")
# f = open("../corpus.txt", "r", encoding="GBK")
print(f.read())


