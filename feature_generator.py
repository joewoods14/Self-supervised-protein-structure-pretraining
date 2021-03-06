import os
import numpy as np
import pandas as pd

matrix = [[] for _ in range(10)]
path = 'D:/linux_test_data'
save_path = 'D://test//test'
proteins = []
index = 0
#遍历文件夹，读取同一特征
for file in os.listdir(path):
    array = np.load(os.path.join(path, file))
    for i in range(array.shape[0]):
        for j in range(array.shape[2]):
            for z in range(array.shape[1]):
                matrix[j].append(array[i][z][j])
    #文件名，开始位置，结束位置
    proteins.append([file, index * array.shape[1], (index + array.shape[0])* array.shape[1]])
    index += array.shape[0]
    
#根据分布等频划分，转换为one-hot
bucket = pd.qcut(matrix[0], 20, duplicates = 'drop', labels = False) 
df = pd.DataFrame([str(i) for i in bucket])
new_feature = pd.get_dummies(df).values
for i in range(1, len(matrix)):
    bucket = pd.qcut(matrix[i], 20, duplicates = 'drop', labels = False) 
    df = pd.DataFrame([str(i) for i in bucket])
    feature = pd.get_dummies(df).values
    new_feature = np.concatenate([new_feature, feature], axis = 1)

# 切割蛋白质，根据proteins
for filename, start, end in proteins:
    file_feature = new_feature[start:end]
    file_feature = file_feature.reshape(file_feature.shape[0]//15, 15, new_feature.shape[1])
    np.save(os.path.join(save_path, filename), file_feature)
    print(file_feature.shape)

