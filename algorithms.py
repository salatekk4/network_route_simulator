from collections import deque
import heapq
from graph_utils import get_neighbors


def bfs(graph, start):
    visited = []
    queue = deque([start])

    while queue:
        node = queue.popleft()

        if node not in visited:
            visited.append(node)
            print("Посетили:", node)

            for to_node, latency, capacity in get_neighbors(graph, node):
                queue.append(to_node)


def find_path_bfs(graph, start, target):
    visited = [start]
    parent = {start: None}
    queue = deque([start])

    while queue:
        node = queue.popleft()

        if node == target:
            break

        for to_node, latency, capacity in get_neighbors(graph, node):
            if to_node not in visited:
                visited.append(to_node)
                queue.append(to_node)
                parent[to_node] = node

    if target not in parent:
        return None

    path = []
    current = target

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def find_fastest_path_dijkstra(graph, start, target):
    if start not in graph or target not in graph:
        return None

    distances = {node: float("inf") for node in graph}
    parent = {start: None}
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        current_distance, node = heapq.heappop(heap)

        if current_distance > distances[node]:
            continue

        if node == target:
            break

        for to_node, latency, capacity in get_neighbors(graph, node):
            new_distance = current_distance + latency

            if new_distance < distances.get(to_node, float("inf")):
                distances[to_node] = new_distance
                parent[to_node] = node
                heapq.heappush(heap, (new_distance, to_node))

    if distances[target] == float("inf"):
        return None

    path = []
    current = target

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path, distances[target]
