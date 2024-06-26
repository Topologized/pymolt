# Priority is higher on top

## variable, parameter, function renaming (easy~medium)
Use a thesaurus. Also you can change some variables into one/two letters.

## remove comments (easy)
this is very easy

I think redbaron may not even support comments
idk

## statement reordering (hard)
```py
a = b
c = d
```
to
``` py
c = d
a = b
```
we need to know when two statements are independent

function definitions can be reordered too

## conditional renaming (a<=b <-> not a>b)
`A (< > <= >= == !=) B <-> not A (>= <= > < != ==) B`

## if Reordering (medium)
```py
if (cond):
  do this
else:
  do that
```
to 
```py
if not (cond):
  do that
else: 
  do this
```

Generalize if possible

## Operator reordering (medium~hard)
``a + b, a * b``
to
``b + a, b * a``

(only if at least one is integer / float)

## variable shifting (medium~hard)
```py
for i in range(a):
  do something with i
```
to
```py
for i in range(1, a + 1):
  do something with i - 1
```
or
```py
for i in range(-1, a - 1):
  do something with i + 1
```

## comprehension -> array (medium)
```py
something(a(x) for x in t)
```
to
```py
l = []
for x in t:
  l.append(x)
something(l)
```
