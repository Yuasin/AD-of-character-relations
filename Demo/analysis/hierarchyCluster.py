# import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
import math
import pypinyin
from matplotlib import pyplot as plt
import itertools
import numpy as np

def cluster_hierarchy(nodes: dict, edges: dict):
    nodes_sorted = sorted(nodes.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    matrix_length = len(nodes_sorted)
    names = []
    adjacency_matrix = []
    similarity_matrix = []

    # 构建人物序列
    for i in range(0, matrix_length):
        names.append(nodes_sorted[i][0])

    # 构建邻接矩阵
    for row in range(0, matrix_length):
        adjacency_matrix.append([])
        source = nodes_sorted[row][0]
        for col in range(0, matrix_length):
            target = names[col]
            if row == col:
                # 此时等于该人物的出现频次
                value = nodes_sorted[row][1]
            else:
                # edges中可能没有相对应到改人的边
                if target not in edges[source]:
                    value = 0
                else:
                    value = edges[source][target]
            adjacency_matrix[row].append(value)

    # 计算相似矩阵,使用 Ochiia 系数将共词矩阵转换为相关矩阵
    for row in range(0, matrix_length):
        similarity_matrix.append([])
        for col in range(0, matrix_length):
            product = adjacency_matrix[row][row] * adjacency_matrix[col][col]
            similarity_matrix[row].append(round(adjacency_matrix[row][col] / math.sqrt(product), 3))

    # 输出矩阵为excel文件
    excel_output(adjacency_matrix, names)
    excel_output(similarity_matrix, names, "similarity")

    # 使用相似矩阵进行层次聚类
    cluster_Number = 10
    ac = AgglomerativeClustering(n_clusters=cluster_Number, affinity='euclidean', linkage='ward', compute_full_tree=True)
    print(ac.fit(similarity_matrix))
    labels = ac.fit_predict(similarity_matrix)
    print(labels)
    print(ac.labels_)
    print(dict(enumerate(ac.children_, ac.n_leaves_)))
    print(ac.children_[0][0])

    # 需要新建立一个多叉树，叶节点是样本
    # 换而言之需要找到同一个label样本的最近父节点x，x代表了这个label下样本的层级
    # 通过此种方式遍历树，


    # 层次聚类树模型示范
    # X = np.concatenate([np.random.randn(3, 10), np.random.randn(2, 10) + 100])
    # print(X)
    # model = AgglomerativeClustering(linkage="average", affinity="cosine")
    # model.fit(X)
    # print(model.labels_)
    #
    # ii = itertools.count(X.shape[0])
    # print([{'node_id': next(ii), 'left': x[0], 'right': x[1]} for x in model.children_])
    # print(dict(enumerate(model.children_, model.n_leaves_)))


    # single每两个样本组成一个层次
    # label = sch.linkage(similarity_matrix, method='complete')
    # 拼音转换
    names_pinyin = pinyin(names)
    # 自带层次聚类图
    # dn = sch.dendrogram(label, labels=names)


    # 保存图片，使用bbox_inches='tight'输出完整图片
    plt.savefig('./static/PaperData/hierarchyCluster1.png', dpi=600, bbox_inches='tight')
    # plt.show()
    # print(names)
    # print(names_pinyin)
    # print(label)
    # print(len(label))
    # print(map(lambda x:x[2:3], label.tolist()))

    # return label.tolist(),names


# 输出二维list为excel文件
def excel_output(content: list, heads: list, name="default"):
    output = open('./static/PaperData/' + name + '_output.xls', 'w', encoding='gbk')
    output.write('人名\t')
    # 写表头
    for head in range(0, len(content)):
        output.write(str(heads[head]))  # write函数不能写int类型的参数，所以使用str()转化
        output.write('\t')  # 相当于Tab一下，换一个单元格
    output.write('\n')
    # 写表体
    for i in range(0, len(content)):
        for j in range(0, len(content[i]) + 1):
            if j == 0:
                # 写列头
                write_content = heads[i]
            else:
                write_content = content[i][j - 1]
            output.write(str(write_content))  # write函数不能写int类型的参数，所以使用str()转化
            output.write('\t')  # 相当于Tab一下，换一个单元格
        output.write('\n')  # 写完一行立马换行
    output.close()


# 将list中的中文转换为拼音
def pinyin(words: list):
    pinyin_words = []
    for word in words:
        s = ''
        for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
            s += ''.join(i)
        pinyin_words.append(s)
    return pinyin_words
