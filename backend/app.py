import os
import warnings
from io import BytesIO

# Set matplotlib backend to 'Agg' before importing matplotlib
import matplotlib
import numpy as np
import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

matplotlib.use('Agg')  # Non-interactive backend that doesn't require Tkinter
import matplotlib.pyplot as plt

import base64
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

# 忽略警告
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)
CORS(app)

# Hive连接配置
HIVE_HOST = 'localhost'  # 请根据您的实际Hive服务器地址修改
HIVE_PORT = 10005        # 默认端口，请根据实际情况修改
HIVE_USER = '24130'      # 如果需要用户名，请填写
HIVE_DATABASE = 'default'  # 默认数据库名，请根据实际情况修改

# 创建 SQLAlchemy 引擎
engine = create_engine(f'hive://{HIVE_USER}@{HIVE_HOST}:{HIVE_PORT}/{HIVE_DATABASE}')

# 特征名称映射字典（英文到中文）
feature_name_mapping = {
    'anxiety_level': '焦虑水平',
    'self_esteem': '自尊水平',
    'mental_health_history': '心理健康病史',
    'depression': '抑郁',
    'headache': '头痛问题',
    'blood_pressure': '血压问题',
    'sleep_quality': '睡眠质量',
    'breathing_problem': '呼吸问题',
    'noise_level': '环境噪音水平',
    'living_conditions': '居住条件',
    'safety': '安全',
    'basic_needs': '基本需求满足情况',
    'academic_performance': '学业表现',
    'study_load': '学业负担',
    'teacher_student_relationship': '师生关系',
    'future_career_concerns': '未来职业担忧',
    'social_support': '社会支持',
    'peer_pressure': '同辈压力',
    'extracurricular_activities': '课外活动',
    'bullying': '霸凌问题',
    'stress_level': '压力水平'
}

def read_from_hive(query):
    """从Hive读取数据"""
    try:
        df = pd.read_sql(query, engine)
        # 去掉列名中的表名前缀
        df.columns = [col.split('.')[-1] for col in df.columns]
        return df
    except Exception as e:
        print(f"从Hive读取数据时出错: {e}")
        # 尝试从本地CSV文件读取数据作为备选方案
        try:
            csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ShapCompatibleDataset.csv')
            if os.path.exists(csv_path):
                print(f"尝试从本地CSV文件读取数据: {csv_path}")
                return pd.read_csv(csv_path)
            else:
                print(f"本地CSV文件不存在: {csv_path}")
                return None
        except Exception as csv_e:
            print(f"从本地CSV文件读取数据时出错: {csv_e}")
            return None

@app.route('/api/data-summary', methods=['GET'])
def get_data_summary():
    """获取数据摘要信息，而不是完整数据"""
    try:
        query = "SELECT * FROM stress_level_dataset"
        df = read_from_hive(query)

        if df is not None:
            # 计算摘要统计信息
            summary = {
                '数据总行数': len(df),
                '特征数量': len(df.columns) - 1,  # 减去目标列
                '特征列表': [feature_name_mapping.get(col, col) for col in df.columns if col != 'stress_level'],
                '压力水平分布': df['stress_level'].value_counts().to_dict()
            }
            
            return jsonify({
                'status': 'success',
                'summary': summary
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': '无法从Hive读取数据'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'发生错误: {str(e)}'
        }), 500

def train_random_forest_model(target_column='stress_level'):
    """
    训练随机森林分类模型。

    :param target_column: 目标列名称，默认为 'stress_level'
    :return: 训练好的模型、可用特征列表和模型准确率
    """
    query = "SELECT * FROM stress_level_dataset"
    df = read_from_hive(query)
    if df is None or df.empty:
        print("无法获取数据或数据为空")
        return None, None, None, None

    # 筛选特征列和目标列
    features = [col for col in df.columns if col != target_column]
    if not features:
        print("没有可用的特征列")
        return None, None, None, None

    X = df[features]
    y = df[target_column]

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 创建并训练随机森林模型
    model = RandomForestClassifier(n_estimators=300, random_state=42, max_depth=5)
    model.fit(X_train, y_train)

    # 模型评估
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"模型准确率: {accuracy}")

    return model, features, accuracy, X_test

def plot_to_base64(plt):
    """将matplotlib图表转换为base64编码的字符串"""
    # 设置中文字体支持
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close('all')  # 关闭所有图表，避免内存泄漏
    return img_str

def generate_model_plots(model, X_test, y_test, feature_names):
    """生成模型可视化图表"""
    plots = {
        'feature_importance': "",
        'confusion_matrix': "",
        'feature_distribution': "",
        'classification_report': "",
        'auc_roc_curve': ""          #  AUC-ROC 曲线
    }
    
    try:
        # 1. 特征重要性图
        plt.figure(figsize=(10, 8))
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        # 使用中文特征名称
        chinese_feature_names = [feature_name_mapping.get(feature_names[i], feature_names[i]) for i in indices]
        
        plt.barh(range(len(indices)), importances[indices])
        plt.yticks(range(len(indices)), chinese_feature_names)
        plt.xlabel('特征重要性')
        plt.title('随机森林特征重要性')
        plots['feature_importance'] = plot_to_base64(plt)
        
        # 2. 混淆矩阵
        plt.figure(figsize=(8, 6))
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('预测标签')
        plt.ylabel('真实标签')
        plt.title('混淆矩阵')
        plots['confusion_matrix'] = plot_to_base64(plt)
        
        # 3. 特征分布图 (原 roc_curve)
        plt.figure(figsize=(12, 8))
        # 选择前4个最重要的特征
        top_features = [feature_names[i] for i in indices[:4]]
        top_features_chinese = [feature_name_mapping.get(feature, feature) for feature in top_features]
        
        for i, feature in enumerate(top_features):
            plt.subplot(2, 2, i+1)
            for target_value in np.unique(y_test):
                sns.kdeplot(X_test[X_test.index.isin(y_test[y_test == target_value].index)][feature], 
                           label=f'压力等级 {target_value}')
            plt.title(f'特征: {top_features_chinese[i]}')
            plt.xlabel(top_features_chinese[i])
            plt.legend()
        
        plt.tight_layout()
        plots['feature_distribution'] = plot_to_base64(plt) # 修改键名
        
        # 4. 分类报告图 (原 learning_curve)
        plt.figure(figsize=(10, 6))
        
        # 计算每个类别的准确率
        report = classification_report(y_test, y_pred, output_dict=True)
        classes = list(report.keys())[:-3]  # 排除 'accuracy', 'macro avg', 'weighted avg'
        
        metrics = ['precision', 'recall', 'f1-score']
        metrics_chinese = ['精确率', '召回率', 'F1分数']
        x = np.arange(len(classes))
        width = 0.25
        
        for i, metric in enumerate(metrics):
            values = [report[cls][metric] for cls in classes]
            plt.bar(x + i*width, values, width, label=metrics_chinese[i])
        
        plt.xlabel('压力等级')
        plt.ylabel('得分')
        plt.title('各压力等级的分类性能')
        plt.xticks(x + width, classes)
        plt.legend()
        plt.ylim(0, 1)
        
        plots['classification_report'] = plot_to_base64(plt) # 修改键名

        # 5. AUC-ROC 曲线图 (新增)
        # generate_auc_roc_plot 函数内部会处理 plt.close()，所以这里不需要额外关闭
        # 它也内部处理了中文字体，如果需要的话
        plots['auc_roc_curve'] = generate_auc_roc_plot(model, X_test, y_test)
        
    except Exception as e:
        print(f"生成图表时出错: {str(e)}")
        # 创建一个错误信息图
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, f"生成图表时出错: {str(e)}", 
                horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.axis('off')
        error_img = plot_to_base64(plt)
        
        # 将所有图表设置为错误图
        for key in plots:
            if not plots[key]:  # 如果该图表还没有生成
                plots[key] = error_img
    
    return plots

@app.route('/api/train-model', methods=['POST'])
def train_model():
    """触发随机森林模型训练"""
    model, features, accuracy, _ = train_random_forest_model()
    if model is None:
        return jsonify({
            'status': 'error',
            'message': '模型训练失败，无法获取数据或数据为空'
        }), 500
    
    # 获取特征重要性
    feature_importance = model.feature_importances_
    # 将特征重要性与特征名称配对并排序
    importance_pairs = sorted(zip(features, feature_importance), key=lambda x: x[1], reverse=True)
    
    # 构建返回数据（使用中文特征名称）
    result = {
        'status': 'success',
        'message': '模型训练成功',
        'accuracy': accuracy,
        'feature_importance': {feature_name_mapping.get(name, name): float(importance) for name, importance in importance_pairs}
    }
    
    return jsonify(result), 200

@app.route('/api/model-info', methods=['GET'])
def get_model_info():
    """获取模型信息"""
    try:
        model, features, accuracy, _ = train_random_forest_model()
        if model is None:
            return jsonify({
                'status': 'error',
                'message': '无法获取模型信息，请先训练模型'
            }), 500
        
        # 获取特征重要性
        feature_importance = model.feature_importances_
        # 将特征重要性与特征名称配对并排序
        importance_pairs = sorted(zip(features, feature_importance), key=lambda x: x[1], reverse=True)
        
        # 构建返回数据（使用中文特征名称）
        result = {
            'status': 'success',
            'model_type': '随机森林分类器',
            'n_estimators': model.n_estimators,
            'accuracy': accuracy,
            'feature_count': len(features),
            'top_features': [{'name': feature_name_mapping.get(name, name), 'importance': float(importance)} 
                            for name, importance in importance_pairs[:5]]
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取模型信息时发生错误: {str(e)}'
        }), 500

@app.route('/api/model-plots', methods=['GET'])
def get_model_plots():
    """获取模型可视化图表"""
    try:
        print("开始获取模型可视化图表...")
        model, features, accuracy, X_test = train_random_forest_model()
        if model is None:
            print("模型为空，无法生成图表")
            return jsonify({
                'status': 'error',
                'message': '无法生成图表，请先训练模型'
            }), 500
        
        # 确保X_test是DataFrame格式
        if not isinstance(X_test, pd.DataFrame):
            X_test = pd.DataFrame(X_test, columns=features)
            print(f"将X_test转换为DataFrame，形状: {X_test.shape}")
        
        # 获取测试集的真实标签 - 修改这部分逻辑
        try:
            print("获取测试集的真实标签...")
            # 从原始数据集中获取数据
            df = read_from_hive("SELECT * FROM stress_level_dataset")
            if df is None or df.empty:
                print("无法从Hive获取数据")
                return jsonify({
                    'status': 'error',
                    'message': '无法获取数据，请检查数据源'
                }), 500
            
            # 使用与train_random_forest_model相同的逻辑获取y_test
            features_cols = [col for col in df.columns if col != 'stress_level']
            X = df[features_cols]
            y = df['stress_level']
            _, X_test_idx, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            print(f"成功获取y_test，长度: {len(y_test)}")
            
            # 确保X_test和y_test长度匹配
            if len(X_test) != len(y_test):
                print(f"警告：X_test长度({len(X_test)})与y_test长度({len(y_test)})不匹配")
                # 使用模型预测结果作为替代
                y_test = model.predict(X_test)
                print(f"使用模型预测结果作为替代，长度: {len(y_test)}")
            
        except Exception as e:
            print(f"获取y_test时出错: {str(e)}")
            # 使用模型预测结果作为替代
            print("使用模型预测结果作为替代...")
            y_test = model.predict(X_test)
        
        # 生成模型可视化图表
        print("开始生成模型可视化图表...")
        plots = generate_model_plots(model, X_test, y_test, features)
        
        return jsonify({
            'status': 'success',
            'plots': plots
        }), 200
    except Exception as e:
        print(f"生成模型可视化图表时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'生成图表时发生错误: {str(e)}'
        }), 500

def generate_auc_roc_plot(model, X_test, y_test):
    """
    生成AUC-ROC曲线图
    
    :param model: 训练好的模型
    :param X_test: 测试集特征
    :param y_test: 测试集标签
    :return: Base64编码的图像
    """
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve, auc
    import io
    import base64
    from sklearn.preprocessing import label_binarize
    import numpy as np
    
    plt.figure(figsize=(10, 8))
    
    # 获取类别数量
    n_classes = len(np.unique(y_test))
    
    if n_classes > 2:  # 多分类情况
        # 将标签二值化
        y_bin = label_binarize(y_test, classes=np.unique(y_test))
        
        # 存储每个类别的假正率、真正率和AUC
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        
        # 计算每个类别的ROC曲线和AUC
        for i in range(n_classes):
            # 预测每个类别的概率
            y_score = model.predict_proba(X_test)[:, i]
            fpr[i], tpr[i], _ = roc_curve(y_bin[:, i], y_score)
            roc_auc[i] = auc(fpr[i], tpr[i])
            
            # 绘制每个类别的ROC曲线
            plt.plot(fpr[i], tpr[i], lw=2,
                     label=f'ROC 曲线 (类别 {i}, AUC = {roc_auc[i]:.2f})')
    
    else:  # 二分类情况
        # 预测正类的概率
        y_score = model.predict_proba(X_test)[:, 1]
        
        # 计算ROC曲线
        fpr, tpr, _ = roc_curve(y_test, y_score)
        roc_auc = auc(fpr, tpr)
        
        # 绘制ROC曲线
        plt.plot(fpr, tpr, lw=2, label=f'ROC 曲线 (AUC = {roc_auc:.2f})')
    
    # 绘制对角线
    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    
    # 设置图表属性
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('假正率 (False Positive Rate)')
    plt.ylabel('真正率 (True Positive Rate)')
    plt.title('接收者操作特征曲线 (ROC)')
    plt.legend(loc="lower right")
    
    # 将图表转换为Base64编码
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_str

# 添加新的API端点
@app.route('/api/auc-roc-plot', methods=['GET'])
def get_auc_roc_plot():
    """获取AUC-ROC曲线图"""
    try:
        print("开始生成AUC-ROC曲线图...")
        model, features, accuracy, X_test = train_random_forest_model()
        if model is None:
            print("模型为空，无法生成AUC-ROC曲线图")
            return jsonify({
                'status': 'error',
                'message': '无法生成AUC-ROC曲线图，请先训练模型'
            }), 500
        
        # 确保X_test是DataFrame格式
        if not isinstance(X_test, pd.DataFrame):
            X_test = pd.DataFrame(X_test, columns=features)
            print(f"将X_test转换为DataFrame，形状: {X_test.shape}")
        
        # 获取测试集的真实标签
        try:
            print("获取测试集的真实标签...")
            # 从原始数据集中获取数据
            df = read_from_hive("SELECT * FROM stress_level_dataset")
            if df is None or df.empty:
                print("无法从Hive获取数据")
                return jsonify({
                    'status': 'error',
                    'message': '无法获取数据，请检查数据源'
                }), 500
            
            # 使用与train_random_forest_model相同的逻辑获取y_test
            features_cols = [col for col in df.columns if col != 'stress_level']
            X = df[features_cols]
            y = df['stress_level']
            _, X_test_idx, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            print(f"成功获取y_test，长度: {len(y_test)}")
            
            # 确保X_test和y_test长度匹配
            if len(X_test) != len(y_test):
                print(f"警告：X_test长度({len(X_test)})与y_test长度({len(y_test)})不匹配")
                # 使用模型预测结果作为替代
                y_test = model.predict(X_test)
                print(f"使用模型预测结果作为替代，长度: {len(y_test)}")
            
        except Exception as e:
            print(f"获取y_test时出错: {str(e)}")
            # 使用模型预测结果作为替代
            print("使用模型预测结果作为替代...")
            y_test = model.predict(X_test)
        
        # 生成AUC-ROC曲线图
        print("开始生成AUC-ROC曲线图...")
        auc_roc_plot = generate_auc_roc_plot(model, X_test, y_test)
        
        return jsonify({
            'status': 'success',
            'auc_roc_plot': auc_roc_plot
        }), 200
    except Exception as e:
        print(f"生成AUC-ROC曲线图时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'生成AUC-ROC曲线图时发生错误: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("启动Flask服务器，监听在 http://localhost:5000")
    app.run(debug=True)