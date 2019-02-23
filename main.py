import operator
import pprint
from collections import Counter
from functools import reduce

import pandas as pd
import pkuseg

from draw import (drawFavouriteJiDu, drawPostFavouriteMean, drawPostHour,
                  drawPostHourAndFavourite, drawPostJiDu,
                  drawTitleLenAndFavourite, drawWordCloud)

seg = pkuseg.pkuseg()


# 数据清理（分词和去掉停用词）
def cleanWord(content):
    # 分词
    text = seg.cut(content)
    # 读取停用词
    stopwords = []
    with open("stopwords/哈工大停用词表.txt", encoding="utf-8") as f:
        stopwords = f.read()

    new_text = []
    # 去掉停用词
    for w in text:
        if w not in stopwords:
            new_text.append(w)

    return new_text


# 选择文章标题并分析
def chooseMostPop50Titles(df):
    texts = []
    for title in list(df['标题']):
        if len(str(title)) > 3:
            if str(title) not in ['分享图片']:
                text = cleanWord(str(title))
                texts.append(text)
    title_cuts = reduce(operator.add, texts)

    # 统计每个词的词频
    counter = Counter(title_cuts)
    # 选出词频最高的30个
    counter = counter.most_common(50)
    # 输出词频最高的15个单词
    pprint.pprint(counter)
    name = []
    value = []
    for count in counter:
        name.append(count[0])
        value.append(count[1])
    return drawWordCloud(name, value)


if __name__ == "__main__":
    df = pd.read_excel('data/data.xlsx')

    # 获取转载文章
    df_copy = df[df['原文链接'].str.len() > 5]
    print('转载文章数量为：'+str(len(df_copy)))
    print('原创文章数量为：'+str(len(df)-len(df_copy)))

    line1 = drawPostJiDu(df)
    line1.render(path='output/1.jpeg')

    line2 = drawFavouriteJiDu(df)
    line2.render(path='output/2.jpeg')

    line = drawPostFavouriteMean(df)
    line.render(path='output/3.jpeg')

    pie = drawPostHour(df)
    pie.render(path='output/4.jpeg')

    wordcloud = chooseMostPop50Titles(df)
    wordcloud.render(path='output/5.jpeg')

    bar1 = drawTitleLenAndFavourite(df)
    bar1.render(path='output/6.jpeg')

    bar2 = drawPostHourAndFavourite(df)
    bar2.render(path='output/7.jpeg')
