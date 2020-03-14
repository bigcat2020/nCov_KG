from get_map import GetMap


def main():
    with open("确诊人数.txt", "r", encoding="utf-8") as fp:
        list_data = []
        for i in fp.readlines():
            city, num = i.split(',')
            num = num.strip('\n')
            list_data.append([city, num])

    mp = GetMap(list_data=list_data[1:], map_name="china",show_lb=True, title="中国地图")
    mp.get_map_html("china.html")


if __name__ == '__main__':
    main()