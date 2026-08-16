def validate_node_name(node):
    if not isinstance(node, str):
        return False, "Имя роутера должно быть строкой"

    if not node.strip():
        return False, "Имя роутера не может быть пустым"

    return True, ""


def validate_connection(from_node, to_node, latency, capacity):
    is_valid, message = validate_node_name(from_node)
    if not is_valid:
        return False, message

    is_valid, message = validate_node_name(to_node)
    if not is_valid:
        return False, message

    if from_node == to_node:
        return False, "Нельзя создать соединение роутера с самим собой"

    if not isinstance(latency, int) or latency <= 0:
        return False, "Задержка должна быть целым числом больше 0"

    if not isinstance(capacity, int) or capacity <= 0:
        return False, "Пропускная способность должна быть целым числом больше 0"

    return True, ""

def add_edge(graph, from_node, to_node, latency, capacity):
    is_valid, message = validate_connection(
        from_node,
        to_node,
        latency,
        capacity
    )

    if not is_valid:
        return False, message

    if from_node not in graph:
        graph[from_node] = []

    if to_node not in graph:
        graph[to_node] = []

    if is_direct_connection(graph, from_node, to_node):
        return False, f"Соединение {from_node} -> {to_node} уже существует"

    graph[from_node].append((to_node, latency, capacity))

    return True, f"Соединение {from_node} -> {to_node} добавлено"


def remove_edge(graph, from_node, to_node):
    if from_node not in graph:
        return False

    edges = graph[from_node]

    for i in range(len(edges)):
        neighbor, latency, capacity = edges[i]

        if neighbor == to_node:
            edges.pop(i)
            return True

    return False


def remove_node(graph, node):
    if node not in graph:
        return False

    del graph[node]

    for current_node in graph:
        new_edges = []

        for to_node, latency, capacity in graph[current_node]:
            if to_node != node:
                new_edges.append((to_node, latency, capacity))

        graph[current_node] = new_edges

    return True


def show_graph(graph):
    for node, edges in graph.items():
        print("Роутер:", node)

        if len(edges) == 0:
            print("  нет соединений")
        else:
            for to_node, latency, capacity in edges:
                print(f"  -> {to_node} | задержка: {latency} мс | скорость: {capacity} Мбит/с")

        print()


def has_node(graph, node):
    return node in graph


def get_neighbors(graph, node):
    return graph.get(node, [])


def is_direct_connection(graph, frm, to):
    for to_node, latency, capacity in get_neighbors(graph, frm):
        if to_node == to:
            return True

    return False


def get_edge_info(graph, from_node, to_node):
    for neighbor, latency, capacity in get_neighbors(graph, from_node):
        if neighbor == to_node:
            return latency, capacity

    return None


def calculate_path_info(graph, path):
    if path is None or len(path) < 2:
        return None

    total_latency = 0
    min_capacity = None

    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]

        edge_info = get_edge_info(graph, from_node, to_node)

        if edge_info is None:
            return None

        latency, capacity = edge_info
        total_latency += latency

        if min_capacity is None or capacity < min_capacity:
            min_capacity = capacity

    return total_latency, min_capacity

def analyze_network(graph):
    node_count = len(graph)
    edge_count = 0
    total_latency = 0

    fastest_edge = None
    slowest_edge = None
    nodes_without_connections = []

    for from_node, edges in graph.items():
        if not edges:
            nodes_without_connections.append(from_node)

        for to_node, latency, capacity in edges:
            edge_count += 1
            total_latency += latency

            edge = (from_node, to_node, latency, capacity)

            if fastest_edge is None or latency < fastest_edge[2]:
                fastest_edge = edge

            if slowest_edge is None or latency > slowest_edge[2]:
                slowest_edge = edge

    average_latency = None

    if edge_count > 0:
        average_latency = total_latency / edge_count

    return {
        "node_count": node_count,
        "edge_count": edge_count,
        "average_latency": average_latency,
        "fastest_edge": fastest_edge,
        "slowest_edge": slowest_edge,
        "nodes_without_connections": nodes_without_connections
    }
