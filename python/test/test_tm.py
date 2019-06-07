import tracemalloc



def print_stat():
    snapshot = tracemalloc.take_snapshot()
    stats = snapshot.statistics('lineno')
    for s in stats:
        print(s)
        pass


t = None
q = None

def alloc1():
    global t
    t = {
        'a': 'ddd' * (1024 * 1023),
        'c': '777'
    }
    pass

def alloc2():
    global q
    q = {'q': 'q' * (1024 * 1024)}
    pass


tracemalloc.start(5)
alloc1()
print ("sp1 ....")
snapshot1 = tracemalloc.take_snapshot()
for s in snapshot1.statistics('lineno')[:20]:
    print(s)
print ("sp2.......")
alloc2()
snapshot2 = tracemalloc.take_snapshot()
diff = snapshot2.compare_to(snapshot1, 'lineno')
for s in diff[:20]:
    print (s)

