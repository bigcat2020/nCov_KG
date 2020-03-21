from modl.neo_models import KGneo4j

neo = KGneo4j()
neo.connect_db()
data = neo.find_relation_by_node_one("钟南山")
data1 = neo.find_relation_by_node_two("钟南山")
print(len(data))
print(data1)

for x in data1:
    print(x['e1']['name'])
    print(x['r']['relation'])
    print(x['e2']['name'])


# for i, j in data1[1]['e1'].items():
#     print(i, j)



