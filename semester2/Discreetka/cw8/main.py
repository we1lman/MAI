import itertools
import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import permutations


def build_latin_square(nodes):
    n = len(nodes)
    latin_square = [[0] * n for _ in range(n)]
    perms = list(permutations(nodes))

    for i in range(n):
        for j in range(n):
            latin_square[i][j] = perms[i][j]

    return latin_square


def enumerate_paths_latin(graph, start, end):
    nodes = list(graph.nodes)
    node_index = {node: i for i, node in enumerate(nodes)}
    latin_square = build_latin_square(nodes)
    paths = []

    def dfs(current_path):
        current_node = current_path[-1]
        if current_node == end:
            paths.append(current_path)
            return
        current_index = node_index[current_node]
        for i in range(len(nodes)):
            next_node = latin_square[current_index][i]
            if next_node not in current_path and next_node in graph[current_node]:
                dfs(current_path + [next_node])

    dfs([start])
    return paths


class Graph:
    def __init__(self, G=None, from_edges=None):
        if G is not None:
            self.G = G
        elif from_edges is not None:
            self.G = nx.DiGraph()
            self.G.add_edges_from(from_edges)
        else:
            self.G = nx.DiGraph()
        self.pos = None

    def add_node(self, node):
        self.G.add_node(node)
        self.pos = nx.spring_layout(self.G)

    def add_edge(self, node1, node2):
        self.G.add_edge(node1, node2)
        self.pos = nx.spring_layout(self.G)

    def remove_node(self, node):
        self.G.remove_node(node)
        self.pos = nx.spring_layout(self.G)

    def remove_edge(self, node1, node2):
        self.G.remove_edge(node1, node2)
        self.pos = nx.spring_layout(self.G)

    def clear_graph(self):
        if nx.is_frozen(self.G):
            self.G = nx.DiGraph()
        else:
            self.G.clear()

    def planar_layout(self):
        return nx.planar_layout(self.G)


class App:
    def __init__(self):
        self.graph = Graph()
        self.root = tk.Tk()
        self.root.title('Ориентированный граф и латинская композиция')
        self._create_interface()
        self._setup_graph_canvas()

    def _create_interface(self):
        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)
        self._create_buttons()

    def _create_buttons(self):
        interaction_frame = tk.Frame(self.root, height=60)
        interaction_frame.pack(side=tk.BOTTOM, fill=tk.X)
        interaction_frame.pack_propagate(False)

        examples_frame = tk.Frame(self.root, height=60)
        examples_frame.pack(side=tk.BOTTOM, fill=tk.X)
        examples_frame.pack_propagate(False)

        interaction_buttons = [
            ('Добавить вершину', self.add_node),
            ('Добавить ребро', self.add_edge),
            ('Удалить вершину', self.remove_node),
            ('Удалить ребро', self.remove_edge),
            ('Перечислить пути', self.enumerate_paths),
            ('Очистить граф', self.clear_graph)
        ]

        for text, command in interaction_buttons:
            tk.Button(interaction_frame, text=text, command=command).pack(side=tk.LEFT, padx=5, pady=5)

    def _setup_graph_canvas(self):
        self.fig = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def draw_graph(self):
        self.fig.clf()
        pos = self.graph.pos if self.graph.pos else nx.spring_layout(self.graph.G)
        nx.draw(self.graph.G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=20,
                font_weight='bold')
        self.canvas.draw_idle()

    def add_node(self):
        node = simpledialog.askstring('Добавление вершины', 'Введите номер вершины')
        if node:
            self.graph.add_node(int(node))
            self.draw_graph()

    def add_edge(self):
        edge = simpledialog.askstring('Добавление ребра', 'Введите номера вершин через пробел')
        if edge:
            try:
                node1, node2 = map(int, edge.split())
                self.graph.add_edge(node1, node2)
                self.draw_graph()
            except ValueError:
                messagebox.showerror('Ошибка', 'Введите два числа, разделенные пробелом')

    def remove_node(self):
        node = simpledialog.askstring('Удаление вершины', 'Введите номер вершины')
        if node:
            self.graph.remove_node(int(node))
            self.draw_graph()

    def remove_edge(self):
        edge = simpledialog.askstring('Удаление ребра', 'Введите номера вершин через пробел')
        if edge:
            try:
                node1, node2 = map(int, edge.split())
                self.graph.remove_edge(node1, node2)
                self.draw_graph()
            except ValueError:
                messagebox.showerror('Ошибка', 'Введите два числа, разделенные пробелом')

    def clear_graph(self):
        self.graph.clear_graph()
        self.draw_graph()

    def enumerate_paths(self):
        start_node = simpledialog.askstring('Начальная вершина', 'Введите номер начальной вершины')
        end_node = simpledialog.askstring('Конечная вершина', 'Введите номер конечной вершины')
        if start_node and end_node:
            try:
                start_node = int(start_node)
                end_node = int(end_node)
                all_paths = enumerate_paths_latin(self.graph.G, start_node, end_node)
                messagebox.showinfo('Перечисление путей',
                                    f'Все пути из вершины {start_node} в вершину {end_node}: {all_paths}')
            except ValueError:
                messagebox.showerror('Ошибка', 'Введите корректные номера вершин')


if __name__ == "__main__":
    app = App()
    app.root.mainloop()