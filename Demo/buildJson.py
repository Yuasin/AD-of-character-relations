import json
import math


# 边的权重为"label":edges[i][j]
# data_list为python数据格式
# buildJson构建可在G6关系图中适用的的Json格式数据
def buildJson(nodes: dict, edges: dict, label=None, names=None):
    if names is None:
        names = []
    if label is None:
        label = []
    data_list = {"nodes": [], "edges": [], "combos": []}
    id_node = {}
    id_n = 0
    # 加点
    for i in nodes.keys():
        id_node[i] = id_n
        # 对节点的size进行处理，能够突出大节点的同时不让大小节点差距过大
        cur_nodes = {"id": str(id_n), "label": i, "size": math.ceil(math.pow(nodes[i], 1 / 3)) + 4}
        data_list["nodes"].append(cur_nodes)
        id_n += 1
    # 加边
    for i in edges.keys():
        for j in edges[i]:
            cur_edges = {"source": str(id_node[i]), "target": str(id_node[j]), "weight": edges[i][j]}
            data_list["edges"].append(cur_edges)

    # 加combo
    # label的前两列为聚类主题，如第一行前两个节点84、86归属于同一个combo
    # 而两个节点combo的父亲combo则根据节点数量 nodesNumber 顺延
    # 加完combo信息还需要在nodes中对每个节点添加其归属combo信息
    # 需要分类讨论节点和combo的情况
    names_len = len(names)
    parentId = names_len
    id_combo = 0
    for l in label:
        combo = {"id": "combo" + str(id_combo), "parentId": "combo" + str(parentId)}
        data_list["combos"].append(combo)
        label_one = int(l[0])
        label_two = int(l[1])
        if label_one < names_len:
            label_name = names[label_one]
            data_list["nodes"][id_node[label_name]]["comboId"] = "combo" + str(id_combo)
        else:
            combo = {"id": "combo" + str(label_one), "parentId": "combo" + str(id_combo)}
            data_list["combos"].append(combo)
        if label_two < names_len:
            label_name = names[label_two]
            data_list["nodes"][id_node[label_name]]["comboId"] = "combo" + str(id_combo)
        else:
            combo = {"id": "combo" + str(label_two), "parentId": "combo" + str(id_combo)}
            data_list["combos"].append(combo)
        id_combo += 1
        parentId += 1


    with open('data2weight.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_list, ensure_ascii=False))

# def add_combo():
