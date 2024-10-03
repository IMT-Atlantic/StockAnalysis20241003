from data_loader import load_data_from_excel
from parameter_optimization import find_best_strategy
from modern_trading_strategy import TradingStrategy
from visualization import plot_results

# 调用主程序
data = load_data_from_excel('E:\\StockDataNADSA\\SZSE\\000998.xlsx')

# 确保数据集足够大
if len(data) < 200:
    raise ValueError("数据集不足200个交易日，请提供更多数据.")

# 参数网格
# 初始资金-建仓资金-补仓资金-回撤止盈线-清仓止盈线-回撤卖出比例-下跌补仓比例
param_grid = {
    'initial_cash': [200000],  # 初始资金保持不变
    'buy_amount_initial': [5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000],  # 5,000到20,000，每次增加1,000
    'buy_amount_additional': [10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000],  # 10,000到30,000，每次增加1,000
    'sell_threshold': [round(1.2 + i*0.01, 2) for i in range(9)],  # 1.2到2.0，每次增加0.1变为0.01
    'stop_loss_threshold': [round(0.5 + i*0.05, 2) for i in range(11)],  # 0.5到1.0，每次增加0.1变为0.05
    'sell_percentage': [0.01 * i for i in range(1, 51)],  # 0.1到0.5，每次增加0.1变为0.01
    'rebuy_percentage': [round(0.6 + i*0.01, 2) for i in range(41)]  # 0.6到1.0，每次增加0.1变为0.01
}

# 找到最佳参数组合
best_params, best_result = find_best_strategy(data, param_grid)

print("最佳参数组合：", best_params)

# 使用最近200个交易日的数据进行可视化
recent_data = data[-200:].reset_index(drop=True)

strategy = TradingStrategy(**best_params)
transactions, dates, portfolio_values, prices, cash_history, profit_percentages, holding_amounts = strategy.execute(recent_data)

plot_results(dates, portfolio_values, prices, cash_history, profit_percentages, holding_amounts)