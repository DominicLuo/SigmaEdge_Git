import requests
import pandas as pd
import os
import yfinance as yf
from bs4 import BeautifulSoup
from io import StringIO
# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

def clean_ticker_symbols(tickers):
    """修正 Yahoo Finance 识别的 S&P 500 代码格式"""
    cleaned_tickers = [ticker.replace(".", "-") for ticker in tickers]
    return cleaned_tickers

def get_sp500_tickers():
    """从 Wikipedia 获取 S&P 500 成分股列表"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 解析表格
    table = soup.find("table", {"id": "constituents"})
    if table is None:
        print("❌ Error: 没有找到 S&P 500 成分股表格，可能 Wikipedia 页面结构变了")
        return []

    # 修正 FutureWarning，使用 StringIO 包装 HTML
    df = pd.read_html(StringIO(str(table)))[0]

    # 提取股票代码
    tickers = df["Symbol"].tolist()
    tickers_file = os.path.join(DATA_RAW_DIR, "sp500_tickers.csv")
    df.to_csv(tickers_file, index=False)

    print(f"✅ 成功获取 {len(tickers)} 只 S&P 500 股票")
    return tickers


def download_sp500_data(start="2010-01-01", end="2025-01-01"):
    """下载 S&P 500 成分股的历史价格数据"""
    tickers = get_sp500_tickers()
    if not tickers:
        print("❌ Error: 未能获取 S&P 500 股票列表")
        return

    print(f"📊 正在下载 {len(tickers)} 只 S&P 500 股票数据...")

    # **获取数据**
    sp500_data = yf.download(tickers, start=start, end=end, group_by="ticker", auto_adjust=False)

    # **检查数据是否为空**
    if sp500_data.empty:
        print("❌ Error: 下载的 S&P 500 数据为空！可能是 API 限制或股票代码错误")
        return

    # ✅ 解决 MultiIndex 问题
    if isinstance(sp500_data.columns, pd.MultiIndex):
        sp500_data = sp500_data.xs("Adj Close", axis=1, level=1)  # 提取 "Adj Close"

    # **打印数据结构**
    print("📊 S&P 500 数据列名:", sp500_data.columns)

    # **检查 `Adj Close` 是否存在**
    if isinstance(sp500_data.columns, pd.MultiIndex):
        try:
            sp500_data = sp500_data[("Adj Close", tickers)]
        except KeyError:
            print("⚠️ Warning: 'Adj Close' not found in MultiIndex columns. Saving full dataset.")
            sp500_data.to_csv(os.path.join(DATA_RAW_DIR, "sp500_data_prices .csv"))
            return
    elif "Adj Close" in sp500_data.columns:
        sp500_data = sp500_data["Adj Close"]
    else:
        print("⚠️ Warning: 'Adj Close' column not found! Saving full dataset for debugging.")
        sp500_data.to_csv(os.path.join(DATA_RAW_DIR, "sp500_data_prices.csv"))
        return

    # **保存数据**
    os.makedirs(DATA_RAW_DIR, exist_ok=True)
    sp500_data.to_csv(os.path.join(DATA_RAW_DIR, "sp500_stock_prices.csv"))
    print("✅ S&P 500 股票数据下载完成")


def download_vix_data(start="2010-01-01", end="2025-01-01"):
    """下载 VIX（恐慌指数）数据"""
    vix_data = yf.download("^VIX", start=start, end=end, auto_adjust=False)

    # **检查数据是否为空**
    if vix_data.empty:
        print("❌ Error: No VIX data downloaded! Check ticker symbol or API limit.")
        return

    # **打印返回的数据格式**
    print("📊 VIX 数据列名:", vix_data.columns)

    # **处理 MultiIndex**
    if isinstance(vix_data.columns, pd.MultiIndex):
        try:
            vix_data = vix_data[("Adj Close", "^VIX")]
        except KeyError:
            print("⚠️ Warning: 'Adj Close' not found in MultiIndex columns. Saving full dataset.")
            vix_data.to_csv("data/raw/vix_data_full.csv")
            return
    elif "Adj Close" in vix_data.columns:
        vix_data = vix_data["Adj Close"]
    else:
        print("⚠️ Warning: 'Adj Close' column not found! Saving full dataset for debugging.")
        vix_data.to_csv("data/raw/vix_data_full.csv")
        return

    # 确保存储目录存在
    os.makedirs(DATA_RAW_DIR, exist_ok=True)

    # **保存数据**
    vix_data.to_csv(os.path.join(DATA_RAW_DIR, "vix_data.csv"))
    print("✅ VIX 数据下载完成")



if __name__ == "__main__":
    get_sp500_tickers()
    download_sp500_data()
    download_vix_data()
