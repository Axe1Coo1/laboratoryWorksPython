def resources(a, b):
	c = []
	d = []
	for i in range(1, 8):
		temp = []
		tempX = []
		for j in range(i + 1):
			temp.append(round(a[j] + b[i - j], 1))
		m = temp[0]
		for p in range(len(temp)):
			if temp[p] >= m:
				m = temp[p]
		for p in range(len(temp)):
			if temp[p] == m:
				tempX.append(p)
		c.append(tempX)
		d.append(m)
	return [c, d]


f1 = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
f2 = [1.0, 1.1, 1.2, 1.2, 1.4, 1.5, 1.7]
f3 = [1.2, 1.4, 1.6, 1.7, 1.8, 1.9, 1.9]
f4 = [0.8, 0.9, 1.1, 1.2, 1.3, 1.4, 1.5]
f5 = [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0]

print("Таблица ресурсов:")

for i in range(len(f1)):
	print(f1[i], ' ', f2[i], ' ', f3[i], ' ', f4[i], ' ', f5[i], ' ')

x5 = [[0], [1], [2], [3], [4], [5], [6], [7]]
f1, f2, f3, f4, w5 = [0] + f1, [0] + f2, [0] + f3, [0] + f4, [0] + f5
w1, w2, w3, w4, x1, x2, x3, x4 = [], [], [], [], [], [], [], []
x4 = resources(f4, w5)[0]
w4 = [0] + resources(f4, w5)[1]
x3 = resources(f3, w4)[0]
w3 = [0] + resources(f3, w4)[1]
x2 = resources(f2, w3)[0]
w2 = [0] + resources(f2, w3)[1]
x1 = resources(f1, w2)[0]
w1 = resources(f1, w2)[1]
w2.pop(0), w3.pop(0), w4.pop(0), w5.pop(0), x5.pop(0)

del f1, f2, f3, f4, f5, i

x_all = [x1, x2, x3, x4, x5]
s = 7
x = []
for i in range(len(x_all)):
	x.append(x_all[i][s - 1][0])
	s = s - x_all[i][s - 1][0]

del s, x_all
print("\nРешение: ")
print(x)
