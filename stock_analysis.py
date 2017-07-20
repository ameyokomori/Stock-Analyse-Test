"""
    
    __author__ = Weiye Zhao
    student number = 44612975
    __email__ = zhaoweiye1993@gmail.com
"""

import stocks


class LoadCSV(stocks.Loader):
    """Abstract class defining basic process of loading trading data."""

    def __init__(self, filename, load_stocks):

        if ".csv" not in filename:
            raise RuntimeError("Contain a none-csv file")

        super().__init__(filename, load_stocks)

    def _process(self, file):
        """Load and parse the stock market data from 'file'."""

        for line in file:
            data = line.strip("\n").split(",")
            if len(data) != 7:
                raise ValueError("This is not a stock csv file")

            try:
                trading_data = stocks.TradingData(data[1], float(data[2]), float(data[3]),
                                                  float(data[4]), float(data[5]), int(data[6]))

                stock = self._stocks.get_stock(data[0])

                stock.add_day_data(trading_data)

            except ValueError:
                print("Data {0} in csv is wrong.".format(data[0]))


class LoadTriplet(stocks.Loader):
    """Abstract class defining basic process of loading trading data."""

    def __init__(self, filename, load_stocks):

        if ".trp" not in filename:
            raise RuntimeError("Contain a none-trp file")

        self._flag = 0
        self._trading_data = stocks.TradingData("", -1, -1, -1, -1, -1)
        super().__init__(filename, load_stocks)

    def _process(self, file):
        """Load and parse the stock market data from 'file'."""

        for line in file:
            data = line.strip("\n").split(":")
            if len(data) != 3:
                raise ValueError("This is not a stock triplet file")

            stock = self._stocks.get_stock(data[0])

            try:
                if self._flag < 6:
                    if data[1] == "DA":
                        self._trading_data.set_date(data[2])
                        self._flag += 1
                    elif data[1] == "OP":
                        self._trading_data.set_open(float(data[2]))
                        self._flag += 1
                    elif data[1] == "HI":
                        self._trading_data.set_high(float(data[2]))
                        self._flag += 1
                    elif data[1] == "LO":
                        self._trading_data.set_low(float(data[2]))
                        self._flag += 1
                    elif data[1] == "CL":
                        self._trading_data.set_close(float(data[2]))
                        self._flag += 1
                    elif data[1] == "VO":
                        self._trading_data.set_volume(int(data[2]))
                        self._flag += 1

            except ValueError:
                print("Data {0} of {1} in trp is wrong.".format(data[1], data[0]))
                self.reset()

            if self._flag == 6:
                stock.add_day_data(self._trading_data)
                self.reset()

    def reset(self):
        """Reset the analysis process in order to perform a new analysis."""
        self._flag = 0
        self._trading_data = stocks.TradingData("", -1, -1, -1, -1, -1)


class HighLow(stocks.Analyser):
    """Determine the average trading volume for a single stock."""

    def __init__(self):

        self._high_price = 0
        self._low_price = 0
        self._highest_price = 0
        self._lowest_price = -1

    def process(self, stock):
        """Abstract method representing collecting and processing DayData.

        Parameters:
            stock (TradingData): Trading data for one stock on one day.
        """
        self._high_price = stock.get_high()
        self._low_price = stock.get_low()

        if self._high_price > self._highest_price:
            self._highest_price = self._high_price
        if self._low_price < self._lowest_price or self._lowest_price == -1:
            self._lowest_price = self._low_price

    def reset(self):
        """Reset the analysis process in order to perform a new analysis."""
        self._high_price = 0
        self._low_price = 0
        self._highest_price = 0
        self._lowest_price = -1

    def result(self):
        """Abstract method representing obtaining the result of the analysis.

        Return:
            None: Subclasses will return result of the analysis.
        """
        return self._highest_price, self._lowest_price


class MovingAverage(stocks.Analyser):
    """Determine the average trading volume for a single stock."""

    def __init__(self, num_days):
        self._num_days = num_days
        self._closing_price = []
        self._sum = 0

    def process(self, stock):
        """Abstract method representing collecting and processing DayData.

        Parameters:
            stock (TradingData): Trading data for one stock on one day.
        """

        self._closing_price.append(stock.get_close())

    def reset(self):
        """Reset the analysis process in order to perform a new analysis."""

        self._closing_price = []
        self._sum = 0

    def result(self):
        """Abstract method representing obtaining the result of the analysis.

        Return:
            None: Subclasses will return result of the analysis.
        """
        prices = self._closing_price[-self._num_days:]

        for i in prices:
            self._sum += i

        return self._sum / self._num_days


class GapUp(stocks.Analyser):
    """Determine the average trading volume for a single stock."""

    def __init__(self, delta):
        self._delta = delta
        self._date = ''
        self._flag = 0
        self._closing_price = 0
        self._opening_price = 0
        self._stock = stocks.TradingData("", 0, 0, 0, 0, 0)

    def process(self, stock):
        """Abstract method representing collecting and processing DayData.

        Parameters:
            stock (TradingData): Trading data for one stock on one day.
        """
        if self._flag == 0:
            self._closing_price = stock.get_close()
            self._flag = 1
        else:
            self._opening_price = stock.get_open()
            if abs(self._opening_price - self._closing_price) >= self._delta:
                self._date = stock.get_date()
                self._stock = stock
            self._closing_price = stock.get_close()

    def reset(self):
        """Reset the analysis process in order to perform a new analysis."""
        
        self._date = ''
        self._flag = 0
        self._closing_price = 0
        self._opening_price = 0

    def result(self):
        """Abstract method representing obtaining the result of the analysis.

        Return:
            None: Subclasses will return result of the analysis.
        """
        if self._date != '':
            return self._stock
        else:
            return None


# main
def main():
    all_stocks = stocks.StockCollection()

    LoadCSV("march1.csv", all_stocks)
    LoadCSV("march2.csv", all_stocks)
    LoadCSV("march3.csv", all_stocks)
    LoadCSV("march4.csv", all_stocks)
    LoadCSV("march5.csv", all_stocks)
    LoadTriplet("feb1.trp", all_stocks)
    LoadTriplet("feb2.trp", all_stocks)
    LoadTriplet("feb3.trp", all_stocks)
    LoadTriplet("feb4.trp", all_stocks)

    stock = all_stocks.get_stock("ADV")

    volume = stocks.AverageVolume()
    stock.analyse(volume)
    print("Average Volume of ADV is", volume.result())

    high_low = HighLow()
    stock.analyse(high_low)
    print("Highest & Lowest trading price of ADV is", high_low.result())

    moving_average = MovingAverage(10)
    stock.analyse(moving_average)
    print("Moving average of ADV over last 10 days is {0:.2f}"
          .format(moving_average.result()))

    gap_up = GapUp(0.011)
    stock = all_stocks.get_stock("YOW")
    stock.analyse(gap_up)
    print("Last gap up date of YOW is", gap_up.result().get_date())


if __name__ == "__main__":
    main()
