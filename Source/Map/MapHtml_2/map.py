from pyecharts import options as opts
from pyecharts.charts import Map


def map_visualmap() -> Map:
    name = []
    value = []
    with open("确诊人数.txt", encoding='utf-8') as f:
        txt = f.read().split('\n')
        for i in txt:
            newtxt = i.split(",")
            name.append(newtxt[0])
            value.append(int(newtxt[1]))
    c = (
        Map()
        .add("确诊点", [list(z) for z in zip(name, value)],"china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各省确诊人数"),
            #visualmap_opts=opts.VisualMapOpts(max_=max(value)),
            visualmap_opts=opts.VisualMapOpts(max_=500),
        )
    )
    return c
map_visualmap().render()