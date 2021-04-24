import json
import math


def buildJson(nodes: dict, edges: dict):
    data_list = {"nodes": [], "edges": []}
    id_node = {}
    id = 0
    for i in nodes.keys():
        id_node[i] = id
        cur_nodes = {"id":str(id), "label":i, "size":math.ceil(math.pow(nodes[i],1/2))}
        data_list["nodes"].append(cur_nodes)
        id += 1
    for i in edges.keys():
        for j in edges[i]:
            cur_edges = {"source":str(id_node[i]), "target":str(id_node[j])} #, "label":edges[i][j]
            data_list["edges"].append(cur_edges)

    with open('data1.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_list, ensure_ascii=False))
