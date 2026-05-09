import yfinance as yf
import pandas as pd


class StockDataFetcher:
    """Handles all API calls to Yahoo Finance via yfinance."""

    def get_stock_info(self, symbol: str):
        """
        Fetch general info about a stock (name, sector, P/E, etc.)
        Returns: (info_dict, error_message)
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # yfinance returns a minimal dict for invalid symbols
            if not info or info.get("regularMarketPrice") is None and info.get("currentPrice") is None:
                # Try fast_info as fallback
                fast = ticker.fast_info
                if not hasattr(fast, "last_price") or fast.last_price is None:
                    return {}, f"Symbol '{symbol}' not found."

            return info, None
        except Exception as e:
            return {}, str(e)

    def get_historical_data(self, symbol: str, period: str = "1mo"):
        """
        Fetch OHLCV historical data.
        period options: 7d, 1mo, 3mo, 6mo, 1y, 2y, 5y
        Returns: (DataFrame, error_message)
        """
        try:
            ticker = yf.Ticker(symbol)

            # yfinance uses 7d not 7d for recent data
            yf_period = period if period != "7d" else "7d"
            hist = ticker.history(period=yf_period, auto_adjust=True)

            if hist is None or hist.empty:
                return None, f"No historical data available for '{symbol}'."

            return hist, None
        except Exception as e:
            return None, str(e)
