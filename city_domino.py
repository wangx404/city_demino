# -*- coding: utf-8 -*-
from pypinyin import lazy_pinyin
from collections import defaultdict
import random


def load_city_list(txt):
    '''
    加载存储于 txt 文件中的城市列表，并去重。
    :param txt: 存储有城市列表的 txt 文件路径
    :return: 去重后的城市名称集合
    '''
    with open(txt, 'r', encoding='utf-8') as f:
        cities = [line.strip() for line in f if line.strip()]
    return set(cities)


def get_city_dict(city_list):
    '''
    得到一个键为拼音、值为城市列表的字典，用于接龙查询。
    :param city_list: 包含城市名称的列表/元组/集合等
    :return: 形式为 {'hai': ['海淀', ...]} 的字典
    '''
    py2city_dict = defaultdict(list)
    for city in city_list:
        pinyin = lazy_pinyin(city[0])[0]
        py2city_dict[pinyin].append(city)
    return py2city_dict


def remove_city(py2city_dict, city):
    '''
    从接龙字典中移除已使用的城市，保证同一城市不会被再次使用。
    :param py2city_dict: 拼音到城市列表的字典
    :param city: 要移除的城市名称
    '''
    if not city:
        return
    pinyin = lazy_pinyin(city[0])[0]
    candidates = py2city_dict.get(pinyin)
    if not candidates:
        return
    try:
        candidates.remove(city)
    except ValueError:
        return
    if not candidates:
        del py2city_dict[pinyin]


def find_next_city(py2city_dict, city):
    '''
    根据城市名称最后一个字的拼音查询下一个接龙城市。
    仅从未使用过的城市中选择；若无可用城市则返回 None。
    :param py2city_dict: 拼音到城市列表的字典（会随使用而缩小）
    :param city: 当前城市
    :return: 下一个城市；若无则返回 None
    '''
    pinyin = lazy_pinyin(city[-1])[0]
    city_list = py2city_dict.get(pinyin)
    if not city_list:
        return None
    next_city = random.choice(city_list)
    remove_city(py2city_dict, next_city)
    return next_city


def city_domino(py2city_dict, max_epoch=20):
    '''
    在最大次数限制下进行城市接龙，每个城市名称最多使用一次。
    :param py2city_dict: 拼音到城市列表的字典
    :param max_epoch: 最大接龙次数
    '''
    city = input('请输入首先要接龙的城市:').strip()
    if not city:
        print('未输入城市，结束接龙。')
        return

    # 起始城市也计入已使用，避免后续再次出现
    remove_city(py2city_dict, city)

    for index in range(1, max_epoch + 1):
        city = find_next_city(py2city_dict, city)
        if city is None:
            print('黔驴技穷，下面没有城市了。')
            return
        print('下一个城市是：%s' % city)

    print('达到最大接龙次数，最大接龙次数为：%d' % max_epoch)


if __name__ == '__main__':
    max_epoch = 20
    txt = 'city_list.txt'
    city_list = load_city_list(txt)
    py2city_dict = get_city_dict(city_list)
    city_domino(py2city_dict, max_epoch)
