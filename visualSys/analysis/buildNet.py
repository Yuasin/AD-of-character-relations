from analysis.processCorpus import getSection
from analysis.buildJson import buildJson
from analysis.network import networkAnalyse
from analysis.hierarchyCluster import cluster_hierarchy
import pypinyin
import re


def buildNet(name: str):
    # 声明网络数据
    all_name = {}
    adjacency_list = {}
    replace_name = {}
    # 读入人物列表，去除人物列表头尾的空白
    with open("./static/book/" + name + "/namelist.txt") as f:
        for line in f.readlines():
            # 分割一行内容，获取别名
            namelist = re.split('-|,|，|;|；', line)
            # 将一行中的最后一个名称去除换行符
            namelist[-1] = namelist[-1].strip()
            # 将别名对应的正名储存在replace_name中
            if len(namelist)>1:
                for i in range(len(namelist)-1):
                    replace_name[namelist[i+1]] = namelist[0]
            cur_name = str(namelist[0])
            all_name[cur_name] = 0
            adjacency_list[cur_name] = {}
    # print(all_name)
    print("需替换人物列表：" + str(replace_name))

    # 获取分段过的语料文件，并将别名替换为正名
    all_section = getSection(name, "./static/book/" + name + "/corpus.txt", replace_name)

    # adjacency_list 储存实体，以及与实体相连的其他实体,以及相连的次数 {entity:{connect_entity:times}}
    for cur_section in all_section:
        section_entity = set()
        # 统计实体出现在section中的次数，在一个section中出现多次只计算一次
        for cur_entity in all_name:
            if cur_entity in cur_section:
                all_name[cur_entity] += 1
                section_entity.add(cur_entity)

                # 建立邻接表
                for e in section_entity:
                    if e == cur_entity: continue
                    if e in adjacency_list[cur_entity].keys():
                        adjacency_list[cur_entity][e] += 1
                    else:
                        adjacency_list[cur_entity][e] = 1
                    if cur_entity in adjacency_list[e].keys():
                        adjacency_list[e][cur_entity] += 1
                    else:
                        adjacency_list[e][cur_entity] = 1
        section_entity.clear()

    print(adjacency_list)
    # 删除文学作品中没有出现的人物以及与其它人物没有关联的人物
    deleteData(all_name, adjacency_list)

    # 将中文转换为拼音
    # all_name, adjacency_list = turn_pinyin(all_name, adjacency_list)

    # 层次聚类情况：前端点击层次聚类按钮时再进行层次聚类
    # 层次聚类返回结果：层次聚类结果应该直接修改json文件
    # combos_tree, labels = cluster_hierarchy(all_name,adjacency_list)
    buildJson(all_name, adjacency_list, None, None)
    networkAnalyse(all_name, adjacency_list)

    return all_name, adjacency_list


# 1.删除网络中出现次数为0的节点
# 2.删除网络中与其它节点相邻数量为0的节点
def deleteData(nodes: dict, edges: dict):
    delete_key = []
    for key in nodes:
        if nodes[key] == 0:
            delete_key.append(key)
        elif len(edges[key]) == 0:
            delete_key.append(key)
    for key in delete_key:
        del nodes[key]
        del edges[key]


# 将网络中人物名称转换为英文
def turn_pinyin(nodes: dict, edges: dict):
    new_nodes = {}
    new_edges = {}
    for k in nodes:
        # print(k)
        s = ''
        count = 0
        for i in pypinyin.pinyin(k, style=pypinyin.NORMAL):
            if count < 2:
                s += ''.join(str(i[0]).title())
            else:
                s += ''.join(i)
            if count == 0:
                s += ' '
            count += 1
        new_nodes[s] = nodes[k]

    for k in edges:
        s = ''
        count = 0
        for i in pypinyin.pinyin(k, style=pypinyin.NORMAL):
            if count < 2:
                s += ''.join(str(i[0]).title())
            else:
                s += ''.join(i)
            if count == 0:
                s += ' '
            count += 1
        new_edges[s] = {}
        for inner in edges[k]:
            new_word = ''
            count = 0
            for i in pypinyin.pinyin(inner, style=pypinyin.NORMAL):
                if count < 2:
                    new_word += ''.join(str(i[0]).title())
                else:
                    new_word += ''.join(i)
                if count == 0:
                    new_word += ' '
                count += 1
            new_edges[s][new_word] = edges[k][inner]

    return new_nodes, new_edges
