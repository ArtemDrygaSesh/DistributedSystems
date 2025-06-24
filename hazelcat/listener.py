import hazelcast
import time

start = time.time()

hz = hazelcast.HazelcastClient(cluster_name='lab2')
queue = hz.get_queue('bounded-queue').blocking()

while True:
    item = queue.take()
    print(f"Recieved: {item}")

hz.shutdown()