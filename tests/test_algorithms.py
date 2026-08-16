import unittest

from algorithms import find_path_bfs, find_fastest_path_dijkstra


class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.graph = {
            "A": [("B", 100, 100), ("C", 10, 80)],
            "B": [("D", 10, 70)],
            "C": [("E", 10, 60)],
            "E": [("D", 10, 60)],
            "D": [],
            "X": []
        }

    def test_bfs_finds_fewest_hops(self):
        path = find_path_bfs(self.graph, "A", "D")

        self.assertEqual(path, ["A", "B", "D"])

    def test_dijkstra_finds_lowest_latency(self):
        result = find_fastest_path_dijkstra(self.graph, "A", "D")

        self.assertIsNotNone(result)

        path, latency = result

        self.assertEqual(path, ["A", "C", "E", "D"])
        self.assertEqual(latency, 30)

    def test_bfs_returns_none_when_path_does_not_exist(self):
        path = find_path_bfs(self.graph, "A", "X")

        self.assertIsNone(path)

    def test_dijkstra_returns_none_when_path_does_not_exist(self):
        result = find_fastest_path_dijkstra(self.graph, "A", "X")

        self.assertIsNone(result)

    def test_dijkstra_returns_none_for_unknown_node(self):
        result = find_fastest_path_dijkstra(self.graph, "A", "Unknown")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
