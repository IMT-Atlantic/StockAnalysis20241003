# parameter_optimization.py
import numpy as np
from itertools import product
from modern_trading_strategy import TradingStrategy

def find_best_strategy(data, param_grid):
    """
    穷举参数网格以找到最佳交易策略参数组合
    :param data: 包含股票收盘价和日期的DataFrame
    :param param_grid: 参数网格字典
    :return: 最佳参数组合和相应的结果
    """
    best_profit = -np.inf
    best_params = None
    best_result = None
    truncated_data = data[:-200]  # 去掉最近200个交易日的数据

    for params in product(*param_grid.values()):
        param_dict = dict(zip(param_grid.keys(), params))
        strategy = TradingStrategy(**param_dict)
        transactions, dates, portfolio_value, prices, cash_history, profit_percentages, holding_amounts = strategy.execute(truncated_data)

        if portfolio_value[-1] > best_profit:
            best_profit = portfolio_value[-1]
            best_params = param_dict
            best_result = (transactions, dates, portfolio_value, prices, cash_history, profit_percentages, holding_amounts)

    return best_params, best_result