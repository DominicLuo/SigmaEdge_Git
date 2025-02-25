import requests
import pandas as pd
import os
import sys
import yfinance as yf
from bs4 import BeautifulSoup
from io import StringIO

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

def clean_ticker_symbols(tickers):
    """修正 Yahoo Finance 识别的 S&P 500 代码格式"""
    return [ticker.replace(".", "-") if "." in ticker else ticker for ticker in tickers]


def get_sp500_tickers():
    """从 Wikipedia 抓取最新 S&P 500 成分股列表"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 解析表格
    table = soup.find("table", {"id": "constituents"})
    df = pd.read_html(StringIO(str(table)))[0]

    # 提取股票代码并修正格式
    df["Symbol"] = clean_ticker_symbols(df["Symbol"].tolist())
    print(f"✅ 成功获取 {len(df)} 只 S&P 500 股票")

    # 保存 CSV
    tickers_file = os.path.join(DATA_RAW_DIR, "sp500_tickers.csv")
    df.to_csv(tickers_file, index=False)
    return df["Symbol"].tolist()


if __name__ == "__main__":
    get_sp500_tickers()
