# modern_trading_strategy.py
class TradingStrategy:
    def __init__(self, initial_cash=100000, buy_amount_initial=10000, buy_amount_additional=20000, sell_threshold=1.3, stop_loss_threshold=0.8, sell_percentage=0.2, rebuy_percentage=0.5):
        self.initial_cash = initial_cash
        self.buy_amount_initial = buy_amount_initial
        self.buy_amount_additional = buy_amount_additional
        self.sell_threshold = sell_threshold
        self.stop_loss_threshold = stop_loss_threshold
        self.sell_percentage = sell_percentage
        self.rebuy_percentage = rebuy_percentage

    def buy_stock(self, current_price, cash, num_shares, holding):
        """
        执行买入操作
        :param current_price: 当前股价
        :param cash: 现金余额
        :param num_shares: 购买的股票数量
        :param holding: 持有的股票数量
        :return: 更新后的现金余额和持股数量
        """
        if num_shares > 0:
            holding += num_shares
            cash -= num_shares * current_price
        return cash, holding

    def execute(self, data):
        """
        执行交易策略
        :param data: 包含股票收盘价和日期的DataFrame
        :return: 所有交易记录，日期，投资组合价值，股价，现金余额，盈利百分比，持仓金额
        """
        if data.empty:
            raise ValueError("输入数据为空，请检查数据源。")

        cash = self.initial_cash
        total_value = self.initial_cash
        holding = 0
        buy_price = []
        transactions = []
        stock_unit = 100  # 股票交易单位(每手)
        initial_build_price = None  # 初始建仓价格

        dates = []
        portfolio_values = []
        prices = []
        cash_history = []
        profit_percentages = []
        holding_amounts = []  # 新增持仓金额列表

        for i in range(len(data)):
            current_price = data['收盘'][i]

            if i == 0:
                num_shares = (self.buy_amount_initial // (current_price * stock_unit)) * stock_unit
                cash, holding = self.buy_stock(current_price, cash, num_shares, holding)
                initial_build_price = current_price
                buy_price.append(current_price)
                transactions.append(('buy', data['日期'][i], current_price, holding, cash, total_value))

            elif current_price < initial_build_price * 0.9 and cash >= self.buy_amount_initial:
                num_shares = (self.buy_amount_initial // (current_price * stock_unit)) * stock_unit
                cash, holding = self.buy_stock(current_price, cash, num_shares, holding)
                buy_price.append(current_price)
                transactions.append(('buy', data['日期'][i], current_price, holding, cash, total_value))
                initial_build_price = sum(buy_price) / len(buy_price)

            elif current_price < initial_build_price * self.rebuy_percentage and cash >= self.buy_amount_additional:
                num_shares = (self.buy_amount_additional // (current_price * stock_unit)) * stock_unit
                cash, holding = self.buy_stock(current_price, cash, num_shares, holding)
                buy_price.append(current_price)
                transactions.append(('buy', data['日期'][i], current_price, holding, cash, total_value))
                initial_build_price = sum(buy_price) / len(buy_price)

            elif current_price > initial_build_price * self.sell_threshold and holding > 0:
                num_shares = (holding * self.sell_percentage // stock_unit) * stock_unit
                if num_shares > 0:
                    holding -= num_shares
                    cash += num_shares * current_price
                    transactions.append(('sell', data['日期'][i], current_price, holding, cash, total_value))

            current_value = holding * current_price + cash
            if holding > 0 and current_value < total_value * self.stop_loss_threshold:
                cash += holding * current_price
                transactions.append(('sell-all', data['日期'][i], current_price, holding, cash, total_value))
                holding = 0

            total_value = holding * current_price + cash

            dates.append(data['日期'][i])
            portfolio_values.append(total_value)
            prices.append(current_price)
            cash_history.append(cash)
            profit_percentages.append((total_value - self.initial_cash) / self.initial_cash * 100)
            holding_amounts.append(holding * current_price)

            if i > 20 and (max(data['收盘'][i-20:i+1]) - min(data['收盘'][i-20:i+1])) / min(data['收盘'][i-20:i+1]) < 0.1 and cash >= self.buy_amount_initial:
                num_shares = (self.buy_amount_initial // (current_price * stock_unit)) * stock_unit
                cash, holding = self.buy_stock(current_price, cash, num_shares, holding)
                buy_price.append(current_price)
                transactions.append(('buy', data['日期'][i], current_price, holding, cash, total_value))
                initial_build_price = sum(buy_price) / len(buy_price)

        return transactions, dates, portfolio_values, prices, cash_history, profit_percentages, holding_amounts