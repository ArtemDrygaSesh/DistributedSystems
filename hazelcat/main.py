import hazelcast

hz = hazelcast.HazelcastClient(cluster_name='lab2')
map = hz.get_map('lab2-map').blocking()

for key in range(1000): map.set(key, key)

hz.shutdown()