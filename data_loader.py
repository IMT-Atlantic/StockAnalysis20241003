import pandas as pd

def load_data_from_excel(file_path, sheet_name='Sheet1'):
    """
    从Excel文件中加载数据，并按日期排序.
    :param file_path: Excel文件路径
    :param sheet_name: 工作表名称
    :return: 排序后的DataFrame
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df['日期'] = pd.to_datetime(df['日期'])
    df = df.sort_values(by='日期').reset_index(drop=True)
    return df