fmt = {0 : 'A', 1 : 'B', 2 : 'C'}

# fuckfuck
def recur(n, a, b, c):
    if n == 1:
        print("Disk 1 : {0} to {1}".format(fmt[a], fmt[b]))
        return
    
    recur(n - 1, a, c, b)
    print("Disk {0} : {1} to {2}".format(n, fmt[a], fmt[b]))
    recur(n - 1, c, b, a)

N = int(input())
recur(N, 0, 2, 1)