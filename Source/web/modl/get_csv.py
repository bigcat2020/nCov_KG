import pandas as np


def get_csv_data(dm):
    cs = np.read_csv("china.csv")
    for i in cs.values:
        if i[0] == dm:
            return i

    cs = np.read_csv("china_city.csv")
    for i in cs.values:
        if i[1] == dm:
            return i

    cs = np.read_csv("world.csv")
    for i in cs.values:
        if i[0] == dm:
            return i

    return []


def china_findall():
    cs = np.read_csv("china.csv")
    return cs.values



cs = np.read_csv("out_nodes.csv")
s = set()
for i in cs['nodeclass']:
    s.add(i)
print(s)
print("国家政策事件"in s)