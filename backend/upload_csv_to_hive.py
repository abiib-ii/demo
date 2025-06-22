import pandas as pd
from sqlalchemy import create_engine, text
import os
import sys
import tempfile

def upload_csv_to_hive(csv_file_path, table_name, hive_host='localhost', hive_port=10005,
                      hive_user='24130', hive_database='default'):
    """
    将本地CSV文件上传到Hive表中
    
    参数:
        csv_file_path (str): CSV文件的路径
        table_name (str): 要上传到的Hive表名
        hive_host (str): Hive服务器主机名
        hive_port (int): Hive服务器端口
        hive_user (str): Hive用户名
        hive_database (str): Hive数据库名
    
    返回:
        bool: 上传是否成功
    """
    try:
        # 检查CSV文件是否存在
        if not os.path.exists(csv_file_path):
            print(f"错误: 文件 '{csv_file_path}' 不存在")
            return False
        
        # 读取CSV文件
        print(f"正在读取CSV文件: {csv_file_path}")
        df = pd.read_csv(csv_file_path)
        
        # 创建Hive连接
        print(f"正在连接到Hive: {hive_host}:{hive_port}/{hive_database}")
        engine = create_engine(f'hive://{hive_user}@{hive_host}:{hive_port}/{hive_database}')
        conn = engine.connect()
        
        # 方法1：使用CREATE TABLE语句创建表结构
        print(f"正在创建或替换表: {table_name}")
        
        # 获取列名和数据类型
        columns = []
        for col_name, dtype in df.dtypes.items():
            # 将pandas数据类型映射到Hive数据类型
            if 'int' in str(dtype):
                hive_type = 'INT'
            elif 'float' in str(dtype):
                hive_type = 'DOUBLE'
            else:
                hive_type = 'STRING'
            columns.append(f"`{col_name}` {hive_type}")
        
        # 创建表
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            {', '.join(columns)}
        )
        ROW FORMAT DELIMITED
        FIELDS TERMINATED BY ','
        STORED AS TEXTFILE
        """
        
        # 如果表已存在，先删除 - 使用text()包装SQL字符串
        conn.execute(text(f"DROP TABLE IF EXISTS `{table_name}`"))
        conn.execute(text(create_table_sql))
        
        # 方法2：将数据保存为临时CSV文件，然后使用LOAD DATA语句加载
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        temp_file_path = temp_file.name
        temp_file.close()
        
        # 保存数据到临时CSV文件（不包含标题行）
        df.to_csv(temp_file_path, index=False, header=False)
        
        # 构建LOAD DATA语句的本地文件路径
        # 在Windows上，需要将路径转换为适合Hive的格式
        hive_path = temp_file_path.replace('\\', '/')
        
        # 加载数据
        print(f"正在将数据加载到表: {table_name}")
        load_data_sql = f"""
        LOAD DATA LOCAL INPATH '{hive_path}'
        INTO TABLE `{table_name}`
        """
        
        conn.execute(text(load_data_sql))
        
        # 清理临时文件
        os.unlink(temp_file_path)
        
        # 验证数据是否已加载
        result = conn.execute(text(f"SELECT COUNT(*) FROM `{table_name}`"))
        count = result.fetchone()[0]
        
        print(f"成功上传 {count} 行数据到 {table_name}")
        return True
        
    except Exception as e:
        print(f"上传过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # 设置文件路径和表名
    csv_file_path = r'C:\Users\24130\Desktop\stress-prediction-frontend\StressLevelDataset.csv'
    table_name = 'stress_level_dataset'
    
    # 调用上传函数
    success = upload_csv_to_hive(csv_file_path, table_name)
    
    # 根据上传结果设置退出代码
    sys.exit(0 if success else 1)