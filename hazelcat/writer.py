import hazelcast
import time

hz = hazelcast.HazelcastClient(cluster_name='lab2')
queue = hz.get_queue("bounded-queue").blocking()

for i in range(100):
    queue.put(i)
    print(f'i: {i} queue capacity: {queue.remaining_capacity()}')
queue.put(-1)

hz.shutdown()