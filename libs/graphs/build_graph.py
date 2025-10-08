
from typing import List, Dict

def build_edges(chunks: List[Dict]) -> List[Dict]:
    edges = []
    for i in range(len(chunks)-1):
        edges.append(dict(src=i, dst=i+1, edge_type="flow", weight=0.2))
    return edges
