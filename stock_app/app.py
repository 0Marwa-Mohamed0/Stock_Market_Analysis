import streamlit as st
import pandas as pd
from data_fetcher import StockDataFetcher
from data_processor import StockDataProcessor
from visualizer import StockVisualizer

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Market Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #1a2235;
    --accent-green: #00ff88;
    --accent-red: #ff4d6d;
    --accent-blue: #3b82f6;
    --accent-yellow: #fbbf24;
    --text-primary: #f1f5f9;
    --text-muted: #64748b;
    --border: rgba(255,255,255,0.07);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0f172a 50%, #0a0e1a 100%);
}

/* Header */
.main-header {
    background: linear-gradient(90deg, rgba(0,255,136,0.08) 0%, rgba(59,130,246,0.08) 100%);
    border: 1px solid rgba(0,255,136,0.2);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0,255,136,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.main-header h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent-green);
    margin: 0;
    letter-spacing: -1px;
}
.main-header p {
    color: var(--text-muted);
    margin: 6px 0 0 0;
    font-size: 0.95rem;
}

/* Metric Cards */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
}
.metric-card:hover {
    border-color: rgba(0,255,136,0.3);
    transform: translateY(-2px);
}
.metric-card .label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-muted);
    font-family: 'Space Mono', monospace;
    margin-bottom: 8px;
}
.metric-card .value {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
}
.metric-card .change {
    font-size: 0.85rem;
    margin-top: 6px;
    font-weight: 500;
}
.change-pos { color: var(--accent-green); }
.change-neg { color: var(--accent-red); }

/* Stock Info Section */
.stock-info-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
}
.stock-info-box h3 {
    font-family: 'Space Mono', monospace;
    color: var(--accent-blue);
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 10px;
}
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.03);
}
.info-row:last-child { border-bottom: none; }
.info-row .key {
    color: var(--text-muted);
    font-size: 0.85rem;
}
.info-row .val {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: var(--text-primary);
    font-weight: 500;
}

/* Ticker Badge */
.ticker-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(59,130,246,0.15));
    border: 1px solid rgba(0,255,136,0.3);
    color: var(--accent-green);
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* Streamlit inputs override */
.stTextInput input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 1rem !important;
    padding: 10px 14px !important;
}
.stTextInput input:focus {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 2px rgba(0,255,136,0.15) !important;
}

.stButton button {
    background: linear-gradient(135deg, #00ff88, #00cc6a) !important;
    color: #0a0e1a !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    width: 100% !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(0,255,136,0.4) !important;
}

.stSelectbox select, div[data-baseweb="select"] {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-muted) !important;
    border-radius: 8px;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background: rgba(0,255,136,0.15) !important;
    color: var(--accent-green) !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* DataFrame */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Alert/info */
.stAlert {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    border-left-color: var(--accent-blue) !important;
}

/* Spinner */
.stSpinner { color: var(--accent-green) !important; }

/* Section headers */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--text-muted);
    margin: 24px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Volume bar color patch */
.stPlotlyChart { border-radius: 12px; overflow: hidden; }
</style>

""", unsafe_allow_html=True)


# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px;">
        <div style="font-family:'Space Mono',monospace; font-size:1.4rem; 
                    color:#00ff88; font-weight:700; letter-spacing:-1px;">
            📈 StockLens
        </div>
        <div style="color:#64748b; font-size:0.8rem; margin-top:4px;">
            Market Analysis System
        </div>
    </div>
    <hr style="margin:16px 0;">
    """, unsafe_allow_html=True)

    st.markdown("**🔍 Search Stock**")
    symbol_input = st.text_input(
        "Stock Symbol",
        value="",
        placeholder="e.g. AAPL, MSFT, TSLA",
        label_visibility="collapsed"
    )

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    period_options = {
        "1 Week":  "7d",
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year":  "1y",
    }
    period_label = st.selectbox("Period", list(period_options.keys()), index=1)
    period = period_options[period_label]

    analyze_btn = st.button("⚡ Analyze")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="color:#64748b; font-size:0.78rem; line-height:1.7;">
        <b style="color:#94a3b8;">Popular Symbols</b><br>
        AAPL · MSFT · GOOGL<br>
        AMZN · TSLA · META<br>
        NVDA · NFLX · AMD
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="color:#64748b; font-size:0.75rem; text-align:center; line-height:1.6;">
        Data via Yahoo Finance<br>
        <span style="color:#374151;">yfinance · plotly · pandas</span>
    </div>
    """, unsafe_allow_html=True)


# ─── Main Content ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📈 Stock Market Analysis</h1>
    <p>Real-time data · Interactive charts · Technical indicators</p>
</div>
""", unsafe_allow_html=True)

fetcher   = StockDataFetcher()
processor = StockDataProcessor()
viz       = StockVisualizer()

# ─── FIX: Only run when user clicks Analyze ────────────────────────────────────
if analyze_btn:
    symbol = symbol_input.strip().upper()

    if not symbol:
        st.warning("⚠️ Please enter a stock symbol.")
        st.stop()

    with st.spinner(f"Fetching data for **{symbol}**..."):
        info, error_info = fetcher.get_stock_info(symbol)
        hist, error_hist = fetcher.get_historical_data(symbol, period)

    # ── Validation ────────────────────────────────────────────────────────────
    if error_info or error_hist or hist is None or hist.empty:
        st.error(f"❌ Could not retrieve data for **'{symbol}'**. "
                 "Please check the symbol and try again.")
        st.info("💡 Try symbols like: AAPL, MSFT, TSLA, GOOGL, AMZN")
        st.stop()

    # ── Process ───────────────────────────────────────────────────────────────
    hist = processor.clean_data(hist)
    hist = processor.add_indicators(hist)
    summary = processor.get_summary_stats(hist, info)

    # ── Ticker Badge ──────────────────────────────────────────────────────────
    company_name = info.get("longName", symbol)
    st.markdown(f"""
    <div class="ticker-badge">● {symbol}</div>
    <div style="font-size:1.3rem; font-weight:600; margin-bottom:20px;">
        {company_name}
    </div>
    """, unsafe_allow_html=True)

    # ── Metric Cards ──────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("CURRENT PRICE",  summary["current_price"], summary["day_change_pct"], "$"),
        ("52W HIGH",        summary["high_52w"],       None, "$"),
        ("52W LOW",         summary["low_52w"],        None, "$"),
        ("MARKET CAP",      summary["market_cap"],     None, ""),
    ]
    for col, (label, val, chg, prefix) in zip([c1,c2,c3,c4], metrics):
        chg_html = ""
        if chg is not None:
            cls = "change-pos" if chg >= 0 else "change-neg"
            arrow = "▲" if chg >= 0 else "▼"
            chg_html = f'<div class="change {cls}">{arrow} {abs(chg):.2f}% today</div>'
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">{label}</div>
                <div class="value">{prefix}{val}</div>
                {chg_html}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Price Chart",
        "📉 Technical",
        "📋 Historical Data",
        "ℹ️ Company Info"
    ])

    with tab1:
        st.markdown('<div class="section-title">Price Trend</div>', unsafe_allow_html=True)
        fig_price = viz.plot_price_chart(hist, symbol, period_label)
        st.plotly_chart(fig_price, use_container_width=True)

        st.markdown('<div class="section-title">Trading Volume</div>', unsafe_allow_html=True)
        fig_vol = viz.plot_volume_chart(hist, symbol)
        st.plotly_chart(fig_vol, use_container_width=True)

    with tab2:
        st.markdown('<div class="section-title">Moving Averages</div>', unsafe_allow_html=True)
        fig_ma = viz.plot_moving_averages(hist, symbol)
        st.plotly_chart(fig_ma, use_container_width=True)

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown('<div class="section-title">OHLC Candlestick</div>', unsafe_allow_html=True)
            fig_candle = viz.plot_candlestick(hist, symbol)
            st.plotly_chart(fig_candle, use_container_width=True)
        with col_r:
            st.markdown('<div class="section-title">Daily Return Distribution</div>', unsafe_allow_html=True)
            fig_ret = viz.plot_daily_returns(hist, symbol)
            st.plotly_chart(fig_ret, use_container_width=True)

    with tab3:
        st.markdown('<div class="section-title">Historical Prices</div>', unsafe_allow_html=True)
        display_df = processor.get_display_dataframe(hist)
        st.dataframe(display_df, use_container_width=True, height=420)

        csv = display_df.to_csv(index=True)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"{symbol}_historical.csv",
            mime="text/csv"
        )

    with tab4:
        st.markdown('<div class="section-title">Company Overview</div>', unsafe_allow_html=True)
        col_info1, col_info2 = st.columns(2)

        info_left = {
            "Sector":        info.get("sector", "N/A"),
            "Industry":      info.get("industry", "N/A"),
            "Country":       info.get("country", "N/A"),
            "Exchange":      info.get("exchange", "N/A"),
            "Currency":      info.get("currency", "N/A"),
        }
        info_right = {
            "P/E Ratio":     summary.get("pe_ratio", "N/A"),
            "EPS":           summary.get("eps", "N/A"),
            "Dividend Yield":summary.get("dividend_yield", "N/A"),
            "Beta":          summary.get("beta", "N/A"),
            "Avg Volume":    summary.get("avg_volume", "N/A"),
        }

        def render_info_box(title, data):
            rows = "".join(
                f'<div class="info-row"><span class="key">{k}</span>'
                f'<span class="val">{v}</span></div>'
                for k, v in data.items()
            )
            st.markdown(f"""
            <div class="stock-info-box">
                <h3>{title}</h3>
                {rows}
            </div>
            """, unsafe_allow_html=True)

        with col_info1:
            render_info_box("🏢 Company Details", info_left)
        with col_info2:
            render_info_box("💹 Financial Metrics", info_right)

        bio = info.get("longBusinessSummary", "")
        if bio:
            st.markdown('<div class="section-title">About</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:var(--bg-card); border:1px solid var(--border);
                        border-radius:12px; padding:20px 24px; 
                        color:#94a3b8; font-size:0.88rem; line-height:1.75;">
                {bio[:600]}{"..." if len(bio) > 600 else ""}
            </div>
            """, unsafe_allow_html=True)

else:
    # ── Welcome State ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:80px 20px;">
        <div style="font-size:4rem; margin-bottom:20px;">📊</div>
        <div style="font-family:'Space Mono',monospace; font-size:1.4rem; 
                    color:#f1f5f9; margin-bottom:12px;">
            Enter a stock symbol to begin
        </div>
        <div style="color:#64748b; font-size:0.95rem; max-width:400px; 
                    margin:0 auto; line-height:1.7;">
            Type a ticker in the sidebar (e.g. <code style="color:#00ff88;">AAPL</code>), 
            choose your time period, and hit <strong>Analyze</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)
