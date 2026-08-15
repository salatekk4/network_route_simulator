import json
from graph_utils import *
from algorithms import *
from storage import *


def print_route_report(graph, start, target):
    path = find_path_bfs(graph, start, target)

    if path is None:
        print(f"Маршрут из {start} в {target} не найден")
        return

    path_info = calculate_path_info(graph, path)

    if path_info is None:
        print("Ошибка: не удалось посчитать параметры маршрута")
        return

    total_latency, min_capacity = path_info

    print("\nОтчет о маршруте")
    print("-" * 20)
    print(f"Откуда: {start}")
    print(f"Куда: {target}")
    print(f"Маршрут: {' -> '.join(path)}")
    print(f"Общая задержка: {total_latency} мс")
    print(f"Минимальная пропускная способность: {min_capacity} Мбит/с")


def print_fastest_route_report(graph, start, target):
    result = find_fastest_path_dijkstra(graph, start, target)

    if result is None:
        print(f"Быстрый маршрут из {start} в {target} не найден")
        return

    path, total_latency = result
    path_info = calculate_path_info(graph, path)

    if path_info is None:
        print("Ошибка: не удалось посчитать параметры быстрого маршрута")
        return

    _, min_capacity = path_info

    print("\nОтчет о самом быстром маршруте")
    print("-" * 30)
    print(f"Откуда: {start}")
    print(f"Куда: {target}")
    print(f"Маршрут: {' -> '.join(path)}")
    print(f"Общая задержка: {total_latency} мс")
    print(f"Минимальная пропускная способность: {min_capacity} Мбит/с")


def compare_routes(graph, start, target):
    print("\nСравнение алгоритмов")
    print("=" * 30)

    bfs_path = find_path_bfs(graph, start, target)
    dijkstra_result = find_fastest_path_dijkstra(graph, start, target)

    print("\n1. BFS")
    if bfs_path is None:
        print("Маршрут не найден")
    else:
        bfs_info = calculate_path_info(graph, bfs_path)

        if bfs_info is None:
            print("Ошибка при расчете параметров маршрута BFS")
        else:
            bfs_latency, bfs_capacity = bfs_info
            print(f"Маршрут: {' -> '.join(bfs_path)}")
            print(f"Прыжков: {len(bfs_path) - 1}")
            print(f"Общая задержка: {bfs_latency} мс")
            print(f"Минимальная пропускная способность: {bfs_capacity} Мбит/с")

    print("\n2. Дейкстра")
    if dijkstra_result is None:
        print("Маршрут не найден")
    else:
        dijkstra_path, dijkstra_latency = dijkstra_result
        dijkstra_info = calculate_path_info(graph, dijkstra_path)

        if dijkstra_info is None:
            print("Ошибка при расчете параметров маршрута Дейкстры")
        else:
            _, dijkstra_capacity = dijkstra_info
            print(f"Маршрут: {' -> '.join(dijkstra_path)}")
            print(f"Прыжков: {len(dijkstra_path) - 1}")
            print(f"Общая задержка: {dijkstra_latency} мс")
            print(f"Минимальная пропускная способность: {dijkstra_capacity} Мбит/с")


def add_edge_from_input(graph):
    from_node = input("Откуда идет соединение: ").strip()
    to_node = input("Куда идет соединение: ").strip()

    try:
        latency = int(input("Введите задержку (мс): ").strip())
        capacity = int(input("Введите пропускную способность (Мбит/с): ").strip())
    except ValueError:
        print("Ошибка: задержка и пропускная способность должны быть числами")
        return

    if from_node not in graph:
        graph[from_node] = []

    if to_node not in graph:
        graph[to_node] = []

    add_edge(graph, from_node, to_node, latency, capacity)
    print(f"Соединение {from_node} -> {to_node} добавлено")


def remove_edge_from_input(graph):
    from_node = input("Откуда удалить соединение: ").strip()
    to_node = input("Куда удалить соединение: ").strip()

    if not has_node(graph, from_node):
        print(f"Роутер {from_node} не найден")
        return

    if remove_edge(graph, from_node, to_node):
        print(f"Соединение {from_node} -> {to_node} удалено")
    else:
        print(f"Соединение {from_node} -> {to_node} не найдено")


def remove_node_from_input(graph):
    node = input("Какой роутер удалить: ").strip()

    if remove_node(graph, node):
        print(f"Роутер {node} удален")
    else:
        print(f"Роутер {node} не найден")


def show_menu():
    print("\nМеню")
    print("1. Показать граф")
    print("2. Найти маршрут")
    print("3. Проверить прямое соединение")
    print("4. Показать соседей узла")
    print("5. Найти самый быстрый маршрут")
    print("6. Сравнить BFS и Дейкстру")
    print("7. Добавить соединение")
    print("8. Удалить соединение")
    print("9. Удалить роутер")
    print("10. Сохранить граф в файл")
    print("11. Загрузить граф из файла")
    print("0. Выход")


def main():
    global graph

    while True:
        show_menu()
        choice = input("Выбери пункт: ").strip()

        if choice == "1":
            show_graph(graph)

        elif choice == "2":
            start = input("Введите начальный роутер: ").strip()
            target = input("Введите конечный роутер: ").strip()

            if not has_node(graph, start):
                print(f"Роутер {start} не найден")
            elif not has_node(graph, target):
                print(f"Роутер {target} не найден")
            else:
                print_route_report(graph, start, target)

        elif choice == "3":
            frm = input("Откуда: ").strip()
            to = input("Куда: ").strip()

            if not has_node(graph, frm):
                print(f"Роутер {frm} не найден")
            elif not has_node(graph, to):
                print(f"Роутер {to} не найден")
            elif is_direct_connection(graph, frm, to):
                print(f"Прямое соединение {frm} -> {to} есть")
            else:
                print(f"Прямого соединения {frm} -> {to} нет")

        elif choice == "4":
            node = input("Введите роутер: ").strip()

            if not has_node(graph, node):
                print(f"Роутер {node} не найден")
            else:
                neighbors = get_neighbors(graph, node)

                if not neighbors:
                    print(f"У роутера {node} нет соседей")
                else:
                    print(f"Соседи роутера {node}:")
                    for to_node, latency, capacity in neighbors:
                        print(f" -> {to_node} | задержка: {latency} мс | скорость: {capacity} Мбит/с")

        elif choice == "5":
            start = input("Введите начальный роутер: ").strip()
            target = input("Введите конечный роутер: ").strip()

            if not has_node(graph, start):
                print(f"Роутер {start} не найден")
            elif not has_node(graph, target):
                print(f"Роутер {target} не найден")
            else:
                print_fastest_route_report(graph, start, target)

        elif choice == "6":
            start = input("Введите начальный роутер: ").strip()
            target = input("Введите конечный роутер: ").strip()

            if not has_node(graph, start):
                print(f"Роутер {start} не найден")
            elif not has_node(graph, target):
                print(f"Роутер {target} не найден")
            else:
                compare_routes(graph, start, target)

        elif choice == "7":
            add_edge_from_input(graph)

        elif choice == "8":
            remove_edge_from_input(graph)

        elif choice == "9":
            remove_node_from_input(graph)

        elif choice == "10":
            filename = input("Введите имя файла (например graph.json): ").strip()
            save_graph_to_file(graph, filename)

        elif choice == "11":
            filename = input("Введите имя файла (например graph.json): ").strip()

            try:
                graph = load_graph_from_file(filename)
                print(f"Граф загружен из файла {filename}")
            except FileNotFoundError:
                print("Ошибка: файл не найден")
            except json.JSONDecodeError:
                print("Ошибка: файл поврежден или не является JSON")

        elif choice == "0":
            print("Выход из программы")
            break

        else:
            print("Неверный пункт меню")


graph = {
    "A": [("B", 10, 100), ("C", 20, 80)],
    "B": [("D", 15, 70)],
    "C": [("D", 5, 60)],
    "D": []
}


if __name__ == "__main__":
    main()
