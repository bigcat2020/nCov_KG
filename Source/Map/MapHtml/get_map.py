from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Map
# world


class GetMap:
    def __init__(self, list_data, map_name="china", max_=1000, show_lb=False, title="中国地图"):
        self.list_data = list_data  # 数据项[['武汉', 100], ['广安', 50]]  世界地图地名给英文名字
        self.map_name = map_name  # 地图名 中国，china。 世界world
        self.max_ = max_  # 设置最大值
        self.show_lb = show_lb  # 设置是否显示地名
        self.title = title

    def map_guangdong(self) -> Map:
        c = (
            Map()
            .add("疫情人数分布", data_pair=self.list_data, maptype=self.map_name)
            .set_global_opts(
                title_opts=opts.TitleOpts(title=self.title),
                visualmap_opts=opts.VisualMapOpts(max_=self.max_),

            )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=self.show_lb))


        )

        return c

    def get_map_html(self, file_name):
        self.map_guangdong().render(file_name)


def main():
    with open("确诊人数.txt", "r", encoding="utf-8") as fp:
        list_data = []
        for i in fp.readlines():
            city, num = i.split(',')
            num = num.strip('\n')
            list_data.append([city, num])



    mp = GetMap(list_data)
    mp.get_map_html("aaa.html")


if __name__ == '__main__':
    main()










