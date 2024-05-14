"""
    The MIT License (MIT)

    Copyright (c) 2023 pkjmesra

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""

import configparser
import glob
import os
import sys

from PKDevTools.classes import Archiver
from PKDevTools.classes.ColorText import colorText
from PKDevTools.classes.log import default_logger
from PKDevTools.classes.Singleton import SingletonType, SingletonMixin
from PKDevTools.classes.OutputControls import OutputControls
parser = configparser.ConfigParser(strict=False)

# Default attributes for Downloading Cache from Git repo
default_period = "280d"
default_duration = "1d"
default_timeout = 2


# This Class manages read/write of user configuration
class tools(SingletonMixin, metaclass=SingletonType):
    def __init__(self):
        super(tools, self).__init__()
        self.consolidationPercentage = 10
        self.volumeRatio = 2.5
        self.minLTP = 20.0
        self.maxLTP = 50000
        self.period = "280d"
        self.duration = "1d"
        self.shuffleEnabled = True
        self.cacheEnabled = True
        self.stageTwo = True
        self.useEMA = False
        self.showunknowntrends = True
        self.enablePortfolioCalculations = False
        self.logsEnabled = False
        self.generalTimeout = 2
        self.defaultIndex = 12
        self.longTimeout = 4
        self.maxNetworkRetryCount = 10
        self.backtestPeriod = 120
        self.maxBacktestWindow = 30
        self.minVolume = 10000
        self.morninganalysiscandlenumber = 25 # 9:40am IST, since market opens at 9:15am IST
        self.morninganalysiscandleduration = '1m'
        self.logger = None
        self.showPastStrategyData = False
        self.atrTrailingStopSensitivity = 1
        self.atrTrailingStopPeriod = 21
        self.atrTrailingStopEMAPeriod = 9
        # This determines how many days apart the backtest calculations are run.
        # For example, for weekly backtest calculations, set this to 5 (5 days = 1 week)
        # For fortnightly, set this to 10 and so on (10 trading sessions = 2 weeks)
        self.backtestPeriodFactor = 1
        self.maxDashboardWidgetsPerRow = 3
        self.maxNumResultRowsInMonitor = 2
        self.calculatersiintraday = False
        self.defaultMonitorOptions = "X:12:9:2.5,|X:0:5:0:40:i 1m,X:12:27,X:12:28,X:12:23,X:12:7:3:.01:1,|{1}X:0:29:,X:12:6:3,X:12:6:8,X:12:6:7:1,X:12:6:9,X:12:6:10:1,X:12:7:3:.02:1,X:12:7:6:1,X:12:17,X:12:2,X:12:24,X:12:12:i 5m,X:12:13:i 1m"
        self.minimumChangePercentage = 0
        self.daysToLookback = 22 * self.backtestPeriodFactor  # 1 month
        self.periods = [1,2,3,4,5,10,15,22,30]
        if self.maxBacktestWindow > self.periods[-1]:
            self.periods.extend(self.maxBacktestWindow)

    @property
    def periodsRange(self):
        self._periodsRange = []
        if self.maxBacktestWindow > self.periods[-1]:
            self.periods.extend(self.maxBacktestWindow)
        for prd in self.periods:
            self._periodsRange.append(prd*self.backtestPeriodFactor)
        return self._periodsRange

    @property
    def effectiveDaysToLookback(self):
        return self.daysToLookback* self.backtestPeriodFactor
    
    @property
    def default_logger(self):
        return self.logger if self.logger is not None else default_logger()

    @default_logger.setter
    def default_logger(self, logger):
        self.logger = logger

    def deleteFileWithPattern(self, pattern=None, excludeFile=None, rootDir=None, recursive=False):
        if pattern is None:
            pattern = (
                f"{'intraday_' if self.isIntradayConfig() else ''}stock_data_*.pkl"
            )
        if rootDir is None:
            rootDir = [Archiver.get_user_outputs_dir(),Archiver.get_user_outputs_dir().replace("results","actions-data-download")]
        else:
            rootDir = [rootDir]
        for dir in rootDir:
            for f in glob.glob(pattern, root_dir=dir, recursive=recursive):
                if excludeFile is not None:
                    if not f.endswith(excludeFile):
                        try:
                            os.remove(f if os.sep in f else os.path.join(dir,f))
                        except Exception as e:
                            self.default_logger.debug(e, exc_info=True)
                            pass
                else:
                    try:
                        os.remove(f if os.sep in f else os.path.join(dir,f))
                    except Exception as e:
                        self.default_logger.debug(e, exc_info=True)
                        pass

    # Handle user input and save config

    def setConfig(self, parser, default=False, showFileCreatedText=True):
        if default:
            try:
                parser.remove_section("config")
                parser.remove_section("filters")
            except Exception as e:  # pragma: no cover
                self.default_logger.debug(e, exc_info=True)
                pass
            parser.add_section("config")
            parser.add_section("filters")
            parser.set("config", "atrtrailingstopemaperiod", str(self.atrTrailingStopEMAPeriod))
            parser.set("config", "atrtrailingstopperiod", str(self.atrTrailingStopPeriod))
            parser.set("config", "atrtrailingstopsensitivity", str(self.atrTrailingStopSensitivity))
            parser.set("config", "backtestPeriod", str(self.backtestPeriod))
            parser.set("config", "backtestPeriodFactor", str(self.backtestPeriodFactor))
            parser.set("config", "cacheStockData", "y" if self.cacheEnabled else "n")
            parser.set("config", "calculatersiintraday", "y" if self.calculatersiintraday else "n")
            parser.set("config", "daysToLookback", str(self.daysToLookback))
            parser.set("config", "defaultIndex", str(self.defaultIndex))
            parser.set("config", "defaultMonitorOptions", str(self.defaultMonitorOptions))
            parser.set("config", "duration", self.duration)
            parser.set("config", "enablePortfolioCalculations", "y" if self.enablePortfolioCalculations else "n")
            parser.set("config", "generalTimeout", str(self.generalTimeout))
            parser.set("config", "logsEnabled", "y" if (self.logsEnabled or "PKDevTools_Default_Log_Level" in os.environ.keys()) else "n")
            parser.set("config", "longTimeout", str(self.longTimeout))
            parser.set("config", "maxBacktestWindow", str(self.maxBacktestWindow))
            parser.set("config", "maxDashboardWidgetsPerRow", str(self.maxDashboardWidgetsPerRow))
            parser.set("config", "maxNetworkRetryCount", str(self.maxNetworkRetryCount))
            parser.set("config", "maxNumResultRowsInMonitor", str(self.maxNumResultRowsInMonitor))
            parser.set("config", "morninganalysiscandlenumber", str(self.morninganalysiscandlenumber))
            parser.set("config", "morninganalysiscandleduration", self.morninganalysiscandleduration)
            parser.set("config", "onlyStageTwoStocks", "y" if self.stageTwo else "n")
            parser.set("config", "period", self.period)
            parser.set("config", "showPastStrategyData", "y" if self.showPastStrategyData else "n")
            parser.set("config", "showunknowntrends", "y" if self.showunknowntrends else "n")
            parser.set("config", "shuffle", "y" if self.shuffleEnabled else "n")
            parser.set("config", "useEMA", "y" if self.useEMA else "n")

            parser.set("filters", "consolidationPercentage", str(self.consolidationPercentage))
            parser.set("filters", "maxPrice", str(self.maxLTP))
            parser.set("filters", "minimumChangePercentage", str(self.minimumChangePercentage))
            parser.set("filters", "minimumVolume", str(self.minVolume))
            parser.set("filters", "minPrice", str(self.minLTP))
            parser.set("filters", "volumeRatio", str(self.volumeRatio))

            try:
                fp = open("pkscreener.ini", "w")
                parser.write(fp)
                fp.close()
                if showFileCreatedText:
                    OutputControls().printOutput(
                        colorText.BOLD
                        + colorText.GREEN
                        + "[+] Default configuration generated as user configuration is not found!"
                        + colorText.END
                    )
                    input("Press <Enter> to continue...")
                    return
            except IOError as e:  # pragma: no cover
                self.default_logger.debug(e, exc_info=True)
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.FAIL
                    + "[+] Failed to save user config. Exiting.."
                    + colorText.END
                )
                input("Press <Enter> to continue...")
                sys.exit(1)
        else:
            parser = configparser.ConfigParser(strict=False)
            parser.add_section("config")
            parser.add_section("filters")
            OutputControls().printOutput("")
            OutputControls().printOutput(
                colorText.BOLD
                + colorText.GREEN
                + "[+] PKScreener User Configuration:"
                + colorText.END
            )
            self.period = input(
                "[+] Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max\n[+] Enter number of days for which stock data to be downloaded (Days).(Optimal = 280): "
            )
            self.daysToLookback = input(
                "[+] Number of recent trading periods (TimeFrame) to screen for Breakout/Consolidation (Days)(Optimal = 22): "
            )
            self.duration = input(
                "[+] Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo\n[+] Enter Duration of each candle (Days)(Optimal = 1): "
            )
            self.minLTP = input(
                "[+] Minimum Price of Stock to Buy (in RS)(Optimal = 20): "
            )
            self.maxLTP = input(
                "[+] Maximum Price of Stock to Buy (in RS)(Optimal = 50000): "
            )
            self.volumeRatio = input(
                "[+] How many times the volume should be more than average for the breakout? (Number)(Optimal = 2.5): "
            )
            self.consolidationPercentage = input(
                "[+] How many % the price should be in range to consider it as consolidation? (Number)(Optimal = 10): "
            )
            self.shuffle = str(
                input(
                    "[+] Shuffle stocks rather than screening alphabetically? (Y/N): "
                )
            ).lower()
            self.cacheStockData = str(
                input(
                    "[+] Enable High-Performance and Data-Saver mode? (This uses little bit more CPU but performs High Performance Screening) (Y/N): "
                )
            ).lower()
            self.stageTwoPrompt = str(
                input(
                    "[+] Screen only for Stage-2 stocks?\n(What are the stages? => https://www.investopedia.com/articles/trading/08/stock-cycle-trend-price.asp)\n(Y/N): "
                )
            ).lower()
            self.useEmaPrompt = str(
                input(
                    "[+] Use EMA instead of SMA? (EMA is good for Short-term & SMA for Mid/Long-term trades)[Y/N]: "
                )
            ).lower()
            self.showunknowntrendsPrompt = str(
                input(
                    "[+] Show even those results where trends are not known[Y/N] (Recommended Y): "
                )
            ).lower()
            self.logsEnabledPrompt = str(
                input(
                    "[+] Enable Viewing logs? You can enable if you are having problems.[Y/N]: "
                )
            ).lower()
            self.enablePortfolioCalculations = str(
                input(
                    "[+] Enable calculating portfolio values? [Y/N]: "
                )
            ).lower()
            self.showPastStrategyData = str(
                input(
                    "[+] Enable showing past strategy data? [Y/N]: "
                )
            ).lower()
            self.calculatersiintraday = str(
                input(
                    "[+] Calculate intraday RSI during trading hours? [Y/N]: "
                )
            ).lower()
            self.generalTimeout = input(
                "[+] General network timeout (in seconds)(Optimal = 2 for good networks): "
            )
            self.longTimeout = input(
                "[+] Long network timeout for heavier downloads(in seconds)(Optimal = 4 for good networks): "
            )
            self.maxNetworkRetryCount = input(
                "[+] Maximum number of retries in case of network timeout(in seconds)(Optimal = 10 for slow networks): "
            )
            self.defaultIndex = input(
                "[+] Default Index(NSE=12, NASDAQ=15): "
            )
            self.backtestPeriod = input(
                "[+] Number of days in the past for backtesting(in days)(Optimal = 30): "
            )
            self.maxBacktestWindow = input(
                "[+] Number of days to show the results for backtesting(in days)(Optimal = 1 to 30): "
            )
            self.morninganalysiscandlenumber = input(
                "[+] Candle number since the market open time(Optimal = 15 to 60): "
            )
            self.morninganalysiscandleduration = input(
                "[+] Enter Duration of each candle (minutes)(Optimal = 1 to 5): "
            )
            self.minVolume = input(
                "[+] Minimum per day traded volume of any stock (number)(Optimal = 100000): "
            )
            self.backtestPeriodFactor = input(
                "[+] Factor for backtest periods. If you choose 5, 1-Pd would mean 5-Pd returns. (number)(Optimal = 1): "
            )
            self.minimumChangePercentage = input(
                "[+] Minimun change in stock price (in percentage). (number)(Optimal = 0): "
            )
            self.atrTrailingStopPeriod = input(
                "[+] ATR Trailing Stop Periods. (number)(Optimal = 10): "
            )
            self.atrTrailingStopSensitivity = input(
                "[+] ATR Trailing Stop Sensitivity. (number)(Optimal = 1): "
            )
            self.atrTrailingStopEMAPeriod = input(
                "[+] ATR Trailing Stop EMA Period. (number)(Optimal = 1 to 200): "
            )
            parser.set("config", "atrtrailingstopemaperiod", self.atrTrailingStopEMAPeriod)
            parser.set("config", "atrtrailingstopperiod", self.atrTrailingStopPeriod)
            parser.set("config", "atrtrailingstopsensitivity", self.atrTrailingStopSensitivity)
            parser.set("config", "backtestPeriod", self.backtestPeriod)
            parser.set("config", "backtestPeriodFactor", self.backtestPeriodFactor)
            parser.set("config", "cacheStockData", self.cacheStockData)
            parser.set("config", "calculatersiintraday", self.calculatersiintraday)
            parser.set("config", "daysToLookback", self.daysToLookback)
            parser.set("config", "defaultIndex", self.defaultIndex)
            parser.set("config", "defaultMonitorOptions", self.defaultMonitorOptions)
            parser.set("config", "duration", self.duration + "d")
            parser.set("config", "enablePortfolioCalculations", self.enablePortfolioCalculations)
            parser.set("config", "generalTimeout", self.generalTimeout)
            parser.set("config", "logsEnabled", self.logsEnabledPrompt)
            parser.set("config", "longTimeout", self.longTimeout)
            parser.set("config", "maxBacktestWindow", self.maxBacktestWindow)
            parser.set("config", "maxNetworkRetryCount", self.maxNetworkRetryCount)
            parser.set("config", "maxDashboardWidgetsPerRow", self.maxDashboardWidgetsPerRow)
            parser.set("config", "maxNumResultRowsInMonitor", self.maxNumResultRowsInMonitor)
            parser.set("config", "morninganalysiscandleduration", self.morninganalysiscandleduration + "m")
            parser.set("config", "morninganalysiscandlenumber", self.morninganalysiscandlenumber)
            parser.set("config", "onlyStageTwoStocks", self.stageTwoPrompt)
            parser.set("config", "period", self.period + "d")
            parser.set("config", "showPastStrategyData", self.showPastStrategyData)
            parser.set("config", "showunknowntrends", self.showunknowntrendsPrompt)
            parser.set("config", "shuffle", self.shuffle)
            parser.set("config", "useEMA", self.useEmaPrompt)

            parser.set("filters", "consolidationPercentage", self.consolidationPercentage)
            parser.set("filters", "maxPrice", self.maxLTP)
            parser.set("filters", "minimumChangePercentage", self.minimumChangePercentage)
            parser.set("filters", "minimumVolume", self.minVolume)
            parser.set("filters", "minPrice", self.minLTP)
            parser.set("filters", "volumeRatio", self.volumeRatio)

            # delete stock data due to config change
            self.deleteFileWithPattern()
            OutputControls().printOutput(
                colorText.BOLD
                + colorText.FAIL
                + "[+] Cached Stock Data Deleted."
                + colorText.END
            )

            try:
                fp = open("pkscreener.ini", "w")
                parser.write(fp)
                fp.close()
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.GREEN
                    + "[+] User configuration saved."
                    + colorText.END
                )
                input("Press <Enter> to continue...")
                return
            except IOError as e:  # pragma: no cover
                self.default_logger.debug(e, exc_info=True)
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.FAIL
                    + "[+] Failed to save user config. Exiting.."
                    + colorText.END
                )
                input("Press <Enter> to continue...")
                sys.exit(1)

    # Load user config from file
    def getConfig(self, parser):
        if len(parser.read("pkscreener.ini")):
            try:
                self.duration = parser.get("config", "duration")
                self.period = parser.get("config", "period")
                self.minLTP = float(parser.get("filters", "minprice"))
                self.maxLTP = float(parser.get("filters", "maxprice"))
                self.volumeRatio = float(parser.get("filters", "volumeRatio"))
                self.consolidationPercentage = float(
                    parser.get("filters", "consolidationPercentage")
                )
                self.daysToLookback = int(parser.get("config", "daysToLookback"))
                self.shuffleEnabled = (
                    True
                    if "n" not in str(parser.get("config", "shuffle")).lower()
                    else False
                )
                self.cacheEnabled = (
                    True
                    if "n" not in str(parser.get("config", "cachestockdata")).lower()
                    else False
                )
                self.stageTwo = (
                    True
                    if "n"
                    not in str(parser.get("config", "onlyStageTwoStocks")).lower()
                    else False
                )
                self.useEMA = (
                    False
                    if "y" not in str(parser.get("config", "useEMA")).lower()
                    else True
                )
                self.showunknowntrends = (
                    False
                    if "y" not in str(parser.get("config", "showunknowntrends")).lower()
                    else True
                )
                self.logsEnabled = (
                    False
                    if "y" not in str(parser.get("config", "logsEnabled")).lower()
                    else True
                )
                self.enablePortfolioCalculations = (
                    False
                    if "y" not in str(parser.get("config", "enablePortfolioCalculations")).lower()
                    else True
                )
                self.showPastStrategyData = (
                    False
                    if "y" not in str(parser.get("config", "showPastStrategyData")).lower()
                    else True
                )
                self.calculatersiintraday = (
                    False
                    if "y" not in str(parser.get("config", "calculatersiintraday")).lower()
                    else True
                )
                self.atrTrailingStopEMAPeriod = int(parser.get("config", "atrtrailingstopemaperiod"))
                self.atrTrailingStopPeriod = int(parser.get("config", "atrtrailingstopperiod"))
                self.atrTrailingStopSensitivity = float(parser.get("config", "atrtrailingstopsensitivity"))
                self.generalTimeout = float(parser.get("config", "generalTimeout"))
                self.defaultIndex = int(parser.get("config", "defaultIndex"))
                self.longTimeout = float(parser.get("config", "longTimeout"))
                self.maxNetworkRetryCount = int(
                    parser.get("config", "maxNetworkRetryCount")
                )
                self.backtestPeriod = int(parser.get("config", "backtestPeriod"))
                self.maxBacktestWindow = int(parser.get("config", "maxBacktestWindow"))
                self.morninganalysiscandlenumber = int(parser.get("config", "morninganalysiscandlenumber"))
                self.morninganalysiscandleduration = parser.get("config", "morninganalysiscandleduration")
                self.minVolume = int(parser.get("filters", "minimumVolume"))
                self.minimumChangePercentage = float(parser.get("filters", "minimumchangepercentage"))
                self.backtestPeriodFactor = int(parser.get("config", "backtestPeriodFactor"))
                self.defaultMonitorOptions = str(parser.get("config", "defaultMonitorOptions"))
                self.maxDashboardWidgetsPerRow = int(parser.get("config", "maxDashboardWidgetsPerRow"))
                self.maxNumResultRowsInMonitor = int(parser.get("config", "maxNumResultRowsInMonitor"))
            except configparser.NoOptionError as e:# pragma: no cover
                self.default_logger.debug(e, exc_info=True)
                # input(colorText.BOLD + colorText.FAIL +
                #       '[+] pkscreener requires user configuration again. Press enter to continue..' + colorText.END)
                parser.remove_section("config")
                parser.remove_section("filters")
                self.setConfig(parser, default=True, showFileCreatedText=False)
            except Exception as e:  # pragma: no cover
                self.default_logger.debug(e, exc_info=True)
                # input(colorText.BOLD + colorText.FAIL +
                #       '[+] pkscreener requires user configuration again. Press enter to continue..' + colorText.END)
                parser.remove_section("config")
                parser.remove_section("filters")
                self.setConfig(parser, default=True, showFileCreatedText=False)
        else:
            self.setConfig(parser, default=True, showFileCreatedText=False)

    # Toggle the duration and period for use in intraday and swing trading
    def toggleConfig(self, candleDuration, clearCache=True):
        if candleDuration is None:
            candleDuration = self.duration.lower()
        self.getConfig(parser)
        if candleDuration[-1] in ["d"]:
            self.period = "280d"
            self.cacheEnabled = True
        if candleDuration[-1] in ["m", "h"] and not self.isIntradayConfig():
            self.period = "1d"
            self.cacheEnabled = True
        if self.isIntradayConfig():
            self.duration = candleDuration if candleDuration[-1] in ["m", "h"] else "1m"
            candleType = candleDuration.replace("m","").replace("h","")
            if candleDuration[-1] in ["m"]:
                lookback = int(60/int(candleType)) * 6 # 6 hours
            elif candleDuration[-1] in ["h"]:
                lookback = (int(24/int(candleType)) + 1 )*2 #  at least 24 hours
            self.daysToLookback = lookback  # At least the past 6 to 24 hours
        else:
            self.duration = candleDuration if candleDuration[-1] == "d" else "1d"
            self.daysToLookback = 22  # At least the past 1.5 month
        self.setConfig(parser, default=True, showFileCreatedText=False)
        if clearCache:
            # Delete any cached *.pkl data
            self.deleteFileWithPattern()
            # Delete any cached session data
            self.restartRequestsCache()

    def restartRequestsCache(self):
        import requests_cache
        try:
            if requests_cache.is_installed():
                requests_cache.clear()
                requests_cache.uninstall_cache()
            cache_file = os.path.join(
                    Archiver.get_user_outputs_dir(), "PKDevTools_cache.sqlite")
            if os.path.isfile(cache_file):
                os.remove(cache_file)
            self.deleteFileWithPattern("*_cache.sqlite")
            requests_cache.install_cache(
                cache_name=f"{Archiver.get_user_outputs_dir().split(os.sep)[-1]}{os.sep}PKDevTools_cache",
                db_path=os.path.join(
                    Archiver.get_user_outputs_dir(), "PKDevTools_cache.sqlite"
                ),
            )
        except Exception as e:  # pragma: no cover
            self.default_logger.debug(e, exc_info=True)

    def isIntradayConfig(self):
        return self.period == "1d"

    # Print config file
    def showConfigFile(self, defaultAnswer=None):
        try:
            prompt = "[+] PKScreener User Configuration:"
            f = open("pkscreener.ini", "r")
            OutputControls().printOutput(colorText.BOLD + colorText.GREEN + prompt + colorText.END)
            configData = f.read()
            f.close()
            OutputControls().printOutput("\n" + configData)
            if defaultAnswer is None:
                input("Press <Enter> to continue...")
            return f"{prompt}\n{configData}"
        except Exception as e:  # pragma: no cover
            self.default_logger.debug(e, exc_info=True)
            OutputControls().printOutput(
                colorText.BOLD
                + colorText.FAIL
                + "[+] User Configuration not found!"
                + colorText.END
            )
            OutputControls().printOutput(
                colorText.BOLD
                + colorText.WARN
                + "[+] Configure the limits to continue."
                + colorText.END
            )
            self.setConfig(parser, default=True, showFileCreatedText=False)

    # Check if config file exists
    def checkConfigFile(self):
        try:
            f = open("pkscreener.ini", "r")
            f.close()
            self.getConfig(parser)
            return True
        except FileNotFoundError as e:  # pragma: no cover
            self.default_logger.debug(e, exc_info=True)
            self.setConfig(parser, default=True, showFileCreatedText=False)
