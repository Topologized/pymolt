a = int(input())
b = int(input())

if a < b - 1:
	print(a)
elif a < b:
	print(a, b)
elif a < b + 1:
	print(b, a)
	for i in range(b):
		print(i)
else:
	print(b)