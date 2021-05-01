import networkx as nx

print(nx)


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

    # 无标度网络数据

    # 点度中心性，节点的度数中心性越高，意味着和该节点有关系的其他节点就越多
    degree_centrality = nx.degree(G)
    degree_centrality_dict = {}
    # print(degree_centrality)
    for (name, degree) in degree_centrality:
        degree_centrality_dict[name] = round(degree / (node_number - 1), 3)
    degree_centrality_dict = sorted(degree_centrality_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print('点度中心性:  ' + str(degree_centrality_dict))

    # 介数中心性，即指一个节点在其他任意两点间最短路径上的个数
    betweenness_centrality = nx.betweenness_centrality(G)
    for i in betweenness_centrality:
        betweenness_centrality[i] = round(betweenness_centrality[i], 3)
    betweenness_centrality = sorted(betweenness_centrality.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print('介数中心性:  ' + str(betweenness_centrality))

    # 接近中心性，计算一个节点到其他所有的节点的平均最短距离，这个距离越小节点周围的紧密程度越高，接近中心性也就越高
    closeness_centrality = nx.closeness_centrality(G)
    for i in closeness_centrality:
        closeness_centrality[i] = round(closeness_centrality[i], 3)
    closeness_centrality = sorted(closeness_centrality.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print('接近中心性:  ' + str(closeness_centrality))

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
        all_path_length += path_distribution[i]*i
    average_shortest_path = all_path_length/sum(path_distribution.values())

    print('路径:  ' + str(shortest_path))
    print('直径:  ' + str(diameter))
    print('最短路径分布:  ' + str(path_distribution))
    print('平均最短路径:  ' + str(average_shortest_path))

