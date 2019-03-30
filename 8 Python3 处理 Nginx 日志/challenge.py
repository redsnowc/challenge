import re


def get_list(file_name):
    list_ip = []
    list_url = []
    regex = re.compile(r'''
        (\d+.\d+.\d+.\d+)\s-\s-\s
        \[(\d+/Jan/2017).+\]\s
        "GET\s(.+)\s\w+/.+"\s
        (\d+)\s
        (\d+)\s
        "(.+)"\s
        "(.+)"
    ''', re.VERBOSE)

    with open(file_name) as f_obj:
        mo = regex.findall(f_obj.read())

    for value in mo:
        if '11/Jan/2017' in value:
            list_ip.append(value[0])
        if value[3] == '404':
            list_url.append(value[2])

    return list_ip, list_url


def get_value(list):
    list_set = []
    sets = set(list)
    num = 0
    for i in sets:
        list_set.append((i, list.count(i)))

    for i in list_set:
        if num < i[1]:
            num = i[1]
            value = i[0]

    return {value: num}


def main():
    list_ip, list_url = get_list('nginx.log')
    dict_ip = get_value(list_ip)
    dict_url = get_value(list_url)
    return dict_ip, dict_url


if __name__ == '__main__':
    print(main())
