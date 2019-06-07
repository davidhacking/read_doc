import tracemalloc

# Store 25 frames
tracemalloc.start(25)

x = {
    'a', '111' * (12024 * 1200),
    'b', '111' * (12024 * 1200),
}

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('traceback')

# pick the biggest memory block
for stat in top_stats[:10]:
    print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
    for line in stat.traceback.format():
        print(line)