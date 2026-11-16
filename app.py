import hashlib
import html
import io

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


BUILD = "RISK-LENS / 02"

BG = "#0b1118"
PANEL = "#111c27"
TEXT = "#edf3f8"
MUTED = "#98a9ba"
LIME = "#c3f36b"
CORAL = "#fb8b98"

st.set_page_config(
    page_title="RiskLens · Market Risk Studio",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="auto",
)


CSS = """
<style>
:root { color-scheme: dark; }

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #0b1118 !important;
    color: #edf3f8 !important;
}

[data-testid="stHeader"] {
    background: #0b1118 !important;
}

[data-testid="stHeader"] button {
    color: #edf3f8 !important;
}

[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {
    background: #0e1721 !important;
    color: #edf3f8 !important;
}

[data-testid="stSidebar"] {
    border-right: 1px solid #23303e;
}

.block-container {
    max-width: 1440px;
    padding: 2rem 3rem;
}

[data-testid="stSidebarUserContent"] {
    padding-top: 1.5rem;
}

/* Streamlit 기본 글자색도 명시적으로 지정 */
[data-testid="stMain"] [data-testid="stMarkdownContainer"] :is(p,li,h1,h2,h3,h4),
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] :is(p,li,h1,h2,h3,h4),
[data-testid="stWidgetLabel"] p {
    color: #edf3f8 !important;
}

[data-testid="stCaptionContainer"] p {
    color: #98a9ba !important;
}

[data-testid="stMain"] hr,
[data-testid="stSidebar"] hr {
    border-color: #263544 !important;
}

/* 버튼 */
[data-testid="stButton"] button,
[data-testid="stDownloadButton"] button {
    background: #152230 !important;
    color: #edf3f8 !important;
    border: 1px solid #344658 !important;
    border-radius: 10px !important;
    min-height: 46px;
    transition: border-color .15s, transform .15s;
}

[data-testid="stButton"] button p,
[data-testid="stDownloadButton"] button p {
    color: #edf3f8 !important;
    font-weight: 600 !important;
}

[data-testid="stButton"] button:hover,
[data-testid="stDownloadButton"] button:hover {
    border-color: #c3f36b !important;
    transform: translateY(-1px);
}

[data-testid="stButton"] button[kind="primary"] {
    background: #c3f36b !important;
    color: #14200b !important;
    border-color: #c3f36b !important;
}

[data-testid="stButton"] button[kind="primary"] p {
    color: #14200b !important;
}

/* 입력 요소 */
[data-baseweb="select"] > div,
[data-testid="stNumberInput"] > div,
[data-testid="stNumberInput"] input {
    background: #152230 !important;
    color: #edf3f8 !important;
    border-color: #344658 !important;
}

[data-baseweb="select"] :is(span, input),
[data-testid="stNumberInput"] button {
    color: #edf3f8 !important;
}

[data-baseweb="popover"] > div,
[role="listbox"],
[role="option"] {
    background: #152230 !important;
    color: #edf3f8 !important;
}

[role="option"]:hover {
    background: #253b4e !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: #111e2b !important;
    border: 1px dashed #3c5064 !important;
}

[data-testid="stFileUploaderDropzone"] :is(span,small,svg) {
    color: #b9c8d5 !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: #1a2b3c !important;
    color: #edf3f8 !important;
    border-color: #3c5064 !important;
}

[data-testid="stFileUploaderDropzone"] button p {
    color: #edf3f8 !important;
}

/* 탭과 안내 */
[data-testid="stTabs"] [role="tablist"] {
    gap: 24px;
    border-bottom: 1px solid #263544;
}

[data-testid="stTabs"] button[role="tab"] {
    color: #98a9ba !important;
    padding: 12px 0;
}

[data-testid="stTabs"] button[role="tab"] p {
    color: #98a9ba !important;
}

[data-testid="stTabs"] button[aria-selected="true"] p {
    color: #c3f36b !important;
}

[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background: #c3f36b !important;
}

[data-testid="stExpander"] {
    background: #111c27 !important;
    border-color: #293b4d !important;
    border-radius: 12px;
}

[data-testid="stExpander"] summary {
    color: #edf3f8 !important;
}

[data-testid="stAlert"] {
    background: #172737 !important;
    color: #edf3f8 !important;
    border-radius: 12px;
}

[data-testid="stAlert"] p {
    color: #dce8f3 !important;
}

[data-testid="stTooltipIcon"] {
    color: #98a9ba !important;
}

[data-testid="stBottomBlockContainer"] {
    background: #0b1118 !important;
}

/* 브랜드와 홈 */
.r-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    border-bottom: 1px solid #263544;
    padding-bottom: 21px;
    margin-bottom: 34px;
}

.r-brand {
    color: #edf3f8 !important;
    font-size: 22px;
    font-weight: 750;
    letter-spacing: -.8px;
}

.r-brand span {
    color: #c3f36b !important;
    margin-right: 9px;
}

.r-topnote, .r-eyebrow {
    color: #98a9ba !important;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 650;
}

.r-sidebrand {
    color: #edf3f8 !important;
    font-size: 25px;
    font-weight: 750;
    margin-bottom: 5px;
}

.r-sidebrand span {
    color: #c3f36b !important;
}

.r-side-note {
    color: #98a9ba !important;
    font-size: 12px;
    line-height: 1.8;
    margin-bottom: 24px;
}

.r-section-label {
    color: #98a9ba !important;
    font-size: 11px;
    letter-spacing: 1.8px;
    margin: 18px 0 12px;
}

.r-hero {
    padding: 22px 0 4px;
}

.r-pill {
    display: inline-block;
    color: #c3f36b !important;
    background: #1b2a1d;
    border: 1px solid #3a5030;
    border-radius: 30px;
    padding: 6px 12px;
    font-size: 11px;
    letter-spacing: 1.4px;
    margin-bottom: 23px;
}

.r-hero-title {
    color: #edf3f8 !important;
    font-size: clamp(35px,3.8vw,57px);
    font-weight: 750;
    letter-spacing: -2.5px;
    line-height: 1.35;
    margin-bottom: 20px;
    word-break: keep-all;
}

.r-hero-title span {
    color: #c3f36b !important;
}

.r-hero-copy {
    color: #aabac9 !important;
    font-size: 15px;
    line-height: 1.95;
    max-width: 450px;
    margin-bottom: 23px;
    word-break: keep-all;
}

.r-small {
    color: #98a9ba !important;
    font-size: 12px;
    line-height: 1.8;
}

/* 홈의 샘플 미리보기 */
.r-preview {
    background: radial-gradient(
        ellipse at 95% 0%, #21332a 0%, #111c27 55%
    );
    border: 1px solid #2b3f47;
    border-radius: 22px;
    padding: 26px;
    margin-top: 20px;
    box-shadow: 0 22px 60px #00000028;
}

.r-preview-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.r-preview-name {
    color: #edf3f8 !important;
    font-size: 15px;
    font-weight: 650;
    margin: 10px 0 5px;
}

.r-demo-label {
    color: #c3f36b !important;
    font-size: 10px;
    letter-spacing: 1px;
    border: 1px solid #476039;
    border-radius: 20px;
    padding: 4px 9px;
    white-space: nowrap;
}

.r-preview-value {
    color: #edf3f8 !important;
    font-size: 34px;
    letter-spacing: -1px;
    font-weight: 700;
}

.r-spark {
    width: 100%;
    height: 165px;
    display: block;
    margin: 16px 0 4px;
}

.r-axis {
    display: flex;
    justify-content: space-between;
    color: #98a9ba !important;
    font-size: 10px;
}

.r-preview-stats {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12px;
    border-top: 1px solid #2b3b46;
    margin-top: 20px;
    padding-top: 17px;
}

.r-preview-stat-label {
    color: #98a9ba !important;
    font-size: 10px;
    margin-bottom: 5px;
}

.r-preview-stat-value {
    color: #edf3f8 !important;
    font-size: 19px;
    font-weight: 650;
}

.r-preview-stat-value.accent {
    color: #c3f36b !important;
}

/* 기능 소개 */
.r-section-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 12px;
    margin: 45px 0 16px;
}

.r-section-title {
    color: #edf3f8 !important;
    font-size: 20px;
    font-weight: 650;
    letter-spacing: -.6px;
}

.r-feature {
    background: #111c27;
    border: 1px solid #263544;
    border-radius: 16px;
    padding: 23px;
    min-height: 175px;
}

.r-feature-number {
    color: #c3f36b !important;
    font-size: 12px;
    letter-spacing: 1px;
    margin-bottom: 18px;
}

.r-feature-title {
    color: #edf3f8 !important;
    font-size: 17px;
    font-weight: 650;
    margin-bottom: 8px;
}

.r-feature-copy {
    color: #aabac9 !important;
    font-size: 13px;
    line-height: 1.8;
    word-break: keep-all;
}

.r-guide {
    border: 1px solid #263544;
    border-radius: 14px;
    padding: 18px 22px;
    margin-top: 24px;
    color: #b2c1cf !important;
    font-size: 13px;
    line-height: 1.9;
}

.r-guide span {
    color: #c3f36b !important;
    font-weight: 650;
}

.r-footer {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
    border-top: 1px solid #263544;
    margin-top: 40px;
    padding: 18px 0;
    color: #98a9ba !important;
    font-size: 11px;
    line-height: 1.8;
}

/* 분석 화면 */
.r-dashboard-title {
    color: #edf3f8 !important;
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -1.3px;
    margin: 8px 0;
}

.r-dashboard-copy {
    color: #aabac9 !important;
    font-size: 13px;
    line-height: 1.9;
    margin-bottom: 23px;
}

.r-banner {
    color: #bdd6c2 !important;
    background: #17291f;
    border: 1px solid #2e4a38;
    border-radius: 10px;
    padding: 11px 16px;
    font-size: 12px;
    line-height: 1.8;
    margin: 0 0 20px;
}

.r-metric {
    background: #111c27;
    border: 1px solid #263544;
    border-radius: 16px;
    padding: 20px;
    min-height: 155px;
    margin-bottom: 14px;
}

.r-metric.featured {
    border-color: #637944;
    background: linear-gradient(135deg,#202e23,#111c27);
}

.r-metric-label {
    color: #aabac9 !important;
    font-size: 10px;
    letter-spacing: 1.3px;
    margin-bottom: 13px;
}

.r-metric-value {
    color: #edf3f8 !important;
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1.2;
}

.r-metric.featured .r-metric-value {
    color: #c3f36b !important;
}

.r-metric-note {
    color: #98a9ba !important;
    font-size: 11px;
    line-height: 1.6;
    margin-top: 10px;
}

.r-chart-title {
    color: #edf3f8 !important;
    font-size: 16px;
    font-weight: 650;
    margin-top: 22px;
}

.r-chart-note {
    color: #98a9ba !important;
    font-size: 12px;
    margin: 5px 0 10px;
    line-height: 1.7;
}

@media(max-width:900px) {
    .block-container {
        padding: 1.3rem 1.2rem 2rem;
    }
    .r-topnote {
        display: none;
    }
    .r-hero-title {
        font-size: 39px;
    }
    .r-preview {
        margin-top: 8px;
        padding: 20px;
    }
    .r-feature {
        min-height: 0;
    }
}
</style>
"""


def markup(content):
    st.markdown(content, unsafe_allow_html=True)


def escaped(value):
    return html.escape(str(value), quote=True)


@st.cache_data
def make_sample():
    rng = np.random.default_rng(42)
    count = 1260

    volatility = np.full(count, 0.009)
    volatility[320:435] = 0.021
    volatility[800:930] = 0.016

    increments = rng.normal(0.0005, volatility)
    increments[[180, 354, 415, 872, 1040]] -= [
        0.04, 0.07, 0.045, 0.06, 0.04
    ]

    return pd.DataFrame({
        "Date": pd.bdate_range("2021-01-04", periods=count),
        "Close": 100 * np.exp(np.cumsum(increments)),
    })


def historical_risk(returns, confidence):
    q = float(returns.quantile(1 - confidence))
    tail = returns[returns <= q]
    return -q, -float(tail.mean()), q, len(tail)


def clean_prices(df, date_col, price_col):
    work = df.copy()

    prices = pd.to_numeric(work[price_col], errors="coerce")
    valid = prices.notna() & np.isfinite(prices) & (prices > 0)
    work[price_col] = prices

    if date_col is not None:
        dates = pd.to_datetime(
            work[date_col],
            errors="coerce",
            utc=True,
            format="mixed",
        )
        work[date_col] = dates.dt.tz_convert(None)
        valid &= dates.notna()

    work = work.loc[valid].copy()

    if date_col is not None:
        work = work.sort_values(date_col, kind="stable")
        if work[date_col].duplicated().any():
            raise ValueError(
                "중복 날짜가 있습니다. 날짜마다 가격을 하나로 "
                "정리한 뒤 업로드해 주세요."
            )

    return work.reset_index(drop=True), len(df) - len(work)


def compute_returns(work, date_col, price_col, log):
    price = work[price_col]

    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        values = (
            np.log(price).diff()
            if log
            else price.pct_change(fill_method=None)
        )

    timeline = (
        work[date_col]
        if date_col
        else pd.Series(np.arange(1, len(work) + 1))
    )

    result = pd.DataFrame({
        "Time": timeline,
        "Price": price,
        "Return": values,
    }).iloc[1:]

    valid = np.isfinite(result["Return"])

    return (
        result.loc[valid].reset_index(drop=True),
        int((~valid).sum()),
    )


def use_sample():
    st.session_state["source"] = "sample"
    st.session_state["screen"] = "analysis"


def use_upload():
    if st.session_state.get("uploaded_csv") is not None:
        st.session_state["source"] = "upload"
        st.session_state["screen"] = "analysis"
    elif st.session_state.get("source") == "upload":
        st.session_state["source"] = None
        st.session_state["screen"] = "home"


def go_home():
    st.session_state["screen"] = "home"


def go_analysis():
    st.session_state["screen"] = "analysis"


def footer():
    markup(
        '<div class="r-footer">'
        '<span>◈ RiskLens · Python / Streamlit / Plotly</span>'
        f'<span>{BUILD} · 학습 및 포트폴리오 프로젝트</span>'
        '</div>'
    )


def preview_markup(sample):
    values = sample["Close"].to_numpy()

    points = values[
        np.linspace(0, len(values) - 1, 160).astype(int)
    ]

    normalized = (
        (points - points.min())
        / max(float(np.ptp(points)), 1e-12)
    )

    pairs = [
        f"{i * 520 / (len(points) - 1):.1f},{145 - val * 125:.1f}"
        for i, val in enumerate(normalized)
    ]

    path = "M " + " L ".join(pairs)
    area = path + " L 520,165 L 0,165 Z"

    rets = sample["Close"].pct_change().dropna()
    var, es, _, _ = historical_risk(rets, 0.95)

    return f"""
<div class="r-preview">
  <div class="r-preview-head">
    <span class="r-eyebrow">SAMPLE WORKSPACE</span>
    <span class="r-demo-label">SYNTHETIC DATA</span>
  </div>
  <div class="r-preview-name">Demo Market Index</div>
  <div class="r-preview-value">
    {values[-1]:,.2f}
    <span class="r-small">INDEX POINTS</span>
  </div>
  <svg class="r-spark" viewBox="0 0 520 165"
       role="img" aria-label="가상 가격 데이터 미리보기">
    <defs>
      <linearGradient id="riskFill" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#c3f36b" stop-opacity="0.20"/>
        <stop offset="100%" stop-color="#c3f36b" stop-opacity="0"/>
      </linearGradient>
    </defs>
    <path d="M 0,30 H 520 M 0,90 H 520 M 0,150 H 520"
          stroke="#2b3b46" stroke-width="1"/>
    <path d="{area}" fill="url(#riskFill)"/>
    <path d="{path}" fill="none" stroke="#c3f36b"
          stroke-width="2.4" stroke-linejoin="round"/>
  </svg>
  <div class="r-axis">
    <span>{sample['Date'].iloc[0]:%Y.%m}</span>
    <span>{sample['Date'].iloc[-1]:%Y.%m}</span>
  </div>
  <div class="r-preview-stats">
    <div>
      <div class="r-preview-stat-label">VaR · 95%</div>
      <div class="r-preview-stat-value accent">{var:.2%}</div>
    </div>
    <div>
      <div class="r-preview-stat-label">Expected Shortfall</div>
      <div class="r-preview-stat-value">{es:.2%}</div>
    </div>
    <div>
      <div class="r-preview-stat-label">수익률 관측치</div>
      <div class="r-preview-stat-value">{len(rets):,}</div>
    </div>
  </div>
  <div class="r-small" style="margin-top:16px">
    실제 시장 데이터가 아닌, 고정된 가상 데이터의 분석 결과입니다.
  </div>
</div>
"""


def render_home():
    left, right = st.columns([1.03, 1], gap="large")

    with left:
        markup("""
<div class="r-hero">
  <div class="r-pill">LESS GUESSWORK. MORE INSIGHT.</div>
  <div class="r-hero-title">
    리스크를 읽는<br><span>더 선명한 방법.</span>
  </div>
  <div class="r-hero-copy">
    가격의 움직임을 넘어, 손실의 가능성까지.<br>
    수익률·VaR·Expected Shortfall을 하나의
    워크스페이스에서 살펴보세요.
  </div>
</div>
""")

        st.button(
            "샘플 데이터 체험하기  →",
            type="primary",
            on_click=use_sample,
            key="hero_sample",
            width="stretch",
        )

        markup(
            '<div class="r-small">'
            '파일 준비 없이 바로 시작 · '
            '내 데이터는 왼쪽에서 CSV 업로드'
            '</div>'
        )

        st.download_button(
            "샘플 CSV 다운로드",
            make_sample().to_csv(index=False).encode("utf-8-sig"),
            "risklens_sample.csv",
            "text/csv",
            width="stretch",
            key="home_sample_download",
        )

    with right:
        markup(preview_markup(make_sample()))

    markup(
        '<div class="r-section-top">'
        '<span class="r-section-title">'
        '숫자를 이해하고, 위험을 발견하세요.</span>'
        '<span class="r-eyebrow">A CLEARER VIEW OF RISK</span>'
        '</div>'
    )

    features = [
        (
            "01 / MEASURE",
            "위험을 숫자로",
            "Historical VaR와 Expected Shortfall로 "
            "손실 분포의 꼬리 영역을 분석합니다.",
        ),
        (
            "02 / EXPLORE",
            "흐름을 한눈에",
            "가격·수익률·Rolling VaR를 인터랙티브 차트로 "
            "비교하고 구간을 확대해 보세요.",
        ),
        (
            "03 / EXPORT",
            "내 데이터로 시작",
            "가격 CSV를 업로드하고 분석에 사용한 "
            "수익률과 위험 지표를 내려받으세요.",
        ),
    ]

    for col, (number, title, text) in zip(
        st.columns(3, gap="medium"), features
    ):
        with col:
            markup(
                '<div class="r-feature">'
                f'<div class="r-feature-number">{number}</div>'
                f'<div class="r-feature-title">{title}</div>'
                f'<div class="r-feature-copy">{text}</div>'
                '</div>'
            )

    markup(
        '<div class="r-guide">'
        '<span>QUICK START</span>　'
        '샘플 또는 CSV 선택　→　신뢰수준·분석 구간 설정　'
        '→　차트 탐색 및 결과 다운로드'
        '</div>'
    )


def style_figure(fig, height=340, percent=False):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(
            color=TEXT,
            family="Segoe UI, Malgun Gothic, sans-serif",
            size=12,
        ),
        height=height,
        margin=dict(l=16, r=24, t=40, b=20),
        hovermode="x unified",
        dragmode="zoom",
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#203246",
            font_color=TEXT,
            bordercolor="#41586f",
        ),
        xaxis=dict(
            gridcolor="#243443",
            zerolinecolor="#344658",
            title=None,
        ),
        yaxis=dict(
            gridcolor="#243443",
            zerolinecolor="#344658",
            title=None,
        ),
        legend=dict(orientation="h", y=1.15, x=0),
    )

    if percent:
        fig.update_yaxes(tickformat=".1%")

    return fig


def chart_title(title, note):
    markup(
        f'<div class="r-chart-title">{escaped(title)}</div>'
        f'<div class="r-chart-note">{escaped(note)}</div>'
    )


def show_chart(fig, key):
    st.plotly_chart(
        fig,
        theme=None,
        width="stretch",
        key=key,
        config={"displaylogo": False, "scrollZoom": False},
    )


def metric(label, value, note, featured=False):
    extra = " featured" if featured else ""

    markup(
        f'<div class="r-metric{extra}">'
        f'<div class="r-metric-label">{escaped(label)}</div>'
        f'<div class="r-metric-value">{escaped(value)}</div>'
        f'<div class="r-metric-note">{escaped(note)}</div>'
        '</div>'
    )


def read_uploaded(uploaded):
    if uploaded is None:
        raise ValueError(
            "왼쪽에서 CSV를 업로드하거나 샘플 데이터를 선택해 주세요."
        )

    if uploaded.size > 20 * 1024 * 1024:
        raise ValueError("CSV는 20MB 이하 파일을 사용해 주세요.")

    content = uploaded.getvalue()

    try:
        frame = pd.read_csv(
            io.BytesIO(content), encoding="utf-8-sig"
        )
    except UnicodeDecodeError:
        try:
            frame = pd.read_csv(
                io.BytesIO(content), encoding="cp949"
            )
        except UnicodeDecodeError as exc:
            raise ValueError(
                "CSV를 UTF-8 형식으로 저장한 뒤 다시 업로드해 주세요."
            ) from exc

    if frame.empty or len(frame.columns) < 1:
        raise ValueError("CSV에 분석할 데이터가 없습니다.")

    dataset_id = hashlib.sha256(content).hexdigest()[:12]
    return frame, dataset_id


def render_analysis(uploaded):
    source = st.session_state.get("source")

    try:
        if source == "sample":
            raw = make_sample()
            dataset_id = "sample_v2"
            source_name = "가상 시장 샘플"
        else:
            raw, dataset_id = read_uploaded(uploaded)
            source_name = uploaded.name
    except (
        ValueError,
        pd.errors.ParserError,
        pd.errors.EmptyDataError,
    ) as exc:
        st.error(str(exc))
        return

    cols = list(raw.columns)

    date_guess = next(
        (
            c for c in cols
            if c.lower() in {
                "date", "datetime", "timestamp", "날짜", "일자"
            }
        ),
        None,
    )

    price_guess = next(
        (
            c for c in cols
            if c.lower() in {
                "close", "adj close", "adj_close",
                "price", "종가", "가격",
            }
        ),
        None,
    )

    if price_guess is None:
        price_guess = next(
            (
                c for c in cols
                if c != date_guess
                and pd.api.types.is_numeric_dtype(raw[c])
            ),
            cols[0],
        )

    with st.sidebar:
        st.divider()

        markup(
            '<div class="r-section-label">'
            '02 / ANALYSIS SETTINGS</div>'
        )

        date_options = ["(날짜 없음)"] + cols

        date_choice = st.selectbox(
            "날짜 열",
            date_options,
            index=(
                date_options.index(date_guess)
                if date_guess else 0
            ),
            key=f"date_{dataset_id}",
        )

        price_col = st.selectbox(
            "가격 열",
            cols,
            index=cols.index(price_guess),
            key=f"price_{dataset_id}",
        )

        return_type = st.radio(
            "수익률 방식",
            ["단순 수익률", "로그 수익률"],
            horizontal=True,
            key="return_type",
        )

        confidence = st.selectbox(
            "신뢰수준",
            [0.95, 0.99],
            format_func=lambda x: f"{x:.0%}",
            key="confidence",
        )

        window = int(st.number_input(
            "이동 구간 (관측치 수)",
            min_value=0,
            value=0,
            step=20,
            key="window",
            help=(
                "0은 전체 기간입니다. 2 이상이면 최근 N개 "
                "수익률로 위험을 추정하고 Rolling VaR도 표시합니다."
            ),
        ))

        st.caption(
            "0 = 전체 기간 · 일별 데이터라면 "
            "1개 관측 구간은 하루입니다."
        )

    date_col = (
        None if date_choice == "(날짜 없음)" else date_choice
    )

    if date_col == price_col:
        st.error("날짜 열과 가격 열을 다르게 선택해 주세요.")
        return

    try:
        work, removed = clean_prices(raw, date_col, price_col)
    except ValueError as exc:
        st.error(str(exc))
        return

    if len(work) < 3:
        st.error(
            "유효한 양수 가격이 최소 3개 필요합니다. "
            "가격 열을 확인해 주세요."
        )
        return

    result, return_removed = compute_returns(
        work,
        date_col,
        price_col,
        return_type == "로그 수익률",
    )

    if len(result) < 2:
        st.error(
            "계산 가능한 유한 수익률이 부족합니다. "
            "가격 값의 범위를 확인해 주세요."
        )
        return

    if window == 1 or window > len(result):
        st.error(
            f"이동 구간은 0(전체 기간) 또는 "
            f"2~{len(result):,} 사이로 설정해 주세요."
        )
        return

    rets = result["Return"]
    selected = rets if window == 0 else rets.iloc[-window:]

    var, es, q, tail_count = historical_risk(
        selected, confidence
    )

    period_label = (
        "전체 기간"
        if window == 0
        else f"최근 {window:,}개 관측 구간"
    )

    markup(
        '<div class="r-eyebrow">YOUR RISK WORKSPACE</div>'
        '<div class="r-dashboard-title">'
        '손실의 가능성까지, 한눈에.</div>'
        '<div class="r-dashboard-copy">'
        f'{escaped(source_name)}　/　{escaped(price_col)}　/　'
        f'{escaped(return_type)}　/　'
        f'{period_label} · {confidence:.0%}</div>'
    )

    if source == "sample":
        markup(
            '<div class="r-banner">'
            'DEMO DATA　·　고정된 난수로 생성한 가상 가격입니다. '
            '홈의 미리보기와 같은 데이터를 사용하며 '
            '실제 종목·지수의 성과를 의미하지 않습니다.'
            '</div>'
        )

    if removed:
        st.warning(
            f"날짜가 유효하지 않거나 가격이 "
            f"0·음수·결측·무한대인 {removed:,}개 행을 제외했습니다. "
            "제외된 행 전후의 수익률은 더 긴 간격을 포함할 수 있습니다."
        )

    if return_removed:
        st.warning(
            f"계산 결과가 유한하지 않은 수익률 "
            f"{return_removed:,}개를 제외했습니다."
        )

    cards = st.columns(4, gap="small")

    with cards[0]:
        metric(
            "HISTORICAL VAR",
            f"{var:.2%}",
            f"{confidence:.0%} · 1개 관측 구간 기준",
            featured=True,
        )

    with cards[1]:
        metric(
            "EXPECTED SHORTFALL",
            f"{es:.2%}",
            f"꼬리 영역 {tail_count:,}개 수익률의 평균 손실",
        )

    with cards[2]:
        metric(
            "RETURN VOLATILITY",
            f"{selected.std():.2%}",
            "선택 구간 수익률의 표본 표준편차",
        )

    with cards[3]:
        metric(
            "OBSERVATIONS",
            f"{len(selected):,}",
            f"위험 추정용 / 전체 수익률 {len(rets):,}개",
        )

    if tail_count < 5:
        st.caption(
            "꼬리 관측치가 5개 미만입니다. 구간을 늘리면 "
            "더 많은 관측치로 위험을 추정할 수 있습니다."
        )

    market_tab, tail_tab, data_tab = st.tabs([
        "시장 흐름", "손실 분포", "데이터 및 방법론"
    ])

    with market_tab:
        chart_title(
            "가격 추이",
            "가격 자체는 신뢰수준을 바꿔도 동일합니다. "
            "드래그해 구간을 확대할 수 있습니다.",
        )

        times = (
            work[date_col]
            if date_col
            else np.arange(1, len(work) + 1)
        )

        fig = go.Figure(go.Scatter(
            x=times,
            y=work[price_col],
            mode="lines",
            name="가격",
            line=dict(color=LIME, width=2),
            hovertemplate="%{y:,.2f}<extra>가격</extra>",
        ))

        show_chart(style_figure(fig), "price_chart")

        chart_title(
            "수익률과 VaR 기준선",
            f"수익률은 그대로, 붉은 점선은 {period_label}의 "
            f"{confidence:.0%} 신뢰수준에 따라 이동합니다.",
        )

        fig = go.Figure(go.Scatter(
            x=result["Time"],
            y=rets,
            mode="lines",
            name="수익률",
            line=dict(color="#7ab8d0", width=1.2),
            hovertemplate="%{y:.2%}<extra>수익률</extra>",
        ))

        fig.add_hline(
            y=q,
            line_color=CORAL,
            line_dash="dash",
            annotation_text=f"VaR {confidence:.0%} 기준",
            annotation_font_color=CORAL,
            annotation_position="top left",
        )

        show_chart(
            style_figure(fig, percent=True),
            "returns_chart",
        )

        if window > 0:
            rolling = (
                -rets.rolling(window).quantile(1 - confidence)
            )

            chart_title(
                "Rolling VaR",
                f"매 관측 시점까지의 최근 {window:,}개 수익률로 "
                f"추정한 {confidence:.0%} VaR입니다.",
            )

            fig = go.Figure(go.Scatter(
                x=result["Time"],
                y=rolling,
                name="Rolling VaR",
                mode="lines",
                line=dict(color=LIME, width=2),
                hovertemplate=(
                    "%{y:.2%}<extra>Rolling VaR</extra>"
                ),
            ))

            show_chart(
                style_figure(fig, percent=True),
                "rolling_chart",
            )

    with tail_tab:
        chart_title(
            "수익률의 꼬리를 들여다보세요.",
            f"{period_label}의 분포입니다. 막대는 수익률 분포, "
            f"붉은 점선은 하위 {1-confidence:.0%} 분위수입니다.",
        )

        fig = go.Figure(go.Histogram(
            x=selected,
            nbinsx=45,
            marker_color="#739b88",
            name="수익률",
            hovertemplate=(
                "수익률 %{x:.2%}<br>"
                "빈도 %{y}<extra></extra>"
            ),
        ))

        fig.add_vline(
            x=q,
            line_color=CORAL,
            line_dash="dash",
            line_width=2,
            annotation_text=f"VaR {confidence:.0%}",
            annotation_font_color=CORAL,
            annotation_position="top left",
        )

        fig = style_figure(fig, height=410)
        fig.update_layout(bargap=0.08, hovermode="closest")
        fig.update_xaxes(tickformat=".1%", title="수익률")
        fig.update_yaxes(title="관측 빈도")

        show_chart(fig, "distribution_chart")

        markup(
            '<div class="r-guide">'
            '<span>READ THE CHART</span>　'
            f'붉은 선에 해당하는 수익률은 {q:.2%}입니다. '
            f'그 이하 {tail_count:,}개 관측치의 평균에 '
            f'−1을 곱하면 Expected Shortfall '
            f'{es:.2%}가 됩니다.</div>'
        )

    with data_tab:
        chart_title(
            "분석 데이터",
            "정제 후 가격 데이터의 첫 100개 행입니다.",
        )

        st.dataframe(
            work.head(100),
            width="stretch",
            hide_index=True,
        )

        dl1, dl2 = st.columns(2)

        with dl1:
            st.download_button(
                "수익률 CSV 다운로드  ↓",
                result.to_csv(index=False).encode("utf-8-sig"),
                "risklens_returns.csv",
                "text/csv",
                width="stretch",
            )

        with dl2:
            summary = pd.DataFrame([{
                "confidence": confidence,
                "return_type": return_type,
                "window": window,
                "observations": len(selected),
                "historical_var": var,
                "expected_shortfall": es,
                "return_std": selected.std(),
                "tail_observations": tail_count,
            }])

            st.download_button(
                "위험 지표 CSV 다운로드  ↓",
                summary.to_csv(index=False).encode("utf-8-sig"),
                "risklens_metrics.csv",
                "text/csv",
                width="stretch",
            )

        with st.expander("계산 방법과 해석", expanded=True):
            st.markdown("""
**수익률**

- 단순 수익률: `현재 가격 / 이전 가격 − 1`
- 로그 수익률: `ln(현재 가격) − ln(이전 가격)`

**Historical VaR / Expected Shortfall**

- `q = 수익률의 하위 (1 − 신뢰수준) 분위수` (선형 보간)
- `VaR = −q`
- `ES = −평균(수익률 ≤ q)` — 분위수 경계와 같은 값도 포함합니다.
- 로그 수익률을 선택하면 위험 지표도 로그 수익률 기준이며,
  단순 손실률로 변환하지 않습니다.

**관측 간격과 이동 구간**

- 위험 지표는 입력 데이터의 관측 간격을 따릅니다.
  일별 가격이라면 일별 위험입니다.
- 날짜가 없으면 CSV 행 순서대로 계산하며,
  날짜가 있으면 오름차순으로 정렬합니다.
- 이동 구간 0은 전체 기간, N은 최근 N개 수익률로
  요약 지표를 계산합니다.
- Rolling VaR는 각 시점까지의 최근 N개 수익률로 계산하며,
  미래 예측이나 백테스트 결과가 아닙니다.

**해석 범위**

- 손실을 양수로 표현하는 부호 규칙입니다.
  데이터의 하위 분위수가 양수라면 VaR는 음수일 수 있습니다.
- VaR는 최대 손실이 아닙니다.
  과거의 경험 분포가 미래 손실을 보장하지 않습니다.
- 샘플은 변동성이 다른 구간을 포함한 가상 가격이며
  실제 시장 데이터가 아닙니다.
""")


def main():
    markup(CSS)

    st.session_state.setdefault("screen", "home")
    st.session_state.setdefault("source", None)

    with st.sidebar:
        markup(
            '<div class="r-sidebrand">'
            '<span>◈</span> RiskLens</div>'
            '<div class="r-side-note">'
            'MARKET RISK STUDIO<br>'
            '데이터로 살펴보는 손실의 가능성</div>'
        )

        if st.session_state["screen"] == "analysis":
            st.button(
                "← 홈으로",
                on_click=go_home,
                width="stretch",
            )
        elif st.session_state["source"] is not None:
            st.button(
                "분석 화면으로 →",
                on_click=go_analysis,
                width="stretch",
            )

        markup(
            '<div class="r-section-label">'
            '01 / DATA SOURCE</div>'
        )

        st.button(
            "샘플 데이터 체험하기 →",
            on_click=use_sample,
            type="primary",
            width="stretch",
            key="sidebar_sample",
        )

        uploaded = st.file_uploader(
            "내 데이터로 분석",
            type=["csv"],
            key="uploaded_csv",
            on_change=use_upload,
        )

        if (
            uploaded is not None
            and st.session_state["source"] != "upload"
        ):
            st.button(
                "업로드한 CSV로 분석 →",
                on_click=use_upload,
                width="stretch",
            )

        st.caption("CSV · 20MB 이하 · 권장 열: Date, Close")

        if st.session_state["screen"] == "home":
            st.divider()

            markup(
                '<div class="r-section-label">'
                'BUILT TO EXPLORE</div>'
                '<div class="r-side-note">'
                'Historical VaR / CVaR<br>'
                'Rolling Risk Analysis<br>'
                'Interactive Charts<br>'
                'CSV Export</div>'
            )

            st.caption(
                "샘플을 선택하면 분석 설정이 나타납니다."
            )

        st.caption(BUILD)

    markup(
        '<div class="r-topbar">'
        '<div class="r-brand">'
        '<span>◈</span>RiskLens</div>'
        '<div class="r-topnote">'
        'MARKET RISK, MADE VISIBLE.</div>'
        '</div>'
    )

    if st.session_state["screen"] == "home":
        render_home()
    else:
        render_analysis(uploaded)

    footer()


if __name__ == "__main__":
    main()