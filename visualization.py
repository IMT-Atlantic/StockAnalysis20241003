import matplotlib.pyplot as plt

def plot_results(dates, portfolio_value, prices, cash_history, profit_percentages, holding_amounts):
    """
    绘制交易结果图表
    :param dates: 日期列表
    :param portfolio_value: 投资组合价值列表
    :param prices: 股票价格列表
    :param cash_history: 现金金额列表
    :param profit_percentages: 盈利百分比列表
    :param holding_amounts: 持仓金额列表
    """
    plt.figure(figsize=(14, 15))

    plt.subplot(5, 1, 1)
    plt.plot(dates, portfolio_value, label='Portfolio Value')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.title('Portfolio Value Over Time')
    plt.legend()
    plt.grid(True)

    plt.subplot(5, 1, 2)
    plt.plot(dates, prices, label='Stock Price', color='orange')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.title('Stock Price Over Time')
    plt.legend()
    plt.grid(True)

    plt.subplot(5, 1, 3)
    plt.plot(dates, cash_history, label='Cash Amount', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Cash Amount')
    plt.title('Cash Amount Over Time')
    plt.legend()
    plt.grid(True)

    plt.subplot(5, 1, 4)
    plt.plot(dates, profit_percentages, label='Profit Percentage', color='green')
    plt.xlabel('Date')
    plt.ylabel('Profit Percentage (%)')
    plt.title('Profit Percentage Over Time')
    plt.legend()
    plt.grid(True)

    plt.subplot(5, 1, 5)
    plt.plot(dates, holding_amounts, label='Holding Amount', color='red')
    plt.xlabel('Date')
    plt.ylabel('Holding Amount')
    plt.title('Holding Amount Over Time')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()