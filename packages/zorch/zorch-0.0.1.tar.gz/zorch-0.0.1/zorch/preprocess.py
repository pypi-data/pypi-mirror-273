# -*- coding:utf-8 -*-

def label_encode(df, column):
    # 获取唯一的标签列表
    unique_labels = df.iloc[:, column].unique()
    # 计算类别的数量
    n_classes = len(unique_labels)
    # 创建从标签到整数的映射字典
    class_to_num = dict(zip(unique_labels, range(n_classes)))
    # 应用映射字典进行标签编码，并添加新列到DataFrame
    df['labelEncoded'] = df.iloc[:, column].map(class_to_num)
    return df


