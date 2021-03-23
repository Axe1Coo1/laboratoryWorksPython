import igraph
import os
import numpy as np
import time
from sys import getsizeof
import matplotlib.pyplot as plt

# -------------------------------------------------
# Алгоритм Краскала поиска минимального остова графа
# -------------------------------------------------

# список ребер графа (длина, вершина 1, вершина 2)

matrix_smez = np.array([np.array([0, 0, 0, 0, 5, 0, 0]),
                        np.array([0, 0, 13, 18, 17, 14, 22]),
                        np.array([0, 0, 0, 26, 0, 22, 0]),
                        np.array([0, 0, 0, 0, 0, 0, 0]),
                        np.array([0, 0, 0, 0, 0, 0, 19]),
                        np.array([0, 0, 0, 0, 0, 0, 0]),
                        np.array([0, 0, 0, 0, 0, 0, 0])])
print('Размер матрицы: ', getsizeof(matrix_smez))
print(len(matrix_smez))


def record_array(matrix):
	name = {}
	for i in range(len(matrix)):
		name[i] = str(i)
	rec_array = []
	count = [0 for i in range(len(matrix))]
	num = [[] for i in range(len(matrix))]
	neigh_num = [[] for i in range(len(matrix))]
	childes = [[] for i in range(len(matrix))]
	weights = [0 for i in range(len(matrix))]
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if matrix[i][j] != 0:
				count[i] += 1
				count[j] += 1
				weights[i] += matrix[i][j]
				weights[j] += matrix[i][j]
				num[j] += [i]
				num[i] += [j]
				childes[i] += [j]
	neigh_count = [i for i in count]
	for i in range(len(neigh_num)):
		neigh_num[i] += [j for j in num[i]]
	for i in range(len(matrix)):
		rec_array += [{'Номер': i, 'Имя': name[i],
		               'Кол. соседей': neigh_count[i],
		               'Номер соседей': neigh_num[i], 'Дети': childes[i],
		               'Сумма веса': weights[i]}]
	print('Размер массива записей: ', getsizeof(rec_array))
	for i in range(len(rec_array)):
		print(rec_array[i])
	return rec_array


def list_smezh(matrix):
	lst_smz = []
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if matrix[i][j] != 0:
				lst_smz += [(matrix_smez[i][j], i, j)]
	print('Размер списка смежности: ', getsizeof(lst_smz))
	print(lst_smz)
	return lst_smz


def plot_graf(rec_array, R, name):
	G = igraph.Graph(directed=True)
	G.add_vertices(rec_array[-1]['Номер'] + 1)
	G.vs['label'] = [rec_array[i]['Имя'] for i in range(len(rec_array))]
	for i in R:
		G.add_edges([(i[1], i[2])])
	# Веса
	G.es['label'] = [i[0] for i in R]
	layout = G.layout('kk')
	igraph.plot(G, (name + '.png'), bbox=(800, 600), layout=layout, vertex_size=40, vertex_label_size=10)


def plot_grafT(rec_array, T):
	G = igraph.Graph(directed=True)
	G.add_vertices(7)
	G.vs['label'] = [rec_array[i]['Имя'] for i in range(len(rec_array))]
	for i in T:
		G.add_edges([(i[1], i[2])])
	# Веса
	G.es['label'] = [i[0] for i in T]
	layout = G.layout('kk')
	igraph.plot(G, 'graphT.png', bbox=(800, 600), layout=layout, vertex_size=40, vertex_label_size=10)



def alg(Rs, U, D, T):
	start_time = time.time()
	Rs = sorted(R, key=lambda x: x[0])
	for i in range(10 ** 6):
		for r in Rs:
			if r[1] not in U or r[2] not in U:  # проверка для исключения циклов в остове
				if r[1] not in U and r[2] not in U:  # если обе вершины не соединены, то
					D[r[1]] = [r[1], r[2]]  # формируем в словаре ключ с номерами вершин
					D[r[2]] = D[r[1]]  # и связываем их с одним и тем же списком вершин
				else:  # иначе
					if not D.get(r[1]):  # если в словаре нет первой вершины, то
						D[r[2]].append(r[1])  # добавляем в список первую вершину
						D[r[1]] = D[r[2]]  # и добавляем ключ с номером первой вершины
					else:
						D[r[1]].append(r[2])  # иначе, все то же самое делаем со второй вершиной
						D[r[2]] = D[r[1]]

				T.append(r)  # добавляем ребро в остов
				U.add(r[1])  # добавляем вершины в множество U
				U.add(r[2])

		for r in Rs:  # проходим по ребрам второй раз и объединяем разрозненные группы вершин
			if r[2] not in D[r[1]]:  # если вершины принадлежат разным группам, то объединяем
				T.append(r)  # добавляем ребро в остов
				gr1 = D[r[1]]
				D[r[1]] += D[r[2]]  # объединем списки двух групп вершин
				D[r[2]] += gr1
	exec_time = time.time() - start_time
	print('Время работы:', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def list_smezh_array(rec_array):
	lst_smz = []
	counter = 1
	for i in rec_array:
		for j in i['Дети']:
			lst_smz += [(counter, int(i['Имя']), j)]
			counter += 1
	print('Размер списка смежности: ', getsizeof(lst_smz))
	print(lst_smz)
	return lst_smz


R = list_smezh(matrix_smez)
Rs = sorted(R, key=lambda x: x[0])
U = set()  # список соединенных вершин
D = {}  # словарь списка изолированных групп вершин
T = []  # список ребер остова

alg(Rs, U, D, T)
rec_array = record_array(matrix_smez)
plot_graf(rec_array, T, 'grafT')
plot_graf(rec_array, R, 'graf')


times = []
sizes = []
number = np.arange(1, 4, 1)
for i in range(1, 4):
	size = i
	start_time = time.time()
	N = size * size
	matrix = ([])
	for i in range(N):
		row = (np.zeros(N))
		for j in range(N):
			if i + 1 != size and i + 1 != size * 2 and i + 1 != size * 3 and i + 1 != size * 4 and i + 1 != size * 5 and i + 1 != size * 3 and i + 1 != size * 6 and i + 1 != size * 7 and i + 1 != size * 8 and i + 1 != size * 9 and i + 1 != size * 10 and i + 1 != size * 11 and i + 1 != size * 12 and i + 1 != size * 13:
				if i + 1 == j:
					row[j] = 1
				elif i + size == j:
					row[j] = 1
			elif i + size == j:
				row[j] = 1
		matrix.append(row)

	exec_time = time.time() - start_time
	times.append(exec_time * 100000)
	sizes.append(getsizeof(matrix))
	print("Размер", getsizeof(matrix))
	print('Время выполнения:', exec_time)

rec_array2 = record_array(matrix)
lsist_smj2 = list_smezh_array(rec_array2)
plot_graf(rec_array2, lsist_smj2, 'квадратная_матрица')

plt.plot(number, sizes)
plt.xlabel('Размер матрицы')
plt.ylabel('Размер в битах')
plt.show()
plt.plot(number, times)
plt.xlabel('Размер матрицы')
plt.ylabel('Время в милисекунда')
plt.show()

# inf = float('inf')
# Edge = namedtuple('Edge', 'start, end, cost')
#
#
# def make_edge(start, end, cost=1):
# 	return Edge(start, end, cost)
#
#
# class Graph:
# 	def __init__(self, edges):
# 		# let's check that the data is right
# 		wrong_edges = [i for i in edges if len(i) not in [2, 3]]
# 		if wrong_edges:
# 			raise ValueError('Неправильные данные: {}'.format(wrong_edges))
#
# 		self.edges = [make_edge(*edge) for edge in edges]
#
# 	@property
# 	def vertices(self):
# 		return set(
# 			sum(
# 				([edge.start, edge.end] for edge in self.edges), []
# 			)
# 		)
#
# 	def get_node_pairs(self, n1, n2, both_ends=True):
# 		if both_ends:
# 			node_pairs = [[n1, n2], [n2, n1]]
# 		else:
# 			node_pairs = [[n1, n2]]
# 		return node_pairs
#
# 	def remove_edge(self, n1, n2, both_ends=True):
# 		node_pairs = self.get_node_pairs(n1, n2, both_ends)
# 		edges = self.edges[:]
# 		for edge in edges:
# 			if [edge.start, edge.end] in node_pairs:
# 				self.edges.remove(edge)
#
# 	def add_edge(self, n1, n2, cost=1, both_ends=True):
# 		node_pairs = self.get_node_pairs(n1, n2, both_ends)
# 		for edge in self.edges:
# 			if [edge.start, edge.end] in node_pairs:
# 				return ValueError('Нет выхода'.format(n1, n2))
#
# 		self.edges.append(Edge(start=n1, end=n2, cost=cost))
# 		if both_ends:
# 			self.edges.append(Edge(start=n2, end=n1, cost=cost))
#
# 	@property
# 	def neighbours(self):
# 		neighbours = {vertex: set() for vertex in self.vertices}
# 		for edge in self.edges:
# 			neighbours[edge.start].add((edge.end, edge.cost))
#
# 		return neighbours
#
# 	def dijkstra(self, source, dest):
# 		assert source in self.vertices, 'Нет выхода'
# 		distances = {vertex: inf for vertex in self.vertices}
# 		previous_vertices = {
# 			vertex: None for vertex in self.vertices
# 		}
# 		distances[source] = 0
# 		vertices = self.vertices.copy()
#
# 		while vertices:
# 			current_vertex = min(
# 				vertices, key=lambda vertex: distances[vertex])
# 			vertices.remove(current_vertex)
# 			if distances[current_vertex] == inf:
# 				break
# 			for neighbour, cost in self.neighbours[current_vertex]:
# 				alternative_route = distances[current_vertex] + cost
# 				if alternative_route < distances[neighbour]:
# 					distances[neighbour] = alternative_route
# 					previous_vertices[neighbour] = current_vertex
#
# 		path, current_vertex = deque(), dest
# 		while previous_vertices[current_vertex] is not None:
# 			path.appendleft(current_vertex)
# 			current_vertex = previous_vertices[current_vertex]
# 		if path:
# 			path.appendleft(current_vertex)
# 		return path
#
#
# matrix = [
# 	("0", "1", 6), ("0", "2", 6), ("1", "4", 4), ("2", "5", 4),
# 	("3", "1", 10), ("3", "2", 10), ("3", "4", 10), ("3", "5", 10),
# 	("4", "5", 2), ("4", "6", 4), ("5", "6", 2)]
# x = np.delete(matrix, ())
# x = x.astype(np.int)
#
# test = []
# for i in range(2, len(x), 3):
# 	test.append([(x[i - 2], x[i - 1]), x[i]])
# print(test)
#
# matrix = []
# for el in test:
# 	matrix.append((str(el[0][0]), str(el[0][1]), el[1]))
# print(matrix)
# graph = Graph(matrix)
# label = ["0", "1", "2", "3", "4", "5", "6"]
# print(graph.dijkstra("0", "6"))
#
# G = igraph.Graph(directed=True)
# G.add_vertices(7)
# G.vs['label'] = [label[i] for i in range(len(label))]
# G.add_edges([i[0] for i in test])
# G.es['weight'] = [i[1] for i in test]
# G.es['label'] = [i[1] for i in test]
# layout = G.layout('kk')
# igraph.plot(G, 'graph.png', bbox=(1000, 1000), layout=layout, vertex_size=40,
#             vertex_label_size=10, edge_width=[edge for edge in G.es['weight']])
# # os.startfile(r'../graph.png')
#
# times = []
# sizes = []
# number = np.arange(1, 10, 1)
# for i in range(1, 10):
# 	size = i
# 	start_time = time.time()
# 	N = size * size
# 	matrix = ([])
# 	for i in range(N):
# 		row = (np.zeros(N))
# 		for j in range(N):
# 			if i + 1 != size and i + 1 != size * 2 and i + 1 != size * 3 and i + 1 != size * 4 and i + 1 != size * 5 and i + 1 != size * 3 and i + 1 != size * 6 and i + 1 != size * 7 and i + 1 != size * 8 and i + 1 != size * 9 and i + 1 != size * 10 and i + 1 != size * 11 and i + 1 != size * 12 and i + 1 != size * 13:
# 				if i + 1 == j:
# 					row[j] = 1
# 				elif i + size == j:
# 					row[j] = 1
# 			elif i + size == j:
# 				row[j] = 1
# 		# matrix=np.append(matrix,row,axis=0)
# 		matrix.append(row)
# 	# print(row)
# 	# print(matrix)
# 	# getsizeof(adj_list)
#
# 	exec_time = time.time() - start_time
# 	times.append(exec_time * 1000)
# 	sizes.append(getsizeof(matrix))
# 	print("Размер", getsizeof(matrix))
# 	print('Время выполнения:', exec_time)
#
# plt.plot(number, sizes)
# plt.xlabel('Размер матрицы')
# plt.ylabel('Размер в битах')
# plt.show()
# plt.plot(number, times)
# plt.xlabel('Размер матрицы')
# plt.ylabel('Время в милисекунда')
# plt.show()
#
# adj_matrix = matrix
#
#
# def Adjacency_List(matrix):
# 	adj_list = []
# 	for i in range(len(matrix)):
# 		for j in range(len(matrix[i])):
# 			if matrix[i][j] != 0:
# 				adj_list += [[tuple([i, j]), adj_matrix[i][j]]]
# 	print(adj_list)
# 	return adj_list, print('Размер списка смежности: ', getsizeof(adj_list))
#
#
# Adjacency_List(matrix)
