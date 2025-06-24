import hazelcast
import time

hz = hazelcast.HazelcastClient(cluster_name='lab2')
map = hz.get_map('lab2-map').blocking()

start = time.time()

map.put_if_absent("key2", 0)

for i in range(10000):
    map.lock("key2")
    try:
        value = map.get("key2")
        map.put("key2", value + 1)
    finally:
        map.unlock("key2")

print(f"Pessimistic map executed in: {time.time() - start:.2f} seconds")

hz.shutdown()