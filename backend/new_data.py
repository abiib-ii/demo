import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 读取数据集
file_path = r"c:\Users\24130\Desktop\stress-prediction-frontend\StressLevelDataset.csv"
df = pd.read_csv(file_path)

# 分离特征和目标变量
X = df.iloc[:, :-1]  # 所有列，除了最后一列
y = df.iloc[:, -1]   # 最后一列 (stress_level)

# 检查数据类型并转换为数值型
for column in X.columns:
    if X[column].dtype == 'object':
        # 将分类变量转换为数值
        X[column] = pd.Categorical(X[column]).codes

# 标准化特征 - 这有助于SHAP分析
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

# 训练随机森林模型
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
model.fit(X_scaled_df, y)

# 获取特征重要性
feature_importance = model.feature_importances_
features = X.columns

# 打印特征重要性
importance_df = pd.DataFrame({'特征': features, '重要性': feature_importance})
importance_df = importance_df.sort_values('重要性', ascending=False)
print("特征重要性排序:")
print(importance_df)

# 生成新数据 - 确保维度一致性
n_samples = 1000  # 固定样本数量，避免过大
n_features = len(X.columns)

# 使用多元正态分布生成相关特征
# 首先计算特征之间的协方差矩阵
cov_matrix = np.cov(X_scaled, rowvar=False)

# 生成多元正态分布的数据
mean_vector = np.zeros(n_features)  # 标准化后的均值为0
new_features_scaled = np.random.multivariate_normal(mean_vector, cov_matrix, n_samples)

# 转换回原始尺度
new_features = scaler.inverse_transform(new_features_scaled)

# 创建新的DataFrame
new_data = pd.DataFrame(new_features, columns=X.columns)

# 确保所有整数列都是整数类型
for column in X.columns:
    if df[column].dtype == 'int64':
        new_data[column] = np.round(new_data[column]).astype(int)
    
    # 确保值在合理范围内
    min_val = df[column].min()
    max_val = df[column].max()
    new_data[column] = new_data[column].clip(min_val, max_val)

# 使用训练好的模型预测新数据的目标变量
new_data_scaled = scaler.transform(new_data)
new_data['stress_level'] = model.predict(new_data_scaled)

# 保存新生成的数据
new_file_path = r"c:\Users\24130\Desktop\stress-prediction-frontend\ShapCompatibleDataset.csv"
new_data.to_csv(new_file_path, index=False)

print(f"新数据已保存到: {new_file_path}")

# 显示原始数据和新数据的统计信息比较
print("\n原始数据统计信息:")
print(df.describe())

print("\n新数据统计信息:")
print(new_data.describe())

# 显示原始数据和新数据的目标变量分布比较
print("\n原始数据目标变量分布:")
print(df['stress_level'].value_counts(normalize=True))

print("\n新数据目标变量分布:")
print(new_data['stress_level'].value_counts(normalize=True))

# 测试SHAP兼容性
try:
    import shap
    # 创建一个简单的解释器
    explainer = shap.TreeExplainer(model)
    
    # 取一小部分数据进行测试
    test_data = new_data.iloc[:10, :-1]
    test_data_scaled = scaler.transform(test_data)
    
    # 计算SHAP值
    shap_values = explainer.shap_values(test_data_scaled)
    
    # 检查维度
    if isinstance(shap_values, list):
        print("\nSHAP值维度检查 (多分类):")
        for i, sv in enumerate(shap_values):
            print(f"类别 {i}: {sv.shape}")
    else:
        print("\nSHAP值维度检查 (二分类):")
        print(f"SHAP值形状: {shap_values.shape}")
        print(f"测试数据形状: {test_data_scaled.shape}")
    
    print("SHAP兼容性测试通过！")
except Exception as e:
    print(f"SHAP兼容性测试失败: {str(e)}")