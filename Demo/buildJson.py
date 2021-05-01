import json
import math

# 边的权重为"label":edges[i][j]
# data_list为python数据格式
def buildJson(nodes: dict, edges: dict):
    data_list = {"nodes": [], "edges": []}
    id_node = {}
    id = 0
    for i in nodes.keys():
        id_node[i] = id
        # 对节点的size进行处理，能够突出大节点的同时不让大小节点差距过大
        cur_nodes = {"id":str(id), "label":i, "size":math.ceil(math.pow(nodes[i],1/3))+4}
        data_list["nodes"].append(cur_nodes)
        id += 1
    for i in edges.keys():
        for j in edges[i]:
            cur_edges = {"source":str(id_node[i]), "target":str(id_node[j]) , "weight":edges[i][j]}
            data_list["edges"].append(cur_edges)

    with open('data2weight.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_list, ensure_ascii=False))
