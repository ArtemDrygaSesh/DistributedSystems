import hazelcast
import time

hz = hazelcast.HazelcastClient(cluster_name='lab2')
map = hz.get_map('lab2-map').blocking()

map.put_if_absent("key", 0)

start = time.time()

for i in range(10000):
    value = map.get("key")
    map.put("key", value + 1)

print(f"No lock executed in: {time.time() - start:.2f} seconds")

hz.shutdown()