from analysis.processCorpus import getSection
from analysis.buildJson import buildJson
from analysis.network import networkAnalyse
from analysis.hierarchyCluster import cluster_hierarchy
import pypinyin

def buildNet(name:str):
    # 获取分段过的语料文件
    all_section = getSection(name, "./static/book/"+name+"/corpus.txt")

    # 读入人物列表，去除人物列表头尾的空白
    all_name = {}
    adjacency_list = {}
    with open("./static/book/"+name+"/namelist.txt") as f:
        for line in f.readlines():
            cur_name = str(line.strip())
            all_name[cur_name] = 0
            adjacency_list[cur_name] = {}
    # print(all_name)

    test_section = all_section[200:250]
    # print(test_section)

    # adjacency_list 储存实体，以及与实体相连的其他实体,以及相连的次数 {entity:{connect_entity:times}}
    for cur_section in all_section:
        section_entity = set()
        # 统计实体出现在section中的次数，在一个section中出现多次只计算一次
        for cur_entity in all_name:
            if cur_entity in cur_section:
                all_name[cur_entity] += 1
                section_entity.add(cur_entity)

                # 建立邻接表
                for e in section_entity :
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

    # 将中文转换为拼音
    all_name, adjacency_list = turn_pinyin(all_name, adjacency_list)
    print(all_name)
    print(adjacency_list)

    # print(all_name)
    # print(adjacency_list)

    # 层次聚类情况：前端点击层次聚类按钮时再进行层次聚类
    # 层次聚类返回结果：层次聚类结果应该直接修改json文件
    # combos_tree, labels = cluster_hierarchy(all_name,adjacency_list)
    # combo_label, sorted_names = cluster_hierarchy(all_name,adjacency_list)
    buildJson(all_name, adjacency_list, None, None)
    networkAnalyse(all_name, adjacency_list)

    return all_name,adjacency_list


def turn_pinyin(nodes: dict, edges: dict):
    new_nodes = {}
    new_edges = {}
    for k in nodes:
        # print(k)
        s = ''
        for i in pypinyin.pinyin(k, style=pypinyin.NORMAL):
            s += ''.join(i)
        new_nodes[s] = nodes[k]

    for k in edges:
        s = ''
        for i in pypinyin.pinyin(k, style=pypinyin.NORMAL):
            s += ''.join(i)
        new_edges[s] = {}
        for inner in edges[k]:
            new_word = ''
            for i in pypinyin.pinyin(inner, style=pypinyin.NORMAL):
                new_word += ''.join(i)
            new_edges[s][new_word] = edges[k][inner]

    return new_nodes,new_edges