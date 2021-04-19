import igraph
import numpy as np
import time
from sys import getsizeof
import matplotlib.pyplot as plt

# На каждом шаге добавляется новая вершина, для которой выбирается только
# один сосед из уже существующих вершин (N = 5, 10, … 100 – количество
# вершин в дереве).


# список смежности графа имеет вид - (вес ребра, вершина 1, вершина 2)

# Тестовый граф
matrix_smez_test_graph = np.array([np.array([0, 0, 0, 0, 5, 0, 0]),
                                   np.array([0, 0, 13, 18, 17, 14, 22]),
                                   np.array([0, 0, 0, 26, 0, 22, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 19]),
                                   np.array([0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0])])
print('Размер матрицы: ', getsizeof(matrix_smez_test_graph))


# Функция записи массива данных из первой лабораторной
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


# Функция записи списка смежности для тестовой матрицы из первой лабораторной
def list_smezh(matrix):
	lst_smz = []
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if matrix[i][j] != 0:
				lst_smz += [(matrix_smez_test_graph[i][j], i, j)]
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


times = []


# Алгоритм Краскала
def alg(Rs, U, D, T):
	start_time = time.time()
	for r in Rs:
		if r[1] not in U or r[2] not in U or r[2] not in D[r[1]]:  # проверка для исключения циклов в остове
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


# print(T)
# for r in Rs:  # проходим по ребрам второй раз и объединяем разрозненные группы вершин
# 	if r[2] not in D[r[1]]:  # если вершины принадлежат разным группам, то объединяем
# 		T.append(r)  # добавляем ребро в остов
# 		# print(D[r[2]], D[r[1]])
# 		print(D)
# 		gr1 = D[r[1]]
# 		D[r[1]] += D[r[2]]  # объединем списки двух групп вершин
# 		D[r[2]] += gr1
# 		print(D)
# print(D)
# print(T)
# exec_time = time.time() - start_time
# times.append(exec_time * 1000)


# exec_time = time.time() - start_time
# print('Время работы:', exec_time)
# print('Ср. время работы: ', exec_time / 10 ** 6)


# Функция для построения списка смежности из массива данных
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


List_smezh_dlya_test_graph = list_smezh(matrix_smez_test_graph)
Sorted_list_smezh = sorted(List_smezh_dlya_test_graph, key=lambda x: x[0])
U = set()  # список соединенных вершин
D = {}  # словарь списка изолированных групп вершин
T = []  # список ребер остова

alg(Sorted_list_smezh, U, D, T)
rec_array = record_array(matrix_smez_test_graph)
plot_graf(rec_array, T, 'Тестовый_граф_после_сортировки')
plot_graf(rec_array, List_smezh_dlya_test_graph, 'Тестовый_граф')

# Построение квадратной решётки
# times = []
sizes = []
number = np.arange(1, 6, 1)
for i in range(1, 6):
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
	start_time = time.time()
	rec_array_graph = record_array(matrix)
	lsist_smzh = list_smezh_array(rec_array_graph)
	# plot_graf(rec_array_graph, lsist_smzh, 'квадратная_матрица')

	Sorted_lst_smezh = sorted(lsist_smzh, key=lambda x: x[0])
	U2 = set()  # список соединенных вершин
	D2 = {}  # словарь списка изолированных групп вершин
	T2 = []  # список ребер остова

	alg(Sorted_lst_smezh, U2, D2, T2)
	plot_graf(rec_array_graph, T2, 'квадратная_матрица_отсортированная')
	exec_time = time.time() - start_time
	times.append(exec_time * 1000)

	# exec_time = time.time() - start_time
	# times.append(exec_time * 1000)
	sizes.append(getsizeof(matrix))
	print("Размер", getsizeof(matrix))
	print('Время выполнения:', exec_time)

rec_array_graph = record_array(matrix)
lsist_smzh = list_smezh_array(rec_array_graph)
plot_graf(rec_array_graph, lsist_smzh, 'квадратная_матрица')

Sorted_lst_smezh = sorted(lsist_smzh, key=lambda x: x[0])
U2 = set()  # список соединенных вершин
D2 = {}  # словарь списка изолированных групп вершин
T2 = []  # список ребер остова

alg(Sorted_lst_smezh, U2, D2, T2)
plot_graf(rec_array_graph, T2, 'квадратная_матрица_отсортированная')

plt.plot(number, sizes)
plt.xlabel('Размер матрицы')
plt.ylabel('Размер в битах')
plt.show()
plt.plot(number, times)
plt.xlabel('Размер матрицы')
plt.ylabel('Время в милисекунда')
plt.show()
