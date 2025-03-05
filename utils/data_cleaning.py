import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler


def clean_data(df):
    """处理缺失值，填充数据"""
    df.fillna(method='ffill', inplace=True)  # 用前值填充缺失值
    df.fillna(method='bfill', inplace=True)  # 用后值填充
    return df


def remove_outliers(df, method="iqr"):
    """去除极值：支持 IQR 或 Z-Score"""
    if method == "iqr":
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1
        df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
    elif method == "zscore":
        df = df[(np.abs(df - df.mean()) / df.std()) < 3]
    return df


def normalize_data(df):
    """数据归一化（使用 RobustScaler 适应金融数据）"""
    scaler = RobustScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
    return df_scaled


def process_stock_data():
    """读取价格数据，进行数据清理"""
    prices = pd.read_csv("data/raw/sp500_stock_prices.csv", index_col=0, parse_dates=True)

    # 处理缺失值
    prices = clean_data(prices)

    # 去除异常值
    prices = remove_outliers(prices, method="iqr")

    # 归一化数据（有利于机器学习）
    prices_normalized = normalize_data(prices)

    # 保存数据
    prices.to_csv("data/processed/clean_stock_prices.csv")
    prices_normalized.to_csv("data/processed/normalized_stock_prices.csv")

    print("✅ 数据清理完成，已保存处理后的数据！")


if __name__ == "__main__":
    process_stock_data()
