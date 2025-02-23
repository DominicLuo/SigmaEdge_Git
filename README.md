# SigmaEdge
SigmaEdge is a systematic quantitative trading strategy designed for US stock markets. It leverages machine learning, factor-based stock selection, Bayesian asset allocation, and hedging strategies to optimize portfolio returns.

Key Features ✅ Stock Selection: Uses XGBoost to select stocks based on momentum, volatility, and liquidity factors. ✅ Portfolio Optimization: Bayesian optimization & Mean-Variance approach for risk-adjusted returns. ✅ Market Timing: Hidden Markov Model (HMM) & LSTM for market state prediction. ✅ Risk Hedging: Heston model + VIX options for volatility hedging. ✅ Execution Optimization: VWAP & Almgren-Chriss model for efficient trade execution. ✅ Backtesting: Uses Backtrader to evaluate performance metrics (Sharpe ratio, drawdowns, etc.).

⚙️ Tech Stack Python 3.9+ Pandas, NumPy, Scikit-learn (Data Processing & ML) XGBoost, LSTM, HMM (Stock Selection & Market Timing) CVXPY, PyPortfolioOpt (Portfolio Optimization) Backtrader (Backtesting) yFinance, Alpha Vantage (Data Source)

📦 SigmaEdge

┣ 📂 data/ # Raw & processed stock data

┣ 📂 models/ # Machine learning models (XGBoost, LSTM, HMM)

┣ 📂 strategies/ # Portfolio optimization & trading execution

┣ 📂 backtesting/ # Backtrader scripts for performance evaluation

┣ 📜 README.md # Project documentation

┣ 📜 requirements.txt # Python dependencies

┗ 📜 main.py # Run the strategy

Results

🔄 Future Improvements ✅ Add more factors (fundamental & alternative data) ✅ Improve market timing using Transformer-based models ✅ Optimize execution with Reinforcement Learning (RL)

📬 Contact 👤 Yucheng Luo 📧 Email: dominic.yucheng@gmail.com 🌍 GitHub: github.com/DominicLuo
