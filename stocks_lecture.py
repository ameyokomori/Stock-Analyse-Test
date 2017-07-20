import stocks

some_stocks = stocks.StockCollection()

stock = some_stocks.get_stock("1AD")
day_data = stocks.TradingData("20170227", 0.225, 0.225, 0.225, 0.225, 19478)
stock.add_day_data(day_data)
day_data = stocks.TradingData("20170306", 0.22, 0.225, 0.22, 0.225, 24259)
stock.add_day_data(day_data)

stock = some_stocks.get_stock("ABU")
day_data = stocks.TradingData("20170227", 0.11, 0.115, 0.11, 0.115, 262306)
stock.add_day_data(day_data)
day_data = stocks.TradingData("20170306", 0.115, 0.115, 0.115, 0.115, 86782)
stock.add_day_data(day_data)
day_data = stocks.TradingData("20170313", 0.105, 0.105, 0.105, 0.105, 75025)
stock.add_day_data(day_data)

stock = some_stocks.get_stock("AGL")
day_data = stocks.TradingData("20170227", 23.6, 23.92, 23.6, 23.85, 1433574)
stock.add_day_data(day_data)
day_data = stocks.TradingData("20170306", 24.7, 24.88, 24.4, 24.86, 1156183)
stock.add_day_data(day_data)
day_data = stocks.TradingData("20170313", 25.48, 25.53, 25.32, 25.45, 1892685)
stock.add_day_data(day_data)

some_stocks.list_stocks()

stock = some_stocks.get_stock("AGL")
volume = stocks.AverageVolume()
stock.analyse(volume)
print("Average Volume of ADV is", volume.result())

