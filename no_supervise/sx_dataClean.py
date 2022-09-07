# 数据清洗与预处理  区分20个标签测点的告警
def dataCleansing(minDataList):
    # 去除秒级数据，只保留分钟前的数据
    for j in range(len(minDataList)):
        minDataList[j] = minDataList[j][0:16]
    # 利用集合的性质去除重复的数据
    minDataList = list(set(minDataList))
    minDataList.sort()

    # 区分告警，将相隔10分钟内的告警聚类在一起
    i = 0
    while i < len(minDataList):
        temp = minDataList[i]
        other = temp[0:11]
        hour = int(temp[11:13])
        min = int(temp[14:16])
        while True:
            j = i + 1
            if j >= len(minDataList):
                break
            tempi = minDataList[j]
            otheri = tempi[0:11]
            # print(otheri)
            houri = int(tempi[11:13])
            mini = int(tempi[14:16])
            if other == otheri:
                if houri - hour > 1:
                    break
                elif houri - hour == 1:
                    if mini + 60 - min > 10:
                        break
                    else:
                        del minDataList[j]
                else:
                    if mini - min <= 10:
                        del minDataList[j]
                    else:
                        break
            else:
                break
        i = i + 1
    return minDataList


# 单测点告警时间与总样本量时间对齐
def outDataCleansing(dcm1, dcm2):
    # 两个集合的交集，即只对齐时间不一致的元素
    sa12 = set(dcm2) & set(dcm1)
    a12 = list(sa12)
    a12.sort()
    dcm1dev = list(set(dcm1) - sa12)
    dcm1dev.sort()
    dcm2dev = list(set(dcm2) - sa12)
    dcm2dev.sort()
    i = 0
    j = 0
    while i < len(dcm1dev) and j < len(dcm2dev):
        tempi = dcm1dev[i]
        tempj = dcm2dev[j]
        otheri = tempi[0:10]
        otherj = tempj[0:10]
        if tempi > tempj:
            houri = int(tempi[11:13])
            mini = int(tempi[14:16])
            hourj = int(tempj[11:13])
            minj = int(tempj[14:16])
            if otherj == otheri:
                if houri - hourj > 1:
                    j = j + 1
                elif houri - hourj == 1:
                    if mini + 60 - minj > 10:
                        j = j + 1
                    else:
                        dcm2dev[j] = dcm1dev[i]
                        j = j + 1
                        i = i + 1
                else:
                    if mini - minj <= 10:
                        dcm2dev[j] = dcm1dev[i]
                        j = j + 1
                        i = i + 1
                    else:
                        j = j + 1
            else:
                j = j + 1
        else:
            houri = int(tempi[11:13])
            mini = int(tempi[14:16])
            hourj = int(tempj[11:13])
            minj = int(tempj[14:16])
            if otherj == otheri:
                if hourj - houri > 1:
                    i = i + 1
                elif hourj - houri == 1:
                    if minj + 60 - mini > 10:
                        i = i + 1
                    else:
                        dcm2dev[j] = dcm1dev[i]
                        j = j + 1
                        i = i + 1
                else:
                    if minj - mini <= 10:
                        dcm2dev[j] = dcm1dev[i]
                        j = j + 1
                        i = i + 1
                    else:
                        i = i + 1
            else:
                i = i + 1
    d2 = list(set(dcm2dev) | sa12)
    d2.sort()
    return d2