if Reordering
- if (cond): (1) else: (2)
 -> if not (cond): (2) else: (1)
- if (cond1): (1) elif (cond2): (2) elif (cond3): (3) ...
 -> permute
Operator reordering
- a + b, a * b
 -> b + a, b * a
 (only if at least one is integer / float)
variable renaming
- anything that got a assignment
parameter reordering
- does what it says
variable shifting
- for i in range(n):
 -> for i in range(-1, n - 1):
 -> for i in range(1, n + 1):
- for i in range(a, b):
 -> shift
comprehension -> array
- f(a) for a in x
 -> l = []
    for a in x:
      l.append(f(a))
    l
conditional renaming (a<=b <-> not a>b)
- A (< > <= >= == !=) B <-> not A (>= <= > < != ==) B
remove comments
