import random
import statistics
import numpy as np
import igraph
from sys import getsizeof
import matplotlib.pyplot as plt

# На каждом шаге добавляется новая вершина, для которой выбирается только
# один сосед из уже существующих вершин (N = 5, 10, … 100 – количество
# вершин в дереве).


# список смежности графа имеет вид - (вес ребра, вершина 1, вершина 2)
# Возраст вершин хранится в словаре ключ - номер вершины, значение - возраст

quantity = [20]  # Список размеров графа
ages = {}  # Словарь для записи возрастов вершин
x = []  # Список усредлнённых значений диаметров графа для построения графиков
acc = []  # Список всех значений диаметров графа для построения графиков



# Функция для генерации списка смежности графа
def generate_list_smezh(quantity, K):
	global ages
	ages = {}
	lst_smz = []
	sort_ages = []
	for i in range(quantity):
		ages[i] = 0
		if len(lst_smz) < 1:
			lst_smz += [(1, i, False)]
			ages = add_ages(ages)
		# print(lst_smz)
		else:
			# for i in ages.values():
			# 	sort_ages.append(i)
			# sort_ages = sorted(sort_ages)
			# for i in range(len(ages)):
			# 	ages[i] = sort_ages[i]

			lst_smz += [(1, i, make_probability_for_real(ages, K))]
			ages = add_ages(ages)
	# print('Размер списка смежности: ', getsizeof(lst_smz))
	# print(lst_smz)
	return lst_smz


# Функция для возврата вершины графа с которой будет сформирована связь
def make_probability_for_real(ages, K):
	probability_list = []  # Создание пустого списка для хранения вероятностей
	for i in range(len(ages) - 1):  # Перебор элементов исключая последний, так-как он имеет нулевой возраст
		add = ages.get(i)  # Получение возраста элемента i
		sum_values = 0
		for i in range(len(ages) - 1):  # Получение суммы из возрастов / 1 в степени К
			sum_values += 1 / (ages.get(i) ** K)
		A = (1 / sum_values)  # Получение значения альфа
		if i == 0:
			continue
		probability_list.append(A * (1 / i ** K))  # Добавление в список вероятностей вероятности выбора вершины i
	item_prob = random.random()  # Генерация случайного числа в диапозоне от 0 до 1
	probability_list = np.cumsum(probability_list)  # Получение кумулитивной суммы списка вероятностей
	counter = 0
	for i in probability_list:  # Сравнение случайного значения с вероятностями в списке
		if item_prob < i:
			return counter  # Возврат счётчика его значение соответстует номеру вершины, с которой нужно построить связь
		counter += 1


# Функция для добавления возраста вершинам
def add_ages(ages):
	for i in range(len(ages)):
		ages[i] += 1
	return ages


# Функция для построения графа
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
	acc.append(G.diameter(directed=True, unconn=True, weights=None))  # Добавление диаметра графа в список acc

# Часть, отвечающая за построение спектра степеней графа
	neis = []
	neis += G.neighborhood_size()
	neis[:] = [x - 1 for x in neis]
	print(neis)
	neis = (np.unique(neis, return_counts=True))
	plt.bar(neis[0], neis[1])
	plt.xlabel('Степень')
	plt.ylabel('Кол-во вершин')
	plt.show()



for K in range(1, 2):
	for i in quantity:
		for j in range(1):
			lst_smz = generate_list_smezh(i, K)
			plot_graf(lst_smz, "Граф")
		# print(acc)
		x.append(statistics.mean(acc))
		acc = []
	plt.plot(x, quantity)
	x = []
plt.xlabel('Диаметр графа')
plt.ylabel('Размер графа')
plt.show()


