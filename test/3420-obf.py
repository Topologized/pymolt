tmp = {0 : 'A', 1 : 'B', 2 : 'C'}
def g(d, var, var1, i):
    if d == 1:
        print("Disk 1 : {0} to {1}".format(tmp[var], tmp[var1]))
        return
    g(d - 1, var, i, var1)
    print("Disk {0} : {1} to {2}".format(d, tmp[var], tmp[var1]))
    g(d - 1, i, var1, var)
b = int(input())
g(b, 0, 2, 1)