import igraph
import numpy as np
import os

edge_colour = []


# поиск всех не смежных вершин
def search_not_adjacant_vertices(vertex, adjacency_graph, vertices_graph):
	not_adjacent_vertices = []  # не смежные вершины
	# 1. поиск не смежных вершин
	for vertex_i, rib_weight_i in enumerate(adjacency_graph[vertex]):
		if (not rib_weight_i) and (vertex_i not in vertices_graph):
			# 2. исключаем вершины смежные между собой
			for vertex_j, rib_weight_j in enumerate(adjacency_graph[vertex_i]):
				if rib_weight_j and (vertex_j in not_adjacent_vertices):
					break  # "Найдена смежная вершина"
			else:
				not_adjacent_vertices.append(vertex_i)  # записываем НЕ смежную вершину
	return not_adjacent_vertices


def Graf_colors(Graph):
	# изначальные данные
	vertices_graph = []  # закрашенные вершины графа
	vertices_color = []  # цвет вершин
	color = 0  # текущий цвет

	# перебираем все вершины графа
	for vertex in range(len(Graph)):
		print("V-graf: ", vertices_graph, "  |  V-color: ", vertices_color)

		# берем не закрашенные вершины
		if vertex not in vertices_graph:
			for vertex_color in search_not_adjacant_vertices(vertex, Graph, vertices_graph):
				print("        v: ", vertex_color)
				vertices_graph.append(vertex_color)
				vertices_color.append(color)
				edge_colour.append(color)

			color += 1  # следующий цвет
	return tuple(zip(vertices_graph, vertices_color))


# лист смежности
def list_smezh(Vn, matrix):
	lst_smz = []
	for i in range(Vn):
		for j in range(i, Vn):
			if matrix[i][j] != 0:
				lst_smz += [[tuple([i, j]), False]]
	return lst_smz


# картинка png
def plot_graf(Vn, lst_smz, V_color, fail):
	v, color = zip(*V_color)

	G = igraph.Graph(directed=False)
	G.add_vertices(Vn)
	G.vs['label'] = list(range(Vn))
	G.vs["color"] = list("#{}{}{}".format(str(hex((80 * color[v.index(k)] + 40) % 201 + 55))[2:],
	                                      str(hex((45 * color[v.index(k)] + 120) % 231 + 25))[2:],
	                                      str(hex((17 * color[v.index(k)]) % 239 + 16))[2:]) for k in range(Vn))
	G.add_edges([i[0] for i in lst_smz])
	layout = G.layout('kk')
	igraph.plot(G, fail, bbox=(800, 600), layout=layout, vertex_size=40, vertex_label_size=10)


def tests_list(tests=[]):
	tests.append(np.array([
		np.array([0, 1, 0, 1, 0, 1, 0, 0, 0, 0]),
		np.array([1, 0, 1, 0, 1, 0, 0, 0, 0, 0]),
		np.array([0, 0, 0, 1, 0, 1, 0, 1, 0, 0]),
		np.array([0, 0, 1, 0, 1, 0, 1, 0, 0, 0]),
		np.array([0, 0, 0, 0, 0, 1, 0, 1, 0, 1]),
		np.array([0, 0, 0, 0, 1, 0, 1, 0, 1, 0]),
		np.array([0, 1, 0, 0, 0, 0, 0, 1, 0, 1]),
		np.array([1, 0, 0, 0, 0, 0, 1, 0, 1, 0]),
		np.array([0, 1, 0, 1, 0, 0, 0, 0, 0, 1]),
		np.array([1, 0, 1, 0, 0, 0, 0, 0, 1, 0])
	]))  # тест

	return tests


def tests():
	test_list = tests_list()  # список тестов, список матриц смежности

	# проводим тесты
	for index, test in enumerate(test_list):
		Vn = len(test)  # размер матрицы
		lst_smz = list_smezh(Vn, test)  # список смежности
		print("\n", lst_smz)
		V_color = Graf_colors(test)  # цвет вершин
		plot_graf(Vn, lst_smz, V_color, 'graph{}.png'.format(index))
		os.startfile(r'graph0.png')
		G = igraph.Graph(directed=False)

		G.add_vertices(10)
		G.vs['label'] = list(range(Vn))
		G.add_edges([i[0] for i in lst_smz])
		print(lst_smz)
		print(V_color)

		colour_counter = 0
		for i in lst_smz:
			if i[1] == False:
				i[1] = colour_counter
				colour_counter += 1

		G.es['label'] = ([i[1] for i in lst_smz])
		layout = G.layout('kk')

		igraph.plot(G, 'graph_normal.png', bbox=(800, 600), layout=layout, vertex_size=40, vertex_label_size=10)
		os.startfile(r'graph_normal.png')


tests()
