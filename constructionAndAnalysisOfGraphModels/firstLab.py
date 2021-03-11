import igraph
import os
import numpy as np
import time
from sys import getsizeof

matrix_smez = np.array([np.array([0, 1, 0, 0, 0]),
                        np.array([0, 0, 2, 2, 2]),
                        np.array([0, 0, 0, 0, 0]),
                        np.array([0, 0, 4, 0, 5]),
                        np.array([1, 0, 0, 0, 0])])
print('Размер матрицы: ', getsizeof(matrix_smez))
print(len(matrix_smez))


def list_smezh(matrix):
	lst_smz = []
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if matrix[i][j] != 0:
				lst_smz += [[tuple([i, j]), matrix_smez[i][j]]]
	print('Размер списка смежности: ', getsizeof(lst_smz))
	print(lst_smz)
	return lst_smz


def record_array(matrix):
	name = {0: 'Idea', 1: 'Plan', 2: 'Calculations', 3: 'Model', 4: 'Produce'}
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


# Поиск соседей матрицы
def search_matrix(matrix):
	neigh_input = int(input('Номер вершины для поиска соседей(матрица): '))
	start_time = time.time()
	for i in range(10 ** 6):
		neigh_num = []
		for j in range(len(matrix)):
			if matrix[neigh_input][j] != 0:
				neigh_num += [j]
		for j in range(len(matrix)):
			if matrix[j][neigh_input] != 0:
				neigh_num += [j]
	exec_time = time.time() - start_time
	print('Соседи:', neigh_num), print('Время работы:', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def chain_matrix(matrix):
	chain = input('Введите последовательность(матрица): ').split()
	start_time = time.time()
	for j in range(10 ** 6):
		for i in range(len(chain) - 1):
			if matrix[int(chain[i])][int(chain[i + 1])] != 0:
				answer = 'Введенная последовательность образует цепь'
			else:
				answer = 'Введенная последовательность  не образует цепь'
				break
	exec_time = time.time() - start_time
	print(answer), print('Время вып.: ', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def weight_matrix(matrix):
	weight = int(input('Введите вес(матрица): '))
	start_time = time.time()
	for k in range(10 ** 6):
		summ = [0 for i in range(len(matrix))]
		for i in range(len(matrix)):
			summ[i] += sum(matrix[i])
			for j in range(len(matrix[i])):
				if matrix[i][j] != 0:
					summ[j] += matrix[i][j]
		summ = [i for i in range(len(summ)) if summ[i] > weight]
	exec_time = time.time() - start_time
	print('Номера вершин: ', summ), print('Время работы: ', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def edge_matrix(matrix):
	start_time = time.time()
	for k in range(10 ** 6):
		edges = 0
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				if matrix[i][j] != 0:
					edges += 1
	exec_time = time.time() - start_time
	print('Количество рёбер в графе: ', edges), print('Время работы: ', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def sosed_list(lst):
	sosed_input = int(input('Введите номер вершины для поиска соседей(список): '))
	start_time = time.time()
	for j in range(10 ** 6):
		sosed_num = []
		for i in lst:
			if sosed_input in i[0] and sosed_input == i[0][0]:
				sosed_num += [i[0][1]]
			elif sosed_input in i[0] and sosed_input == i[0][1]:
				sosed_num += [i[0][0]]
	exec_time = time.time() - start_time
	print('Соседи: ', sosed_num), print('Время работы: ', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def chain_list(lst):
	chain = input('Введите последовательность(список): ').split()
	start_time = time.time()
	for k in range(10 ** 6):
		for i in range(len(chain) - 1):
			mid_var = tuple([int(chain[i]), int(chain[i + 1])])
			for j in range(len(lst)):
				if mid_var == lst[j][0]:
					answer = 'Введенная последовательность образует цепь'
					break
			else:
				answer = 'Введенная последовательность  не образует цепь'
				break
	exec_time = time.time() - start_time
	print(answer), print('Время работы: ', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def weight_list(lst):
	weight = int(input('Введите вес(список): '))
	start_time = time.time()
	for k in range(10 ** 6):
		verts = []
		for i in lst:
			for j in i[0]:
				if j not in verts:
					verts += [j]
		verts = np.sort(verts)
		sums = [0 for i in range(len(verts))]
		for i in range(len(verts)):
			for j in lst:
				if verts[i] in j[0]:
					sums[i] += j[1]
		sums = [i for i in range(len(sums)) if sums[i] > weight]
	exec_time = time.time() - start_time
	print('Номера вершин: ', sums), print("Время работы: ", exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def edge_list(lst):
	start_time = time.time()
	for i in range(10 ** 6):
		edges = len(lst)
	exec_time = time.time() - start_time
	print('Количество ребер: ', edges), print('Время работы: ', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def sosed_rec(array):
	sosed_input = int(input('Номер вершины для поиска соседей (массив): '))
	start_time = time.time()
	for j in range(10 ** 6):
		for i in array:
			if i['Номер'] == sosed_input:
				sosed_num = i['Кол. соседей']
				break
	exec_time = time.time() - start_time
	print('Соседи: ', sosed_num), print('Время работы: ', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def chain_rec(array):
	chain = input('Введите последовательность (массив): ').split()
	start_time = time.time()
	for k in range(10 ** 6):
		for i in range(len(chain) - 1):
			for j in array:
				if j['Номер'] == int(chain[i]) \
						and int(chain[i + 1]) != int(chain[i]) \
						and int(chain[i + 1]) in j['Дети']:
					answer = 'Введенная последовательность образует цепь'
					break
			else:
				answer = 'Введенная последовательность не образует цепь'
				break
	exec_time = time.time() - start_time
	print(answer), print('Время работы: ', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def weight_rec(array):
	weight = int(input('Введите вес (массив): '))
	start_time = time.time()
	for j in range(10 ** 6):
		verts = []
		for i in array:
			if i['Сумма веса'] > weight:
				verts += [i['Номер']]
	exec_time = time.time() - start_time
	print('Номера вершин: ', verts), print('Время работы: ', exec_time)
	print('Среднее время выполнения: ', exec_time / 10 ** 6)


def edge_rec(array):
	start_time = time.time()
	for j in range(10 ** 6):
		edges = 0
		for i in array:
			edges += len(i['Дети'])
	exec_time = time.time() - start_time
	print('Количество ребер: ', edges), print('Время работы: ', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


def plot_graf(rec_array, lst_smz):
	G = igraph.Graph(directed=True)
	G.add_vertices(5)
	G.vs['label'] = [rec_array[i]['Имя'] for i in range(len(rec_array))]
	G.add_edges([i[0] for i in lst_smz])
	# Веса
	G.es['label'] = [i[1] for i in lst_smz]
	layout = G.layout('kk')
	igraph.plot(G, 'graph.png', bbox=(800, 600), layout=layout, vertex_size=40, vertex_label_size=10)
	os.startfile(r'../graph.png')


def chain_cicle(array):
	chain = input('Введите последовательность (массив): ').split()

	flag = 0
	chars = "0123456789"
	for char in chars:
		count = chain[1: -1].count(char)
		if count > 1:
			flag = 1
			break

	start_time = time.time()
	for k in range(10 ** 6):
		for i in range(len(chain) - 1):
			for j in array:
				if j['Номер'] == int(chain[i]) \
						and int(chain[i + 1]) != int(chain[i]) \
						and int(chain[i + 1]) in j['Дети']:
					answer = 'Введенная последовательность образует цепь'
					if answer == 'Введенная последовательность образует цепь' \
							and chain[0] == chain[-1] and flag == 0:
						answer += ' , а так же, введенная последовательность образует простой цикл'
					elif answer == 'Введенная последовательность образует цепь' \
							and chain[0] == chain[-1] and flag == 1:
						answer += ' , а так же, введенная последовательность образует цикл'
					break
			else:
				answer = 'Введенная последовательность не образует цепь'
				break
	exec_time = time.time() - start_time
	print(answer), print('Время работы: ', exec_time)
	print('Ср. время работы: ', exec_time / 10 ** 6)


lst_smz = list_smezh(matrix_smez)
rec_array = record_array(matrix_smez)


def choose():
	print("Выбор действий:")
	print("(1) Показать граф  \n"
	      "(2) Найти соседей (матрица) \n"
	      "(3) Найти цепь(матрица) \n"
	      "(4) Найти сумму весов(матрица) \n"
	      "(5) Найти кол. ребер (матрица) \n"
	      "(6) Найти соседей(список) \n"
	      "(7) Найти цепт(список) \n"
	      "(8) Найти сумму весов(список) \n"
	      "(9) Найти кол. ребер (список) \n"
	      "(10) Найти соседей(массив) \n"
	      "(11) Найти цепт(массив) \n"
	      "(12) Найти сумму весов(массив) \n"
	      "(13) Найти кол. ребер (массив) \n"
	      "(14) Доп задание (массив) \n"
	      )
	print("Ввод ")
	chs = int(input())
	if chs == 1:
		plot_graf(rec_array, lst_smz)
	if chs == 2:
		search_matrix(matrix_smez)
	if chs == 3:
		chain_matrix(matrix_smez)
	if chs == 4:
		weight_matrix(matrix_smez)
	if chs == 5:
		edge_matrix(matrix_smez)
	if chs == 6:
		sosed_list(lst_smz)
	if chs == 7:
		chain_list(lst_smz)
	if chs == 8:
		weight_list(lst_smz)
	if chs == 9:
		edge_list(lst_smz)
	if chs == 10:
		sosed_rec(rec_array)
	if chs == 11:
		chain_rec(rec_array)
	if chs == 12:
		weight_rec(rec_array)
	if chs == 13:
		edge_rec(rec_array)
	if chs == 14:
		chain_cicle(rec_array)


while True:
	choose()
