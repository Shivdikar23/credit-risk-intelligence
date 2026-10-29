
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# =====================================================
# 1. CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CreditIQ | Risk Intelligence",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

FILES = {
    "loans": "Loan_Data_PowerBI.csv",
    "original": "Loan_default.csv",
    "models": "Model_Comparison_PowerBI.csv",
    "risk": "Risk_Segmentation_PowerBI.csv",
    "shap": "SHAP_Feature_Importance_PowerBI.csv",
    "sql": "SQL_Risk_Profile_PowerBI.csv",
}

NAVY = "#142744"
BLUE = "#3478F6"
CYAN = "#27B6C8"
GREEN = "#159B72"
RED = "#D95362"
AMBER = "#E9A23B"
PURPLE = "#8267D8"
MUTED = "#78879B"

SCORE_ORDER = ["Poor", "Fair", "Good", "Very Good", "Excellent"]
SCORE_COLORS = {
    "Poor": RED,
    "Fair": AMBER,
    "Good": BLUE,
    "Very Good": CYAN,
    "Excellent": GREEN,
    "Unknown": MUTED,
}


# =====================================================
# 2. PROFESSIONAL FINTECH UI + FLOATING MONEY
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #F5F7FB;
    color: #142744;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(245,247,251,0.9);
}

[data-testid="stSidebar"] {
    background: #111E33;
    border-right: 1px solid #263750;
}

[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem;
}

[data-testid="stSidebar"] * {
    color: #EAF0FA;
}

.brand {
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #FFFFFF;
}

.brand span {
    color: #72A7FF;
}

.brand-sub {
    color: #91A6C3;
    font-size: 0.65rem;
    letter-spacing: 2px;
    margin: 4px 0 30px;
}

.nav-label {
    color: #8295B1;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin: 12px 0;
}

[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    min-height: 46px;
    text-align: left;
    justify-content: flex-start;
    background: transparent;
    border: 1px solid transparent;
    color: #B7C5D9;
    border-radius: 9px;
    padding: 11px 13px;
    font-size: 0.84rem;
    font-weight: 500;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] div.stButton > button:hover {
    background: #223651;
    color: #FFFFFF;
    border-color: #314966;
}

[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: #244A80;
    color: #FFFFFF;
    border: 1px solid #477BC0;
    font-weight: 700;
}

.sidebar-status {
    margin-top: 30px;
    padding: 14px;
    border: 1px solid #2B405B;
    border-radius: 10px;
    color: #DCE6F5;
    font-size: 0.77rem;
    line-height: 1.8;
}

.page-eyebrow {
    color: #3478F6;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 1.8px;
}

.page-title {
    color: #142744;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 4px 0;
}

.page-description {
    color: #78879B;
    font-size: 0.88rem;
    margin-bottom: 22px;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E6EBF2;
    border-top: 3px solid var(--accent, #3478F6);
    border-radius: 13px;
    padding: 18px;
    min-height: 118px;
    box-shadow: 0 4px 14px rgba(20,39,68,0.04);
}

.metric-label {
    color: #78879B;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.metric-value {
    color: #142744;
    font-size: 1.65rem;
    font-weight: 800;
    margin-top: 10px;
    line-height: 1.2;
    overflow-wrap: anywhere;
}

.metric-note {
    color: #8996A8;
    font-size: 0.7rem;
    margin-top: 7px;
}

.section-heading {
    color: #142744;
    font-size: 1rem;
    font-weight: 750;
    margin-top: 8px;
}

.section-note {
    color: #78879B;
    font-size: 0.76rem;
    margin-bottom: 10px;
}

div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E6EBF2;
    border-radius: 12px;
    padding: 5px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #E6EBF2;
    border-radius: 10px;
}

.footer {
    text-align: center;
    padding: 24px 0 6px;
    color: #8A97A9;
    font-size: 0.7rem;
}

/* Subtle decorative floating currency symbols */
.money-layer {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}

.money {
    position: absolute;
    bottom: -90px;
    color: #3478F6;
    opacity: 0.10;
    font-weight: 800;
    animation: moneyFloat 22s linear infinite;
    user-select: none;
}

.money:nth-child(1) { left: 12%; font-size: 38px; animation-delay: -3s; }
.money:nth-child(2) { left: 31%; font-size: 24px; animation-delay: -13s; }
.money:nth-child(3) { left: 55%; font-size: 45px; animation-delay: -8s; }
.money:nth-child(4) { left: 75%; font-size: 29px; animation-delay: -18s; }
.money:nth-child(5) { left: 90%; font-size: 35px; animation-delay: -5s; }

@keyframes moneyFloat {
    0%   { transform: translateY(0) rotate(-12deg); opacity: 0; }
    12%  { opacity: 0.09; }
    80%  { opacity: 0.07; }
    100% { transform: translateY(-115vh) rotate(20deg); opacity: 0; }
}

@media (prefers-reduced-motion: reduce) {
    .money { animation: none; display: none; }
}
</style>

<div class="money-layer" aria-hidden="true">
    <span class="money">$</span>
    <span class="money">₹</span>
    <span class="money">＄</span>
    <span class="money">₹</span>
    <span class="money">$</span>
</div>
""", unsafe_allow_html=True)


# =====================================================
# 3. LOAD DATASETS
# =====================================================

@st.cache_data(show_spinner="Loading credit risk datasets...")
def load_csv(filename):
    path = DATA / filename
    if not path.exists():
        return None
    try:
        return pd.read_csv(path, low_memory=False)
    except (OSError, ValueError, pd.errors.ParserError):
        return None


loans = load_csv(FILES["loans"])
if loans is None:
    loans = load_csv(FILES["original"])

models = load_csv(FILES["models"])
risk_data = load_csv(FILES["risk"])
shap_data = load_csv(FILES["shap"])
sql_data = load_csv(FILES["sql"])


# =====================================================
# 4. HELPER FUNCTIONS
# =====================================================

def num(df, column):
    if df is None or column not in df.columns:
        return pd.Series(dtype=float, index=df.index if df is not None else None)
    return pd.to_numeric(df[column], errors="coerce")


def money(value):
    return "N/A" if pd.isna(value) else f"{value:,.0f}"


def pct(value):
    return "N/A" if pd.isna(value) else f"{value:.2f}%"


def default_rate(df):
    if "Default" not in df.columns:
        return np.nan
    values = num(df, "Default")
    values = values[values.isin([0, 1])]
    return values.mean() * 100 if len(values) else np.nan


def score_band(score):
    if pd.isna(score):
        return "Unknown"
    if score < 580:
        return "Poor"
    if score < 670:
        return "Fair"
    if score < 740:
        return "Good"
    if score < 800:
        return "Very Good"
    return "Excellent"


def card(label, value, note, accent=BLUE):
    st.markdown(f"""
    <div class="metric-card" style="--accent:{accent}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def heading(title, note=""):
    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True,
    )
    if note:
        st.markdown(
            f'<div class="section-note">{note}</div>',
            unsafe_allow_html=True,
        )


def style_chart(fig, height=340, legend=False):
    fig.update_layout(
        height=height,
        margin=dict(l=18, r=18, t=30, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, Arial", color=NAVY, size=11),
        showlegend=legend,
        hoverlabel=dict(bgcolor=NAVY, font_color="white"),
    )
    fig.update_xaxes(showgrid=False, automargin=True)
    fig.update_yaxes(
        showgrid=True, gridcolor="#EDF1F7",
        zeroline=False, automargin=True
    )
    return fig


def show_table(df, height=330):
    st.dataframe(
        df, use_container_width=True, hide_index=True, height=height
    )


# =====================================================
# 5. SIDEBAR NAVIGATION - NO FILTERS
# =====================================================

PAGES = {
    "Executive Overview": "▦",
    "Credit Score Analytics": "◉",
    "Loan Portfolio": "▤",
    "Borrower Risk": "♙",
    "Model Performance": "⌘",
    "Explainable AI": "⌁",
    "Data Explorer": "▧",
}

with st.sidebar:
    st.markdown(
        '<div class="brand">CREDIT<span>IQ</span></div>'
        '<div class="brand-sub">RISK INTELLIGENCE PLATFORM</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="nav-label">WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Executive Overview"

    for name, symbol in PAGES.items():
        if st.button(
            f"{symbol}    {name}",
            key=f"nav_{name}",
            use_container_width=True,
            type="primary" if st.session_state.active_page == name else "secondary",
        ):
            st.session_state.active_page = name
            st.rerun()

    st.markdown(
        '<div class="sidebar-status">'
        '<span style="color:#37C995">●</span> Analytics workspace'
        '<br><span style="color:#91A6C3">Loan portfolio monitoring</span>'
        '</div>',
        unsafe_allow_html=True,
    )

page = st.session_state.active_page

if loans is None or loans.empty:
    st.error("Could not load the loan dataset. Check the data folder.")
    st.stop()

# No filters: every page uses the full loan dataset.
df = loans.copy()
df["Score Band"] = num(df, "CreditScore").apply(score_band) if "CreditScore" in df.columns else "Unknown"

defaults = num(df, "Default") if "Default" in df.columns else pd.Series(dtype=float)
valid_defaults = defaults[defaults.isin([0, 1])]
default_count = int((valid_defaults == 1).sum()) if len(valid_defaults) else np.nan
default_pct = valid_defaults.mean() * 100 if len(valid_defaults) else np.nan
avg_score = num(df, "CreditScore").mean()
avg_loan = num(df, "LoanAmount").mean()
avg_income = num(df, "Income").mean()


# =====================================================
# 6. PAGE HEADER
# =====================================================

DESCRIPTIONS = {
    "Executive Overview": ("PORTFOLIO MONITORING", "A high-level view of loans, credit scores and observed defaults."),
    "Credit Score Analytics": ("SCORE INTELLIGENCE", "Explore score distributions, illustrative score bands and observed outcomes."),
    "Loan Portfolio": ("LENDING ANALYTICS", "Analyze loan amounts, borrower income and interest rate patterns."),
    "Borrower Risk": ("BORROWER INTELLIGENCE", "Review borrower characteristics and available risk summaries."),
    "Model Performance": ("MACHINE LEARNING", "Compare evaluation metrics recorded in your model comparison dataset."),
    "Explainable AI": ("MODEL INTERPRETABILITY", "Explore recorded SHAP feature importance values."),
    "Data Explorer": ("DATA QUALITY", "Inspect the underlying records and download CSV data."),
}

eyebrow, description = DESCRIPTIONS[page]
st.markdown(
    f'<div class="page-eyebrow">{eyebrow}</div>'
    f'<div class="page-title">{page}</div>'
    f'<div class="page-description">{description}</div>',
    unsafe_allow_html=True,
)


# =====================================================
# 7. EXECUTIVE OVERVIEW
# =====================================================

if page == "Executive Overview":

    cols = st.columns(4, gap="medium")
    values = [
        ("TOTAL LOANS", f"{len(df):,}", "Loan records", BLUE),
        ("OBSERVED DEFAULTS", f"{default_count:,}" if pd.notna(default_count) else "N/A", "Default = 1", RED),
        ("DEFAULT RATE", pct(default_pct), "Valid binary labels", AMBER),
        ("AVERAGE CREDIT SCORE", f"{avg_score:.0f}" if pd.notna(avg_score) else "N/A", "Observed score average", GREEN),
    ]
    for col, args in zip(cols, values):
        with col:
            card(*args)

    st.write("")
    left, right = st.columns(2, gap="medium")

    with left:
        heading("Default composition", "Share of valid default labels")
        if len(valid_defaults):
            outcomes = valid_defaults.map({0: "Non-default", 1: "Default"}).value_counts()
            chart = px.pie(
                names=outcomes.index, values=outcomes.values, hole=0.67,
                color=outcomes.index,
                color_discrete_map={"Non-default": BLUE, "Default": RED},
            )
            chart.update_traces(
                textinfo="percent",
                hovertemplate="%{label}<br>Records: %{value:,}<extra></extra>",
            )
            chart.add_annotation(
                text=f"{len(valid_defaults):,}<br><sup>records</sup>",
                x=.5, y=.5, showarrow=False, font=dict(size=18, color=NAVY),
            )
            st.plotly_chart(style_chart(chart), use_container_width=True)
        else:
            st.info("No valid binary default labels found.")

    with right:
        heading("Credit score distribution", "Borrower count by score")
        scores = num(df, "CreditScore").dropna()
        if not scores.empty:
            chart = px.histogram(
                x=scores, nbins=30, color_discrete_sequence=[BLUE],
                labels={"x": "Credit score", "y": "Borrower count"},
            )
            st.plotly_chart(style_chart(chart), use_container_width=True)
        else:
            st.info("Credit score data unavailable.")

    left, right = st.columns(2, gap="medium")

    with left:
        heading("Default rate by score band", "Observed rates, not predictions")
        temp = df.copy()
        temp["Default"] = num(temp, "Default") if "Default" in temp.columns else np.nan
        temp = temp[temp["Default"].isin([0, 1]) & (temp["Score Band"] != "Unknown")]
        if not temp.empty:
            result = temp.groupby("Score Band", observed=False)["Default"].agg(["mean", "count"]).reset_index()
            result["Default Rate (%)"] = result["mean"] * 100
            result["Score Band"] = pd.Categorical(result["Score Band"], SCORE_ORDER, ordered=True)
            result = result.sort_values("Score Band")
            chart = px.bar(
                result, x="Score Band", y="Default Rate (%)",
                color="Score Band", color_discrete_map=SCORE_COLORS,
                category_orders={"Score Band": SCORE_ORDER},
                custom_data=["count"],
            )
            chart.update_traces(
                hovertemplate="%{x}<br>Default rate: %{y:.2f}%"
                              "<br>Records: %{customdata[0]:,}<extra></extra>"
            )
            chart.update_yaxes(title="Default rate (%)", ticksuffix="%")
            st.plotly_chart(style_chart(chart), use_container_width=True)
        else:
            st.info("Required score or default data is unavailable.")

    with right:
        heading("Loan purpose breakdown", "Number of loans by purpose")
        if "LoanPurpose" in df.columns:
            purpose = df["LoanPurpose"].fillna("Unknown").value_counts().reset_index()
            purpose.columns = ["Loan Purpose", "Records"]
            chart = px.bar(
                purpose.sort_values("Records"), x="Records", y="Loan Purpose",
                orientation="h", color_discrete_sequence=[CYAN],
            )
            chart.update_xaxes(title="Number of loans")
            st.plotly_chart(style_chart(chart), use_container_width=True)
        else:
            st.info("LoanPurpose column unavailable.")

    heading("Portfolio indicators", "Descriptive statistics")
    summary = pd.DataFrame({
        "Indicator": ["Average loan amount", "Average income", "Average interest rate", "Average DTI ratio"],
        "Value": [
            money(avg_loan), money(avg_income),
            f"{num(df, 'InterestRate').mean():.2f}%" if num(df, "InterestRate").notna().any() else "N/A",
            f"{num(df, 'DTIRatio').mean():.3f}" if num(df, "DTIRatio").notna().any() else "N/A",
        ],
    })
    show_table(summary, 230)


# =====================================================
# 8. CREDIT SCORE ANALYTICS
# =====================================================

elif page == "Credit Score Analytics":

    scores = num(df, "CreditScore").dropna()
    a, b, c = st.columns(3)

    with a:
        card("AVERAGE SCORE", f"{scores.mean():.0f}" if len(scores) else "N/A", "Mean score", BLUE)
    with b:
        card("MEDIAN SCORE", f"{scores.median():.0f}" if len(scores) else "N/A", "50th percentile", CYAN)
    with c:
        card("VALID SCORES", f"{len(scores):,}", "Non-missing values", GREEN)

    left, right = st.columns(2, gap="medium")

    with left:
        heading("Score distribution", "Histogram of observed scores")
        if len(scores):
            chart = px.histogram(
                x=scores, nbins=35, color_discrete_sequence=[BLUE],
                labels={"x": "Credit score", "y": "Borrower count"},
            )
            st.plotly_chart(style_chart(chart), use_container_width=True)
        else:
            st.info("No score values available.")

    with right:
        heading("Borrowers by score band", "Illustrative score ranges")
        counts = df[df["Score Band"] != "Unknown"]["Score Band"].value_counts().reindex(SCORE_ORDER, fill_value=0).reset_index()
        counts.columns = ["Score Band", "Borrowers"]
        chart = px.bar(
            counts, x="Score Band", y="Borrowers",
            color="Score Band", color_discrete_map=SCORE_COLORS,
            category_orders={"Score Band": SCORE_ORDER},
        )
        st.plotly_chart(style_chart(chart), use_container_width=True)

    heading("Default rate by score band", "Valid binary default labels only")
    if "Default" in df.columns:
        temp = df.copy()
        temp["Default"] = num(temp, "Default")
        temp = temp[temp["Default"].isin([0, 1]) & (temp["Score Band"] != "Unknown")]
        if not temp.empty:
            result = temp.groupby("Score Band", observed=False)["Default"].agg(["mean", "count"]).reset_index()
            result["Default Rate (%)"] = result["mean"] * 100
            result["Score Band"] = pd.Categorical(result["Score Band"], SCORE_ORDER, ordered=True)
            result = result.sort_values("Score Band")
            chart = px.bar(
                result, x="Score Band", y="Default Rate (%)",
                color="Score Band", color_discrete_map=SCORE_COLORS,
                category_orders={"Score Band": SCORE_ORDER},
                custom_data=["count"],
            )
            chart.update_traces(hovertemplate="%{x}<br>Rate: %{y:.2f}%<br>Records: %{customdata[0]:,}<extra></extra>")
            chart.update_yaxes(title="Default rate (%)", ticksuffix="%")
            st.plotly_chart(style_chart(chart), use_container_width=True)
            show_table(result[["Score Band", "count", "Default Rate (%)"]].rename(columns={"count": "Valid records"}))
        else:
            st.info("No valid outcomes available.")

    st.info(
        "Illustrative FICO-style score bands: Poor (<580), Fair (580–669), "
        "Good (670–739), Very Good (740–799), Excellent (800+). "
        "These are not an official bureau score or lending policy."
    )


# =====================================================
# 9. LOAN PORTFOLIO
# =====================================================

elif page == "Loan Portfolio":

    a, b, c = st.columns(3)
    with a:
        card("AVERAGE LOAN", money(avg_loan), "Mean loan amount", BLUE)
    with b:
        card("AVERAGE INCOME", money(avg_income), "Mean income", CYAN)
    with c:
        interest = num(df, "InterestRate").mean()
        card("AVERAGE INTEREST", f"{interest:.2f}%" if pd.notna(interest) else "N/A", "Recorded rate", AMBER)

    left, right = st.columns(2, gap="medium")

    with left:
        heading("Loan amount distribution", "Distribution across all records")
        amounts = num(df, "LoanAmount").dropna()
        if len(amounts):
            chart = px.histogram(x=amounts, nbins=35, color_discrete_sequence=[BLUE], labels={"x": "Loan amount", "y": "Loans"})
            st.plotly_chart(style_chart(chart), use_container_width=True)
        else:
            st.info("Loan amounts unavailable.")

    with right:
        heading("Average loan by purpose", "Mean amount per loan purpose")
        if {"LoanPurpose", "LoanAmount"}.issubset(df.columns):
            temp = df[["LoanPurpose", "LoanAmount"]].copy()
            temp["LoanAmount"] = num(temp, "LoanAmount")
            result = temp.groupby("LoanPurpose", dropna=False)["LoanAmount"].mean().reset_index().sort_values("LoanAmount")
            chart = px.bar(result, x="LoanAmount", y="LoanPurpose", orientation="h", color_discrete_sequence=[CYAN])
            chart.update_xaxes(title="Average loan amount")
            st.plotly_chart(style_chart(chart), use_container_width=True)
        else:
            st.info("Required columns unavailable.")

    left, right = st.columns(2, gap="medium")

    with left:
        heading("Income vs loan amount", "Each point represents one record")
        if {"Income", "LoanAmount"}.issubset(df.columns):
            temp = df[["Income", "LoanAmount"]].copy()
            temp["Income"] = num(temp, "Income")
            temp["LoanAmount"] = num(temp, "LoanAmount")
            temp = temp.dropna()
            if not temp.empty:
                temp = temp.sample(min(len(temp), 3000), random_state=42)
                chart = px.scatter(temp, x="Income", y="LoanAmount", opacity=.6, color_discrete_sequence=[BLUE])
                chart.update_xaxes(title="Income")
                chart.update_yaxes(title="Loan amount")
                st.plotly_chart(style_chart(chart), use_container_width=True)
            else:
                st.info("No valid pairs.")
        else:
            st.info("Required fields unavailable.")

    with right:
        heading("Interest rate by purpose", "Average recorded interest rate")
        if {"LoanPurpose", "InterestRate"}.issubset(df.columns):
            temp = df[["LoanPurpose", "InterestRate"]].copy()
            temp["InterestRate"] = num(temp, "InterestRate")
            result = temp.groupby("LoanPurpose", dropna=False)["InterestRate"].mean().reset_index().sort_values("InterestRate")
            chart = px.bar(result, x="InterestRate", y="LoanPurpose", orientation="h", color_discrete_sequence=[PURPLE])
            chart.update_xaxes(title="Average interest rate (%)")
            st.plotly_chart(style_chart(chart), use_container_width=True)
        else:
            st.info("Required fields unavailable.")

    heading("Loan records", "First 1,000 records")
    show_table(df.head(1000), 350)
    st.download_button("Download loan CSV", df.to_csv(index=False).encode("utf-8"), "creditiq_loans.csv", "text/csv")


# =====================================================
# 10. BORROWER RISK
# =====================================================

elif page == "Borrower Risk":

    st.info(
        "This section describes patterns in the supplied data. "
        "Associations do not prove causation, and this dashboard does not approve or reject loans."
    )

    left, right = st.columns(2, gap="medium")

    with left:
        heading("Default rate by employment", "Observed binary outcomes")
        if {"EmploymentType", "Default"}.issubset(df.columns):
            temp = df[["EmploymentType", "Default"]].copy()
            temp["Default"] = num(temp, "Default")
            temp = temp[temp["Default"].isin([0, 1])]
            if not temp.empty:
                result = temp.groupby("EmploymentType")["Default"].agg(["mean", "count"]).reset_index()
                result["Default Rate (%)"] = result["mean"] * 100
                chart = px.bar(result.sort_values("Default Rate (%)"), x="Default Rate (%)", y="EmploymentType", orientation="h", color_discrete_sequence=[BLUE], custom_data=["count"])
                chart.update_traces(hovertemplate="%{y}<br>Rate: %{x:.2f}%<br>Records: %{customdata[0]:,}<extra></extra>")
                chart.update_xaxes(title="Default rate (%)", ticksuffix="%")
                st.plotly_chart(style_chart(chart), use_container_width=True)
            else:
                st.info("No valid outcome data.")
        else:
            st.info("Required fields unavailable.")

    with right:
        heading("Debt-to-income distribution", "Observed DTI values")
        dti = num(df, "DTIRatio").dropna()
        if len(dti):
            chart = px.histogram(x=dti, nbins=30, color_discrete_sequence=[AMBER], labels={"x": "DTI ratio", "y": "Borrowers"})
            st.plotly_chart(style_chart(chart), use_container_width=True)
        else:
            st.info("DTI values unavailable.")

    left, right = st.columns(2, gap="medium")

    with left:
        heading("Default by mortgage status", "Descriptive comparison")
        if {"HasMortgage", "Default"}.issubset(df.columns):
            temp = df[["HasMortgage", "Default"]].copy()
            temp["Default"] = num(temp, "Default")
            temp = temp[temp["Default"].isin([0, 1])]
            if not temp.empty:
                result = temp.groupby("HasMortgage")["Default"].mean().mul(100).reset_index(name="Default Rate (%)")
                chart = px.bar(result, x="HasMortgage", y="Default Rate (%)", color="HasMortgage", color_discrete_sequence=[BLUE, CYAN])
                chart.update_yaxes(title="Default rate (%)", ticksuffix="%")
                st.plotly_chart(style_chart(chart), use_container_width=True)
            else:
                st.info("No valid outcomes.")
        else:
            st.info("Required fields unavailable.")

    with right:
        heading("Aggregated risk profile", "SQL-derived summary")
        if sql_data is not None and not sql_data.empty:
            show_table(sql_data, 350)
        else:
            st.info("SQL risk profile unavailable.")

    if risk_data is not None and not risk_data.empty:
        heading("Risk segmentation dataset")
        show_table(risk_data.head(500), 300)


# =====================================================
# 11. MODEL PERFORMANCE
# =====================================================

elif page == "Model Performance":

    if models is None or models.empty:
        st.warning("Model comparison dataset unavailable.")
    elif "Model" not in models.columns:
        st.warning("Model column missing.")
        show_table(models)
    else:
        metric_names = {
            "Accuracy": "Accuracy",
            "Precision": "Precision",
            "Recall": "Recall",
            "F1-score": "F1",
            "ROC-AUC": "ROC_AUC",
        }
        available = {label: col for label, col in metric_names.items() if col in models.columns}

        if not available:
            st.warning("No recognized metrics found.")
            show_table(models)
        else:
            selected = st.selectbox("Performance metric", list(available.keys()))
            metric = available[selected]
            temp = models[["Model", metric]].copy()
            temp[metric] = pd.to_numeric(temp[metric], errors="coerce")
            temp = temp.dropna().sort_values(metric)

            heading(f"Model comparison — {selected}", "Compare recorded model results")
            if not temp.empty:
                chart = px.bar(
                    temp, x=metric, y="Model", orientation="h",
                    color=metric, text=metric,
                    color_continuous_scale=["#DCE8FF", BLUE, NAVY],
                )
                chart.update_traces(texttemplate="%{text:.3f}", textposition="outside", cliponaxis=False)
                if temp[metric].between(0, 1).all():
                    chart.update_xaxes(range=[0, min(1.1, max(1, temp[metric].max() * 1.15))])
                chart.update_xaxes(title=selected)
                st.plotly_chart(style_chart(chart, max(350, len(temp) * 45)), use_container_width=True)
                best = temp.loc[temp[metric].idxmax()]
                st.success(f"Highest recorded {selected}: {best['Model']} ({best[metric]:.4f})")
            else:
                st.info("No valid numeric metrics.")

            heading("Full model comparison")
            show_table(models, 350)

            st.info("Accuracy alone may be misleading for imbalanced data. Evaluate recall, precision, F1 and ROC-AUC together.")


# =====================================================
# 12. EXPLAINABLE AI
# =====================================================

elif page == "Explainable AI":

    if shap_data is None or shap_data.empty:
        st.warning("SHAP dataset unavailable.")
    elif not {"Feature", "Mean_Absolute_SHAP"}.issubset(shap_data.columns):
        st.warning("Expected SHAP columns are missing.")
        show_table(shap_data)
    else:
        temp = shap_data.copy()
        temp["Mean_Absolute_SHAP"] = pd.to_numeric(temp["Mean_Absolute_SHAP"], errors="coerce")
        temp = temp.dropna(subset=["Mean_Absolute_SHAP"]).sort_values("Mean_Absolute_SHAP", ascending=False)

        if temp.empty:
            st.info("No valid SHAP values found.")
        else:
            n = st.slider("Features to display", 3, max(3, min(30, len(temp))), min(10, max(3, len(temp))))
            top = temp.head(n)

            a, b = st.columns(2)
            with a:
                card("FEATURES AVAILABLE", f"{len(temp):,}", "Valid importance rows", BLUE)
            with b:
                card("TOP FEATURE", str(temp.iloc[0]["Feature"]), "Largest mean absolute SHAP", PURPLE)

            heading("Global feature importance", "Higher mean absolute SHAP indicates greater average influence")
            chart = px.bar(
                top.sort_values("Mean_Absolute_SHAP"),
                x="Mean_Absolute_SHAP", y="Feature", orientation="h",
                color="Mean_Absolute_SHAP",
                color_continuous_scale=["#DCE8FF", BLUE, NAVY],
            )
            chart.update_xaxes(title="Mean absolute SHAP value")
            st.plotly_chart(style_chart(chart, max(350, 38 * len(top))), use_container_width=True)

            heading("SHAP importance data")
            show_table(temp, 350)

            st.info(
                "Mean absolute SHAP describes average feature influence. "
                "It does not establish the direction of impact or prove causation."
            )


# =====================================================
# 13. DATA EXPLORER
# =====================================================

elif page == "Data Explorer":

    missing_cells = int(df.isna().sum().sum())

    a, b, c = st.columns(3)
    with a:
        card("TOTAL RECORDS", f"{len(df):,}", "Loan dataset", BLUE)
    with b:
        card("TOTAL COLUMNS", f"{len(df.columns):,}", "Available fields", CYAN)
    with c:
        card("MISSING CELLS", f"{missing_cells:,}", "Across the dataset", AMBER)

    heading("Loan records", "First 1,000 rows")
    show_table(df.head(1000), 400)

    st.download_button(
        "Download loan dataset",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="creditiq_data.csv",
        mime="text/csv",
    )

    heading("Column quality", "Types, missing values and unique counts")
    quality = pd.DataFrame({
        "Column": df.columns,
        "Data type": [str(df[c].dtype) for c in df.columns],
        "Missing values": [int(df[c].isna().sum()) for c in df.columns],
        "Missing (%)": [round(df[c].isna().mean() * 100, 2) for c in df.columns],
        "Unique values": [int(df[c].nunique(dropna=True)) for c in df.columns],
    })
    show_table(quality, 400)


# =====================================================
# 14. FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    CREDITIQ · CREDIT RISK & LOAN DEFAULT ANALYTICS
    <br>
    Academic analytics platform · Not an official credit bureau score
</div>
""", unsafe_allow_html=True)
