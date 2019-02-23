import operator
import pprint
from collections import Counter
from functools import reduce

import numpy as np
from pyecharts import Bar, Line, Pie, WordCloud, configure

from utils import (getFavouriteJiDu, getHour, getJiDu, getMonth, getPostHour,
                   getPostJiDu, getYear)

# 将这行代码置于首部，设置全局图表主题
configure(global_theme='vintage')

# 画出发文数量随季度变化的走势图
def drawPostJiDu(df):
    res_list = getPostJiDu(df)
    # 构造标题列表
    attr = []
    for year in range(len(res_list)):
        for month in range(len(res_list[year])):
            attr.append("{}年第{}季度".format(str(year+2015), str(month+1)))

    # 构造值列表
    v1 = reduce(operator.add, res_list)

    # 去掉无用值
    attr = attr[2:-3]
    v1 = v1[2:-3]

    line = Line("发文数量变化走势图", width=1500, height=500)
    line.add("某知名公众号", attr, v1, is_stack=True,
             is_label_show=True, is_smooth=True, is_fill=True,  xaxis_name='季度', yaxis_name='发文数', xaxis_rotate=30, mark_line=['average'])
    return line

# 画出发文数量随季度变化的走势图
def drawFavouriteJiDu(df):
    res_list = getFavouriteJiDu(df)
    # 构造标题列表
    attr = []
    for year in range(len(res_list)):
        for month in range(len(res_list[year])):
            attr.append("{}年第{}季度".format(str(year+2015), str(month+1)))

    # 构造值列表
    v1 = reduce(operator.add, res_list)
    # 去掉无用值
    attr = attr[2:-3]
    v1 = v1[2:-3]

    line = Line("点赞数量变化走势图", width=1500, height=500)
    line.add("某知名公众号", attr, v1, is_stack=True,
             is_label_show=True, is_smooth=True, is_fill=True, xaxis_name='季度', yaxis_name='点赞数', xaxis_rotate=30, mark_line=['average'])
    return line

# 画出平均每篇文章的点赞量随季度变化的走势图
def drawPostFavouriteMean(df):
    post_list = getPostJiDu(df)
    fav_list = getFavouriteJiDu(df)
    res_list = np.array(fav_list)/np.array(post_list)
    res_list = np.nan_to_num(res_list)
    # 构造标题列表
    attr = []
    for year in range(len(res_list)):
        for month in range(len(res_list[year])):
            attr.append("{}年第{}季度".format(str(year+2015), str(month+1)))
    # 构造值列表
    v1 = res_list.flatten()
    # 去掉无用值
    attr = attr[2:-3]
    v1 = v1[2:-3]

    line = Line("平均每篇文章点赞数量变化走势图", width=1500, height=600)
    line.add("某知名公众号", attr, v1, is_stack=True, is_label_show=True, is_smooth=True,
             is_fill=True, xaxis_name='季度', yaxis_name='点赞数', xaxis_rotate=30, mark_line=['average'])
    return line

# 画出发文数量和所在小时之间的饼状关系图
def drawPostHour(df):
    # 获取发文时间
    list_hour = getPostHour(df)
    array = np.array(list_hour)
    # 获取发文时间最多的5个时间段
    attr = list(sorted(np.argsort(array)[-5:]))
    attr = ["{}时".format(i) for i in attr]
    # 获取发文时间最多的5个时间的数量
    v1 = list(array[sorted(np.argsort(array)[-5:])])
    pie = Pie("发文时间分布图")
    pie.add("", attr, v1, is_label_show=True)
    return pie

# 数据可视化（生成词云)
def drawWordCloud(name, value):
    wordcloud = WordCloud(width=800, height=400)
    wordcloud.add("标题词云图", name, value, word_size_range=[
                  20, 100], rotate_step=20)
    return wordcloud

# 画出标题长度和点赞数之间的关系
def drawTitleLenAndFavourite(df):
    v1 = [0]*6
    for i in range(len(df['标题'])):
        title_len = len(str(df['标题'][i]))
        if title_len >= 5 and title_len <= 8:
            v1[0] += df['点赞'][i]
        elif title_len >= 9 and title_len <= 12:
            v1[1] += df['点赞'][i]
        elif title_len >= 13 and title_len <= 16:
            v1[2] += df['点赞'][i]
        elif title_len >= 17 and title_len <= 20:
            v1[3] += df['点赞'][i]
        elif title_len >= 20 and title_len <= 24:
            v1[4] += df['点赞'][i]
        elif title_len >= 25:
            v1[5] += df['点赞'][i]
    attr = ['5-8', '9-12', '13-16', '17-20', '21-24', '24+']
    bar = Bar("标题长度和点赞数之间的关系", title_pos='center')
    bar.add("", attr, v1, is_label_show=True)
    return bar

# 画出点赞数和所在小时的柱状关系图
def drawPostHourAndFavourite(df):
    list_hour = [0]*25
    list_dianzan = list(df['点赞'])
    for i in range(len(df['发文时间'])):
        articleTime = df['发文时间'][i]
        time = str(articleTime).split(' ')[1]
        hour = getHour(time)
        list_hour[hour] += list_dianzan[i]
    attr = ["{}时".format(i) for i in range(0, 25)]
    bar = Bar("发文时间和点赞数之间的关系", title_pos='center', width=1500)
    bar.add("", attr, list_hour, is_label_show=True)
    return bar
