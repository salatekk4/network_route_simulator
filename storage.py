import json


def save_graph_to_file(graph, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(graph, file, indent=4, ensure_ascii=False)

    print(f"Граф сохранен в файл {filename}")


def load_graph_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("JSON должен содержать объект с роутерами")

    graph = {}

    for node, edges in data.items():
        if not isinstance(node, str) or not node.strip():
            raise ValueError("Имя роутера в JSON должно быть непустой строкой")

        if not isinstance(edges, list):
            raise ValueError(f"Соединения роутера {node} должны быть списком")

        graph[node] = []

        for edge in edges:
            if not isinstance(edge, list) or len(edge) != 3:
                raise ValueError(
                    f"Некорректное соединение у роутера {node}: {edge}"
                )

            to_node, latency, capacity = edge

            if not isinstance(to_node, str) or not to_node.strip():
                raise ValueError("Конечный роутер должен быть непустой строкой")

            if not isinstance(latency, int) or latency <= 0:
                raise ValueError("Задержка в JSON должна быть целым числом больше 0")

            if not isinstance(capacity, int) or capacity <= 0:
                raise ValueError(
                    "Пропускная способность в JSON должна быть целым числом больше 0"
                )

            graph[node].append((to_node, latency, capacity))

    return graph
