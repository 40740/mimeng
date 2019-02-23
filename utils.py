# 获取年份
def getYear(date):
    return int(date.split('-')[0])

# 获取月份
def getMonth(date):
    return int(date.split('-')[1])

# 获取小时
def getHour(time):
    return int(str(time).split(':')[0])

# 获取季度
def getJiDu(date):
    if getMonth(date) in [1, 2, 3]:
        return 1
    if getMonth(date) in [4, 5, 6]:
        return 2
    if getMonth(date) in [7, 8, 9]:
        return 3
    if getMonth(date) in [10, 11, 12]:
        return 4

# 获取文章数随季度变化的矩阵
def getPostJiDu(df):
    list_jidu = [[0]*4 for i in range(5)]
    for articleTime in df['发文时间']:
        date = str(articleTime).split(' ')[0]
        year = getYear(date)
        jidu = getJiDu(date)
        list_jidu[year-2015][jidu-1] += 1
    return list_jidu

# 获取点赞数随季度变化的矩阵
def getFavouriteJiDu(df):
    list_jidu = [[0]*4 for i in range(5)]
    list_dianzan = df['点赞']
    for i in range(len(df['发文时间'])):
        date = str(df['发文时间'][i]).split(' ')[0]
        year = getYear(date)
        jidu = getJiDu(date)
        list_jidu[year-2015][jidu-1] += list_dianzan[i]
    return list_jidu

# 获取发文数量和发文小时的矩阵
def getPostHour(df):
    list_hour = [0]*25
    for articleTime in df['发文时间']:
        time = str(articleTime).split(' ')[1]
        hour = getHour(time)
        list_hour[hour] += 1
    return list_hour
