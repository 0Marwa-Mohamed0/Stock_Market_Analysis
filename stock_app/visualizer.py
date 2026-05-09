import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# ── Shared theme ───────────────────────────────────────────────────────────────
BG       = "#111827"
BG_PAPER = "#111827"
GRID     = "rgba(255,255,255,0.05)"
TEXT     = "#94a3b8"
GREEN    = "#00ff88"
RED      = "#ff4d6d"
BLUE     = "#3b82f6"
YELLOW   = "#fbbf24"
PURPLE   = "#a78bfa"

LAYOUT_BASE = dict(
    paper_bgcolor=BG_PAPER,
    plot_bgcolor=BG,
    font=dict(family="Space Mono, monospace", color=TEXT, size=11),
    margin=dict(l=16, r=16, t=40, b=16),
    legend=dict(
        bgcolor="rgba(17,24,39,0.8)",
        bordercolor="rgba(255,255,255,0.08)",
        borderwidth=1,
        font=dict(size=10),
    ),
    xaxis=dict(
        gridcolor=GRID, zeroline=False,
        tickfont=dict(size=10),
        showspikes=True, spikecolor=GRID, spikethickness=1,
    ),
    yaxis=dict(
        gridcolor=GRID, zeroline=False,
        tickfont=dict(size=10),
        showspikes=True, spikecolor=GRID, spikethickness=1,
    ),
    hovermode="x unified",
)


class StockVisualizer:
    """All Plotly chart builders."""

    # ── 1. Price line chart with gradient fill ────────────────────────────────
    def plot_price_chart(self, df: pd.DataFrame, symbol: str, period: str) -> go.Figure:
        first = df["Close"].iloc[0]
        last  = df["Close"].iloc[-1]
        color = GREEN if last >= first else RED

        fig = go.Figure()

        # Area fill
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Close"],
            mode="lines",
            name="Close Price",
            line=dict(color=color, width=2),
            fill="tozeroy",
            fillcolor=f"rgba({_hex_to_rgb(color)},0.08)",
            hovertemplate="<b>%{x|%Y-%m-%d}</b><br>Price: $%{y:.2f}<extra></extra>",
        ))

        layout = {**LAYOUT_BASE}
        layout["title"] = dict(
            text=f"{symbol} — Close Price ({period})",
            font=dict(size=14, color="#f1f5f9"),
            x=0.01
        )
        layout["yaxis"] = {**layout.get("yaxis", {}), "tickprefix": "$"}
        fig.update_layout(**layout)
        return fig

    # ── 2. Volume bar chart ───────────────────────────────────────────────────
    def plot_volume_chart(self, df: pd.DataFrame, symbol: str) -> go.Figure:
        colors = [GREEN if r >= 0 else RED
                  for r in df.get("Daily_Return", [0] * len(df))]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df.index,
            y=df["Volume"],
            name="Volume",
            marker_color=colors,
            opacity=0.75,
            hovertemplate="<b>%{x|%Y-%m-%d}</b><br>Vol: %{y:,.0f}<extra></extra>",
        ))

        layout = {**LAYOUT_BASE}
        layout["title"] = dict(
            text=f"{symbol} — Trading Volume",
            font=dict(size=14, color="#f1f5f9"), x=0.01
        )
        fig.update_layout(**layout)
        return fig

    # ── 3. Moving averages ────────────────────────────────────────────────────
    def plot_moving_averages(self, df: pd.DataFrame, symbol: str) -> go.Figure:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df.index, y=df["Close"],
            name="Close", mode="lines",
            line=dict(color="rgba(255,255,255,0.35)", width=1),
            hovertemplate="Close: $%{y:.2f}<extra></extra>",
        ))

        ma_config = [
            ("MA7",  YELLOW, "MA 7"),
            ("MA20", BLUE,   "MA 20"),
            ("MA50", PURPLE, "MA 50"),
        ]
        for col, clr, lbl in ma_config:
            if col in df.columns:
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[col],
                    name=lbl, mode="lines",
                    line=dict(color=clr, width=1.8),
                    hovertemplate=f"{lbl}: $%{{y:.2f}}<extra></extra>",
                ))

        layout = {**LAYOUT_BASE}
        layout["title"] = dict(
            text=f"{symbol} — Moving Averages",
            font=dict(size=14, color="#f1f5f9"), x=0.01
        )
        layout["yaxis"] = {**layout.get("yaxis", {}), "tickprefix": "$"}
        fig.update_layout(**layout)
        return fig

    # ── 4. Candlestick ────────────────────────────────────────────────────────
    def plot_candlestick(self, df: pd.DataFrame, symbol: str) -> go.Figure:
        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df["Open"], high=df["High"],
            low=df["Low"],   close=df["Close"],
            name="OHLC",
            increasing=dict(line=dict(color=GREEN), fillcolor=f"rgba({_hex_to_rgb(GREEN)},0.7)"),
            decreasing=dict(line=dict(color=RED),   fillcolor=f"rgba({_hex_to_rgb(RED)},0.7)"),
        ))

        layout = {**LAYOUT_BASE}
        layout["title"] = dict(
            text=f"{symbol} — Candlestick",
            font=dict(size=13, color="#f1f5f9"), x=0.01
        )
        layout["xaxis_rangeslider_visible"] = False
        layout["yaxis"] = {**layout.get("yaxis", {}), "tickprefix": "$"}
        fig.update_layout(**layout)
        return fig

    # ── 5. Daily returns histogram ────────────────────────────────────────────
    def plot_daily_returns(self, df: pd.DataFrame, symbol: str) -> go.Figure:
        returns = df["Daily_Return"].dropna()

        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=returns,
            nbinsx=30,
            name="Daily Return",
            marker_color=BLUE,
            opacity=0.8,
            hovertemplate="Return: %{x:.2f}%<br>Count: %{y}<extra></extra>",
        ))

        # zero line
        fig.add_vline(x=0, line_color="rgba(255,255,255,0.3)", line_dash="dash")

        layout = {**LAYOUT_BASE}
        layout["title"] = dict(
            text=f"{symbol} — Daily Returns",
            font=dict(size=13, color="#f1f5f9"), x=0.01
        )
        layout["xaxis"] = {**layout.get("xaxis", {}), "ticksuffix": "%"}
        fig.update_layout(**layout)
        return fig


# ── Helper ─────────────────────────────────────────────────────────────────────
def _hex_to_rgb(hex_color: str) -> str:
    """Convert #rrggbb to 'r,g,b' string for rgba()."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r},{g},{b}"
