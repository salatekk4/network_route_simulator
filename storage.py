import json


def save_graph_to_file(graph, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(graph, file, indent=4, ensure_ascii=False)

    print(f"Граф сохранен в файл {filename}")


def load_graph_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    graph = {}

    for node, edges in data.items():
        graph[node] = []

        for edge in edges:
            to_node, latency, capacity = edge
            graph[node].append((to_node, latency, capacity))

    return graph
