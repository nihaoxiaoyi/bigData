import csv
import apriro
import sx_dataClean
from apyori import apriori
# 数据集根路径（根据个人电脑实际情况修改)
filename_root = "F:\hlt_export_data\dataset_correlation\measure_point_"
# 字典，用于结构化存储清洗和预处理过后的数据集
dict_dataset = {}
# 总样本量
total_time = []
# 遍历20个测点数据csv文件
for i in range(20):
    time_list = []
    filename = filename_root + str(i) + ".csv"
    with open(filename) as f:
        reader = csv.reader(f)
        # 去除首行的label信息
        header_row = next(reader)
        for row in reader:
            time_list.append(row[1])
        # 数据清洗与预处理
        time_list = sx_dataClean.dataCleansing(time_list)
        total_time += time_list
    dict_dataset[i] = time_list

# 总样本去重，并再进行一次数据清洗，得到最终的总样本
total_time = list(set(total_time))
total_time.sort()
total_time = sx_dataClean.dataCleansing(total_time)
print(dict_dataset)
print(total_time)

# 将20个测点字典数据分别与总样本进行时间对齐
for i in range(20):
    dict_dataset[i] = sx_dataClean.outDataCleansing(total_time, dict_dataset[i])

# 字典，用于存储transaction，用于寻找频繁项集
dict_pfxj = {}
count = 0
for j in range(len(total_time)):
    dict_pfxj[count] = []
    for i in range(20):
        if total_time[j] in dict_dataset[i]:
            dict_pfxj[count].append(i)
    if len(dict_pfxj[count]) == 1:
        del dict_pfxj[count]
    else:
        count += 1
for i in range(len(dict_pfxj)):
    print(dict_pfxj[i])
print(dict_pfxj)
data_set = []
for i in range(len(dict_pfxj)):
    data_set.append(dict_pfxj[i])

# 手动实现的apriori算法
print("手动实现apriori")
L, suppData = apriro.apriori(data_set)
print(L)
print(suppData)

# 调用apriori算法库
print("调用apriori库")
L_r = list(apriori(transactions=data_set, min_support=0.2))
print(L_r)



