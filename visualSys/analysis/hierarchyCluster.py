import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
import math
import pypinyin
from matplotlib import pyplot as plt
from analysis.tree import TreeNode


def cluster_hierarchy(nodes: dict, edges: dict, num=5):
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
                # edges中可能没有相对应到该人的边
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
            if product == 0:
                similarity_matrix[row].append(0)
            else:
                similarity_matrix[row].append(round(adjacency_matrix[row][col] / math.sqrt(product), 3))

    # 输出矩阵为excel文件
    excel_output(adjacency_matrix, names)
    excel_output(similarity_matrix, names, "similarity")

    # 使用相似矩阵进行层次聚类
    # 可改聚类数量的层次聚类
    # linkage四选项  {'ward', 'complete', 'average', 'single'
    cluster_Number = num
    ac = AgglomerativeClustering(n_clusters=cluster_Number, affinity='euclidean', linkage='ward',
                                 compute_full_tree=True)
    print(ac.fit(similarity_matrix))
    labels = ac.fit_predict(similarity_matrix)
    original_tree = dict(enumerate(ac.children_, ac.n_leaves_))
    print("样本归属聚类标记： "+str(labels))
    print("节点与其左右子节点： " + str(dict(enumerate(ac.children_, ac.n_leaves_))))

    # 需要新建立一个多叉树，叶节点是样本
    # 换而言之需要找到同一个label样本的最近父节点x，x代表了这个label下样本的层级
    # 通过此种方式遍历树，建立字典 dict{label: x}
    # ！！或者通过另一种方式，进行遍历树，当遍历到叶子节点时，用叶子节点的值作为索引
    # 找到labels_中对应的值，并且对当前节点的值进行替换
    # 当一个节点左右节点的值相等时，将该值赋予当前节点，并且把左右节点置为空
    # 当树修改完毕之后，从上到下通过树建立combos信息，再根据label对nodes添加combos信息

    # tree_dict = {id:TreeNode}
    # root 为最顶端 TreeNode
    # 建立树
    tree_dict = {}
    for i in original_tree.items():
        left = i[1][0]
        right = i[1][1]
        parent = i[0]
        if parent not in tree_dict:
            tree_dict[parent] = TreeNode(parent)
        if left not in tree_dict:
            tree_dict[left] = TreeNode(left)
        if right not in tree_dict:
            tree_dict[right] = TreeNode(right)
        tree_dict[parent].left = tree_dict[left]
        tree_dict[parent].right = tree_dict[right]
        tree_dict[left].parent = tree_dict[parent]
        tree_dict[right].parent = tree_dict[parent]

    root = tree_dict[(len(tree_dict)) - 1]
    # 重建树
    traveseTree(root, labels)
    # 打印树
    Print(root)


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
    # names_pinyin = pinyin(names)
    # 自带层次聚类图
    # dn = sch.dendrogram(label, labels=names_pinyin)


    # 保存图片，使用bbox_inches='tight'输出完整图片
    # plt.savefig('./static/PaperData/hierarchyCluster3.png', dpi=600, bbox_inches='tight')
    # plt.show()
    # return label.tolist(),names
    return root, labels

def traveseTree(root: TreeNode, labels: list):
    if root.left is not None:
        traveseTree(root.left, labels)
        traveseTree(root.right, labels)
        root.emerge()
    else:
        root.val = labels[root.val]
        return

def Print(root:TreeNode):
    # write code here
    if not root:
        return []

    nodes = [root]
    # results = []

    while nodes:
        temp, res = [], []
        for node in nodes:
            res.append(node.val)
            if node.left:
                temp.append(node.left)
            if node.right:
                temp.append(node.right)
        print(res)
        nodes = temp


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
