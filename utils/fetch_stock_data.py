import yfinance as yf
import pandas as pd
import os
import sys

# 获取当前脚本（fetch_stock_data.py）的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取 `SigmaEdge` 的路径
sigmaedge_dir = os.path.dirname(current_dir)

# 将 `SigmaEdge` 添加到 Python 模块搜索路径
sys.path.append(sigmaedge_dir)

# 现在可以正确导入
from utils.fetch_sp500 import get_sp500_tickers

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

def download_sp500_data(start='2010-01-01', end='2025-01-01'):
    """下载 S&P 500 成分股的历史价格数据"""
    tickers = get_sp500_tickers()

    # 下载数据
    sp500_data = yf.download(tickers, start=start, end=end, auto_adjust=False)

    # 选择调整后收盘价
    if 'Adj Close' in sp500_data.columns:
        sp500_data = sp500_data['Adj Close']
    else:
        print("⚠️ Warning: 'Adj Close' column not found! Check YFinance response.")
        return

    # 保存数据
    stock_prices_file = os.path.join(DATA_RAW_DIR, "sp500_stock_prices.csv")
    sp500_data.to_csv(stock_prices_file)
    print("✅ S&P 500 股票数据下载完成")


if __name__ == "__main__":
    download_sp500_data()
