import pandas as pd
import numpy as np


class StockDataProcessor:
    """Cleans, processes, and computes indicators on stock data."""

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove NaN rows, sort by date, reset index."""
        df = df.copy()
        df.dropna(subset=["Close"], inplace=True)
        df.sort_index(inplace=True)
        return df

    def add_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add technical indicators:
        - MA7  : 7-day moving average
        - MA20 : 20-day moving average
        - MA50 : 50-day moving average
        - Daily_Return : percentage change day-over-day
        - Cum_Return   : cumulative return from start of window
        """
        df = df.copy()

        df["MA7"]  = df["Close"].rolling(window=7,  min_periods=1).mean()
        df["MA20"] = df["Close"].rolling(window=20, min_periods=1).mean()
        df["MA50"] = df["Close"].rolling(window=50, min_periods=1).mean()

        df["Daily_Return"] = df["Close"].pct_change() * 100          # %
        df["Cum_Return"]   = ((df["Close"] / df["Close"].iloc[0]) - 1) * 100

        return df

    def get_summary_stats(self, df: pd.DataFrame, info: dict) -> dict:
        """Compute summary metrics shown in the header cards."""
        current_price  = df["Close"].iloc[-1]
        previous_close = df["Close"].iloc[-2] if len(df) > 1 else current_price
        day_change_pct = ((current_price - previous_close) / previous_close) * 100

        # 52-week high/low from info, fallback to df
        high_52w = info.get("fiftyTwoWeekHigh") or df["High"].max()
        low_52w  = info.get("fiftyTwoWeekLow")  or df["Low"].min()

        # Market cap formatting
        mkt_cap_raw = info.get("marketCap")
        if mkt_cap_raw:
            if mkt_cap_raw >= 1e12:
                mkt_cap = f"{mkt_cap_raw/1e12:.2f}T"
            elif mkt_cap_raw >= 1e9:
                mkt_cap = f"{mkt_cap_raw/1e9:.2f}B"
            elif mkt_cap_raw >= 1e6:
                mkt_cap = f"{mkt_cap_raw/1e6:.2f}M"
            else:
                mkt_cap = str(mkt_cap_raw)
        else:
            mkt_cap = "N/A"

        # Volume formatting
        avg_vol_raw = info.get("averageVolume")
        if avg_vol_raw:
            if avg_vol_raw >= 1e6:
                avg_vol = f"{avg_vol_raw/1e6:.1f}M"
            elif avg_vol_raw >= 1e3:
                avg_vol = f"{avg_vol_raw/1e3:.0f}K"
            else:
                avg_vol = str(avg_vol_raw)
        else:
            avg_vol = "N/A"

        # P/E, EPS, Beta, Dividend
        pe    = info.get("trailingPE")
        eps   = info.get("trailingEps")
        beta  = info.get("beta")
        div_y = info.get("dividendYield")

        return {
            "current_price":  f"{current_price:.2f}",
            "day_change_pct": day_change_pct,
            "high_52w":       f"{high_52w:.2f}",
            "low_52w":        f"{low_52w:.2f}",
            "market_cap":     mkt_cap,
            "avg_volume":     avg_vol,
            "pe_ratio":       f"{pe:.2f}"  if pe   else "N/A",
            "eps":            f"{eps:.2f}" if eps  else "N/A",
            "beta":           f"{beta:.2f}" if beta else "N/A",
            "dividend_yield": f"{div_y*100:.2f}%" if div_y else "N/A",
        }

    def get_display_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return a clean, human-readable DataFrame for the data table."""
        cols = ["Open", "High", "Low", "Close", "Volume", "Daily_Return"]
        available = [c for c in cols if c in df.columns]
        display = df[available].copy()

        # Round floats
        for col in ["Open", "High", "Low", "Close", "Daily_Return"]:
            if col in display.columns:
                display[col] = display[col].round(2)

        # Format volume
        if "Volume" in display.columns:
            display["Volume"] = display["Volume"].apply(
                lambda x: f"{int(x):,}" if pd.notnull(x) else "N/A"
            )

        # Format daily return
        if "Daily_Return" in display.columns:
            display["Daily_Return"] = display["Daily_Return"].apply(
                lambda x: f"{x:+.2f}%" if pd.notnull(x) else "N/A"
            )

        # Format index
        display.index = display.index.strftime("%Y-%m-%d")
        display.index.name = "Date"

        return display.iloc[::-1]   # most recent first
