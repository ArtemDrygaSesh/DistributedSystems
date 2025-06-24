import hazelcast

hz = hazelcast.HazelcastClient(cluster_name='lab2')
map = hz.get_map('lab2-map').blocking()

print("Final value 1:", map.get("key"))
print("Final value 2:", map.get("key2"))
print("Final value 3:", map.get("key3"))
hz.shutdown()