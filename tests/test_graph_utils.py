import unittest

from graph_utils import (
    add_edge,
    remove_edge,
    remove_node,
    is_direct_connection,
    calculate_path_info,
    analyze_network
)


class TestGraphUtils(unittest.TestCase):
    def setUp(self):
        self.graph = {
            "A": [("B", 10, 100), ("C", 20, 80)],
            "B": [("D", 15, 70)],
            "C": [("D", 5, 60)],
            "D": []
        }
    def test_analyze_network(self):
        result = analyze_network(self.graph)

        self.assertEqual(result["node_count"], 4)
        self.assertEqual(result["edge_count"], 4)
        self.assertEqual(result["average_latency"], 12.5)
        self.assertEqual(result["fastest_edge"], ("C", "D", 5, 60))
        self.assertEqual(result["slowest_edge"], ("A", "C", 20, 80))
        self.assertEqual(result["nodes_without_connections"], ["D"])

    def test_add_valid_edge(self):
        success, message = add_edge(self.graph, "D", "E", 8, 50)

        self.assertTrue(success)
        self.assertEqual(message, "Соединение D -> E добавлено")
        self.assertTrue(is_direct_connection(self.graph, "D", "E"))
        self.assertIn("E", self.graph)

    def test_add_duplicate_edge(self):
        success, message = add_edge(self.graph, "A", "B", 10, 100)

        self.assertFalse(success)
        self.assertEqual(message, "Соединение A -> B уже существует")

    def test_add_self_loop(self):
        success, message = add_edge(self.graph, "A", "A", 10, 100)

        self.assertFalse(success)
        self.assertEqual(
            message,
            "Нельзя создать соединение роутера с самим собой"
        )

    def test_add_edge_with_invalid_latency(self):
        success, message = add_edge(self.graph, "A", "E", 0, 100)

        self.assertFalse(success)
        self.assertEqual(
            message,
            "Задержка должна быть целым числом больше 0"
        )

    def test_add_edge_with_invalid_capacity(self):
        success, message = add_edge(self.graph, "A", "E", 10, -5)

        self.assertFalse(success)
        self.assertEqual(
            message,
            "Пропускная способность должна быть целым числом больше 0"
        )

    def test_remove_edge(self):
        result = remove_edge(self.graph, "A", "B")

        self.assertTrue(result)
        self.assertFalse(is_direct_connection(self.graph, "A", "B"))

    def test_remove_node_removes_all_connections(self):
        result = remove_node(self.graph, "D")

        self.assertTrue(result)
        self.assertNotIn("D", self.graph)
        self.assertFalse(is_direct_connection(self.graph, "B", "D"))
        self.assertFalse(is_direct_connection(self.graph, "C", "D"))

    def test_calculate_path_info(self):
        path = ["A", "B", "D"]

        result = calculate_path_info(self.graph, path)

        self.assertEqual(result, (25, 70))


if __name__ == "__main__":
    unittest.main()
