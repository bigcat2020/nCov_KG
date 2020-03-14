from get_map import GetMap


def main():
    with open("确诊人数.txt", "r", encoding="utf-8") as fp:
        list_data = []
        for i in fp.readlines():
            city, num = i.split(',')
            num = num.strip('\n')
            list_data.append([city, num])
        list_data.append(['China', 500])
        print(list_data[1:])

    mp = GetMap(list_data=list_data[1:], map_name="world", show_lb=False, title="世界地图")
    mp.get_map_html("world.html")


if __name__ == '__main__':
    main()