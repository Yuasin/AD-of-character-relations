import networkx as nx
import json
from analysis.hierarchyCluster import pinyin


def networkAnalyse(nodes: dict, edges: dict):
    # 构建无向加权图
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for i in edges.keys():
        for j in edges[i]:
            G.add_edge(i, j, weight=edges[i][j])
            # print(G.edges['一灯', '郭靖']['weight'])

    # 量化数据计算
    # print(nx.info(G))
    # print(nx.degree_histogram(G))
    # print(G.degree('郭靖'))
    # print('图的连边数量' + str(G.size()))

    # 节点数量
    node_number = len(G.nodes)

    # 边数量
    edge_number = G.number_of_edges()
    print('边数量:  ' + str(edge_number))

    # 聚类系数，节点的邻接结点实际边数和总的可能边数的比值
    cluster = nx.clustering(G)
    all_cluster = 0
    for i in cluster:
        cluster[i] = round(cluster[i], 3)
        all_cluster += cluster[i]
    cluster = sorted(cluster.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print('聚类系数:  ' + str(cluster))

    # 网络平均聚类系数
    average_cluster = round(all_cluster / node_number, 3)
    print('聚类系数之和:  ' + str(all_cluster) + ' 平均聚类系数:  ' + str(average_cluster))

    # 网络密度,网络实际边缘数与可能边缘数的比值
    density = nx.density(G)

    # 无标度网络数据，根据人物出现频次分布和平均度数，绘制成散点图
    print(nx.degree_histogram(G))

    # 点度中心性，节点的度数中心性越高，意味着和该节点有关系的其他节点就越多
    degree_centrality = nx.degree(G)
    degree_centrality_dict = {}
    # print(degree_centrality)
    for (name, degree) in degree_centrality:
        degree_centrality_dict[name] = round(degree / (node_number - 1), 3)
    degree_centrality_dict_sort = sorted(degree_centrality_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print('点度中心性:  ' + str(degree_centrality_dict_sort))

    # 介数中心性，即指一个节点在其他任意两点间最短路径上的个数
    betweenness_centrality = nx.betweenness_centrality(G)
    for i in betweenness_centrality:
        betweenness_centrality[i] = round(betweenness_centrality[i], 3)
    betweenness_centrality_sorted = sorted(betweenness_centrality.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print('介数中心性:  ' + str(betweenness_centrality_sorted))

    # 接近中心性，计算一个节点到其他所有的节点的平均最短距离，这个距离越小节点周围的紧密程度越高，接近中心性也就越高
    closeness_centrality = nx.closeness_centrality(G)
    for i in closeness_centrality:
        closeness_centrality[i] = round(closeness_centrality[i], 3)
    closeness_centrality_sort = sorted(closeness_centrality.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print('接近中心性:  ' + str(closeness_centrality_sort))

    # 路径相关
    shortest_path = nx.shortest_path(G)
    # 最短路径分布
    path_distribution = {}
    for source in shortest_path:
        for target in shortest_path[source]:
            cur_length = len(shortest_path[source][target])
            if cur_length in path_distribution:
                path_distribution[cur_length] += 1
            else:
                path_distribution[cur_length] = 1
    # 直径
    diameter = max(path_distribution.keys())
    # 平均最短路径
    all_path_length = 0
    for i in path_distribution:
        all_path_length += path_distribution[i] * i
    average_shortest_path = all_path_length / sum(path_distribution.values())

    print('路径:  ' + str(shortest_path))
    print('直径:  ' + str(diameter))
    print('最短路径分布:  ' + str(path_distribution))
    print('平均最短路径:  ' + str(average_shortest_path))

    # 构建json
    data_list = {"frequency": [], "density": [], "centrality": {}, "degree": {}, "between": {}, "closeness": {},
                 "cluster": {}, "average_cluster": [], "path": {}, "edges": []}
    # 挑选频次前二十组成环形图
    sorted_nodes = sorted(nodes.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    for i in range(0, 20):
        data_list["frequency"].append({"value": sorted_nodes[i][1], "name": sorted_nodes[i][0]})

    # 网络密度
    data_list["density"] = {"value": density, "name": "网络密度"}

    # 平均聚类系数
    data_list["average_cluster"] = {"value": average_cluster, "name": "平均聚类系数"}

    # 聚类系数
    data_list["cluster"]["names"] = []
    data_list["cluster"]["pinyinnames"] = []
    data_list["cluster"]["values"] = []
    for i in cluster:
        data_list["cluster"]["names"].append(i[0])
        data_list["cluster"]["values"].append(i[1])
    data_list["cluster"]["pinyinnames"] = pinyin(data_list["cluster"]["names"])

    # 点度中心性
    # 介数中心性
    # 接近中心性
    data_list["centrality"]["names"] = []
    data_list["centrality"]["pinyinnames"] = []
    data_list["centrality"]["degree"] = []
    data_list["centrality"]["between"] = []
    data_list["centrality"]["closeness"] = []
    for i in sorted_nodes:
        data_list["centrality"]["names"].append(i[0])
        data_list["centrality"]["degree"].append(degree_centrality_dict[i[0]])
        data_list["centrality"]["between"].append(betweenness_centrality[i[0]])
        data_list["centrality"]["closeness"].append(closeness_centrality[i[0]])
    data_list["centrality"]["pinyinnames"] = pinyin(data_list["centrality"]["names"])

    data_list["degree"]["data"] = []
    data_list["degree"]["name"] = []
    data_list["degree"]["pinyinname"] = []
    for i in degree_centrality_dict_sort:
        data_list["degree"]["data"].append(i[1])
        data_list["degree"]["name"].append(i[0])
    data_list["degree"]["pinyinname"] = pinyin(data_list["degree"]["name"])

    data_list["between"]["data"] = []
    data_list["between"]["name"] = []
    data_list["between"]["pinyinname"] = []
    for i in betweenness_centrality_sorted:
        data_list["between"]["data"].append(i[1])
        data_list["between"]["name"].append(i[0])
    data_list["between"]["pinyinname"] = pinyin(data_list["between"]["name"])

    data_list["closeness"]["data"] = []
    data_list["closeness"]["name"] = []
    data_list["closeness"]["pinyinname"] = []
    for i in closeness_centrality_sort:
        data_list["closeness"]["data"].append(i[1])
        data_list["closeness"]["name"].append(i[0])
    data_list["closeness"]["pinyinname"] = pinyin(data_list["closeness"]["name"])

    # 路径相关
    data_list["path"]["names"] = []
    data_list["path"]["dis"] = []
    data_list["path"]["dia"] = diameter
    data_list["path"]["shortest"] = round(average_shortest_path, 2)
    for i in path_distribution:
        data_list["path"]["names"].append(str(i))
        data_list["path"]["dis"].append({})
        data_list["path"]["dis"][i - 1]["name"] = i
        data_list["path"]["dis"][i - 1]["value"] = path_distribution[i]

    # 输出json
    with open('./static/analyseData1.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_list, ensure_ascii=False))
