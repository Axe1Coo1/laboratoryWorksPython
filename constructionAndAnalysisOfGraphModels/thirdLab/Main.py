import random
import statistics

import igraph
from sys import getsizeof
import matplotlib.pyplot as plt

# На каждом шаге добавляется новая вершина, для которой выбирается только
# один сосед из уже существующих вершин (N = 5, 10, … 100 – количество
# вершин в дереве).


# список смежности графа имеет вид - (вес ребра, вершина 1, вершина 2)
# Возраст вершин хранится в словаре ключ - номер вершины, значение - возраст

# quantity = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
quantity = [20]
ages = {}
global x
x = []
acc = []

print(random.random())


def generate_list_smezh(quantity, K):
	global ages
	ages = {}
	lst_smz = []
	for i in range(quantity):
		ages[i] = 0
		if len(lst_smz) < 1:
			lst_smz += [(1, i, False)]
			ages = add_ages(ages)
		# print(lst_smz)
		else:
			lst_smz += [(1, i, make_probability_for_real(ages, K))]
			ages = add_ages(ages)
	# print('Размер списка смежности: ', getsizeof(lst_smz))
	# print(lst_smz)
	return lst_smz


def make_probability_for_real(ages, K):
	probability_list = []
	for i in range(len(ages) - 1):
		add = ages.get(i)
		sum_values = 0
		for i in range(len(ages) - 1):
			sum_values += 1 / ages.get(i)
		A = 1 / (1 / sum_values ** K)
		probability_list.append(A * (1 / add))
	probability_list.sort()
	# print(probability_list)
	item_prob = random.random()
	counter = 0
	for i in probability_list:
		if item_prob < i:
			return ages.get(counter + 1)
		counter += 1


def add_ages(ages):
	for i in range(len(ages)):
		ages[i] += 1
	return ages


def plot_graf(lst_smz, name):
	G = igraph.Graph(directed=True)
	G.add_vertices(lst_smz[-1][1] + 1)
	G.vs['label'] = [lst_smz[i][1] for i in range(len(lst_smz))]
	lst_smz.pop(0)
	for i in lst_smz:
		G.add_edges([(i[1], i[2])])
	# Веса
	G.es['label'] = [i[0] for i in lst_smz]
	layout = G.layout('kk')
	igraph.plot(G, (name + '.png'), bbox=(800, 600), layout=layout, vertex_size=40, vertex_label_size=10)
	acc.append(G.diameter(directed=True, unconn=True, weights=None))


for K in range(3, 4):
	for i in quantity:
		for j in range(100):
			lst_smz = generate_list_smezh(i, K)
			plot_graf(lst_smz, "Граф")
		# print(acc)
		x.append(statistics.mean(acc))
		acc = []
	plt.plot(x, quantity)
	plt.xlabel('Диаметр графа')
	plt.ylabel('Размер графа')
	plt.show()
	x = []
