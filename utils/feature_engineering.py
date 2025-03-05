import pandas as pd
import numpy as np

def calculate_momentum(df, lookback=21):
    """计算动量因子（Momentum）"""
    return df.pct_change(lookback)

def calculate_volatility(df, lookback=21):
    """计算波动率因子（Volatility）"""
    return df.pct_change().rolling(lookback).std()

def calculate_liquidity(df, volume_df, lookback=21):
    """计算流动性因子（使用 Amihud Illiquidity Ratio）"""
    illiquidity = df.pct_change().abs() / volume_df
    return illiquidity.rolling(lookback).mean()
