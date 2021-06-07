import json
import math
from analysis.tree import TreeNode


# 边的权重为"label":edges[i][j]
# data_list为python数据格式
# buildJson构建可在G6关系图中适用的的Json格式数据
def buildJson(nodes: dict, edges: dict, combos_tree:TreeNode, labels=None):
    if combos_tree is None:
        names = []
    if labels is None:
        label = []
    data_list = {"nodes": [], "edges": [], "combos": []}
    id_node = {}
    id_n = 0

    # 加点
    for i in nodes.keys():
        id_node[i] = id_n
        # 对节点的size进行处理，能够突出大节点的同时不让大小节点差距过大
        cur_nodes = {"id": str(id_n), "label": i, "size": math.ceil(math.pow(nodes[i], 1 / 3)) + 4, "times":nodes[i]}
        data_list["nodes"].append(cur_nodes)
        id_n += 1
    # 加边
    for i in edges.keys():
        for j in edges[i]:
            cur_edges = {"source": str(id_node[i]), "target": str(id_node[j]), "weight": edges[i][j]}
            data_list["edges"].append(cur_edges)

    # 添加combo
    if combos_tree is not None:
        nodes_level = [combos_tree]
        while nodes_level:
            temp, res = [], []
            for node in nodes_level:
                combo = {"id": "combo" + str(node.val)}
                res.append(node.val)
                if node.parent:
                    combo["parentId"] = "combo" + str(node.parent.val)
                if node.left:
                    temp.append(node.left)
                if node.right:
                    temp.append(node.right)
                data_list["combos"].append(combo)
            nodes_level = temp
        #  在节点中添加归属combo信息
        nodes_sorted = sorted(nodes.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        rank = 0
        for i in nodes_sorted:
            # print(i[0])
            data_list["nodes"][id_node[i[0]]]["comboId"] = "combo" + str(labels[rank])
            data_list["nodes"][id_node[i[0]]]["cluster"] = "combo" + str(labels[rank])
            rank += 1

    # names_len = len(names)
    # parentId = names_len
    # id_combo = 0
    # for l in label:
    #     combo = {"id": "combo" + str(id_combo), "parentId": "combo" + str(parentId)}
    #     data_list["combos"].append(combo)
    #     label_one = int(l[0])
    #     label_two = int(l[1])
    #     if label_one < names_len:
    #         label_name = names[label_one]
    #         data_list["nodes"][id_node[label_name]]["comboId"] = "combo" + str(id_combo)
    #     else:
    #         combo = {"id": "combo" + str(label_one), "parentId": "combo" + str(id_combo)}
    #         data_list["combos"].append(combo)
    #     if label_two < names_len:
    #         label_name = names[label_two]
    #         data_list["nodes"][id_node[label_name]]["comboId"] = "combo" + str(id_combo)
    #     else:
    #         combo = {"id": "combo" + str(label_two), "parentId": "combo" + str(id_combo)}
    #         data_list["combos"].append(combo)
    #     id_combo += 1
    #     parentId += 1

    with open('./static/dataWithWeight.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_list, ensure_ascii=False))

    return data_list
