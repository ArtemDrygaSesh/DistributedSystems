import hazelcast
import time

hz = hazelcast.HazelcastClient(cluster_name='lab2')
map = hz.get_map('lab2-map').blocking()

start = time.time()

map.put_if_absent("key3", 0)

for i in range(10000):
        while True:
            oldcounter = map.get("key3")
            newcounter = oldcounter + 1
            if map.replace_if_same("key3", oldcounter, newcounter): break

print(f"Optimistic map executed in: {time.time() - start:.2f} seconds")

hz.shutdown()