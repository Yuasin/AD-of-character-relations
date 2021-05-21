function findPath(graph, data){
    const clearStates = () => {
        graph.getNodes().forEach((node) => {
            graph.clearItemStates(node);
            });
        graph.getEdges().forEach((edge) => {
            graph.clearItemStates(edge);
            });
    };
    graph.on('canvas:click', (e) => {
      clearStates();
    });

    buttonFindPath.addEventListener('click', (e) => {
          const selectedNodes = graph.findAllByState('node', 'selected');
          if (selectedNodes.length !== 2) {
            alert('Please select TWO nodes!\n\r请选择有且两个节点！');
            return;
          }
          clearStates();
          const { findShortestPath } = G6.Algorithm;
          // path 为其中一条最短路径，allPath 为所有的最短路径
          const { path, allPath } = findShortestPath(
            data,
            selectedNodes[0].getID(),
            selectedNodes[1].getID(),
          );

          const pathNodeMap = {};
          path.forEach((id) => {
            const pathNode = graph.findById(id);
            pathNode.toFront();
            graph.setItemState(pathNode, 'highlight', true);
            pathNodeMap[id] = true;
          });
          graph.getEdges().forEach((edge) => {
            const edgeModel = edge.getModel();
            const source = edgeModel.source;
            const target = edgeModel.target;
            const sourceInPathIdx = path.indexOf(source);
            const targetInPathIdx = path.indexOf(target);
            if (sourceInPathIdx === -1 || targetInPathIdx === -1) return;
            if (Math.abs(sourceInPathIdx - targetInPathIdx) === 1) {
              graph.setItemState(edge, 'highlight', true);
            } else {
              graph.setItemState(edge, 'inactive', true);
            }
          });
          graph.getNodes().forEach((node) => {
            if (!pathNodeMap[node.getID()]) {
              graph.setItemState(node, 'inactive', true);
            }
          });
        });
}
