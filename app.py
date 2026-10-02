from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Netflix | Viewing Intelligence",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
        :root { --ink:#f5f5f1; --muted:#a8a8a8; --paper:#050505; --surface:rgba(20,20,20,.88); --surface-2:rgba(28,28,28,.72); --line:rgba(255,255,255,.10); --red:#e50914; }
        html,body,[class*="css"] { font-family:'DM Sans',sans-serif; }
        body { background:#050505; }
        .stApp { color:var(--ink); background:radial-gradient(circle at 8% 5%,rgba(229,9,20,.22),transparent 25%),radial-gradient(circle at 92% 18%,rgba(150,0,0,.16),transparent 24%),linear-gradient(135deg,#030303 0%,#0b0b0b 48%,#050505 100%); background-attachment:fixed; }
        .stApp::before { content:""; position:fixed; inset:0; pointer-events:none; background-image:linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.018) 1px,transparent 1px); background-size:42px 42px; mask-image:linear-gradient(to bottom,black,transparent 82%); z-index:0; }
        [data-testid="stSidebar"] { background:linear-gradient(180deg,rgba(12,12,12,.98),rgba(5,5,5,.96)); border-right:1px solid var(--line); box-shadow:12px 0 40px rgba(0,0,0,.25); }
        [data-testid="stSidebar"]>div { padding-top:1.4rem; }
        .block-container { padding-top:2rem; padding-bottom:3rem; max-width:1440px; position:relative; z-index:1; }
        h1,h2,h3 { font-family:'Space Grotesk',sans-serif; color:var(--ink); }
        h1 { font-size:2.55rem; margin-bottom:.2rem; font-weight:700; }
        h2 { font-size:1.25rem; }
        [data-testid="stMetric"] { background:linear-gradient(145deg,rgba(30,30,30,.94),rgba(12,12,12,.88)); border:1px solid var(--line); border-top:3px solid var(--red); border-radius:14px; padding:1.05rem 1.15rem; min-height:116px; box-shadow:0 12px 30px rgba(0,0,0,.22); transition:transform .2s ease,border-color .2s ease; }
        [data-testid="stMetric"]:hover { transform:translateY(-3px); border-color:rgba(229,9,20,.55); }
        [data-testid="stMetricLabel"],[data-testid="stCaptionContainer"] { color:var(--muted); }
        [data-testid="stMetricValue"] { font-family:'Space Grotesk',sans-serif; color:var(--ink); }
        .eyebrow { color:#ff2430; text-transform:uppercase; font-size:.72rem; font-weight:700; letter-spacing:.15em; }
        .brand-mark { color:var(--red); font-family:'Space Grotesk',sans-serif; font-size:1.05rem; font-weight:700; letter-spacing:.13em; }
        .subhead { color:#b7b7b7; margin-top:0; margin-bottom:1.35rem; font-size:1rem; }
        .section-label { color:#ff2430; text-transform:uppercase; font-size:.72rem; font-weight:700; letter-spacing:.12em; }
        [data-testid="stVegaLiteChart"],[data-testid="stDataFrame"] { background:var(--surface); border:1px solid var(--line); border-radius:14px; box-shadow:0 12px 30px rgba(0,0,0,.18); }
        [data-testid="stVegaLiteChart"] { padding:.5rem; }
        [data-testid="stFileUploader"],[data-baseweb="select"],[data-testid="stDateInput"] { background:var(--surface-2); border-radius:10px; }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:var(--muted); }
        .hero-card { padding:1.35rem 1.5rem; margin-bottom:1.35rem; border:1px solid rgba(255,255,255,.10); border-left:4px solid var(--red); border-radius:16px; background:linear-gradient(105deg,rgba(25,25,25,.92),rgba(12,12,12,.68)); box-shadow:0 18px 45px rgba(0,0,0,.25); }
        .hero-title { font-family:'Space Grotesk',sans-serif; font-size:2.45rem; font-weight:700; margin:.25rem 0 .35rem; }
        .hero-text { color:#b9b9b9; font-size:.98rem; margin:0; }
        .footer-note { color:#777; text-align:center; font-size:.78rem; margin-top:2rem; }
        @media(max-width:700px){ h1{font-size:1.8rem;} .hero-title{font-size:1.8rem;} .block-container{padding-top:1.3rem;} }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_local_csv() -> pd.DataFrame | None:
    search_roots=[Path.cwd(),Path(__file__).resolve().parent]
    preferred_names=["netflix.csv","netflix_100_customers_dataset.csv","netflix_100_customers_dataset (3).csv"]
    for root in search_roots:
        for candidate in [root/name for name in preferred_names]:
            if candidate.is_file(): return pd.read_csv(candidate)
        for csv_path in sorted(root.glob("*.csv")):
            name=csv_path.name.lower()
            if "netflix" in name or "customer" in name:
                try: return pd.read_csv(csv_path)
                except (OSError,pd.errors.ParserError,pd.errors.EmptyDataError,UnicodeDecodeError): continue
    return None

st.sidebar.markdown('<div class="brand-mark">NETFLIX</div>',unsafe_allow_html=True)
st.sidebar.header("Your dataset")
uploaded_file=st.sidebar.file_uploader("Upload a CSV file",type=["csv"])
try:
    if uploaded_file is not None: netflix=pd.read_csv(uploaded_file); source_label=uploaded_file.name
    else: netflix=load_local_csv(); source_label="netflix.csv"
except (OSError,pd.errors.ParserError,pd.errors.EmptyDataError,UnicodeDecodeError) as error:
    st.error(f"Could not read the CSV file: {error}"); st.stop()

if netflix is None:
    st.title("Viewing intelligence")
    st.markdown("Add your viewing data to explore revenue, ratings, and audience trends.")
    st.info("Upload a CSV from the sidebar, or place `netflix.csv` beside this app.")
    st.stop()

netflix=netflix.copy()
if "Watch_Date" in netflix.columns: netflix["Watch_Date"]=pd.to_datetime(netflix["Watch_Date"],errors="coerce")
if "Monthly_Revenue" in netflix.columns: netflix["Monthly_Revenue"]=pd.to_numeric(netflix["Monthly_Revenue"],errors="coerce")
if "Rating" in netflix.columns: netflix["Rating"]=pd.to_numeric(netflix["Rating"],errors="coerce")

st.sidebar.caption(f"Source: {source_label} · {len(netflix):,} rows")
st.sidebar.divider(); st.sidebar.subheader("Filters")
filtered=netflix.copy()
for column in ["Region","Subscription_Plan","Category"]:
    if column in filtered.columns:
        choices=sorted(filtered[column].dropna().astype(str).unique().tolist())
        selected=st.sidebar.multiselect(column.replace("_"," "),choices)
        if selected: filtered=filtered[filtered[column].astype(str).isin(selected)]

if "Watch_Date" in filtered.columns and filtered["Watch_Date"].notna().any():
    min_date=filtered["Watch_Date"].min().date(); max_date=filtered["Watch_Date"].max().date()
    selected_dates=st.sidebar.date_input("Watch date",value=(min_date,max_date),min_value=min_date,max_value=max_date)
    if isinstance(selected_dates,tuple) and len(selected_dates)==2:
        start_date,end_date=selected_dates
        filtered=filtered[filtered["Watch_Date"].dt.date.between(start_date,end_date)]

st.markdown('<div class="hero-card"><div class="eyebrow">NETFLIX AUDIENCE ANALYTICS</div><div class="hero-title">Viewing Intelligence Dashboard</div><p class="hero-text">Professional insights into revenue, ratings, regions and audience viewing behaviour.</p></div>',unsafe_allow_html=True)
st.markdown('<div class="section-label">At a glance</div>',unsafe_allow_html=True)
revenue=filtered["Monthly_Revenue"].sum() if "Monthly_Revenue" in filtered.columns else 0
average_rating=filtered["Rating"].mean() if "Rating" in filtered.columns else None
unique_regions=filtered["Region"].nunique() if "Region" in filtered.columns else None
metric_columns=st.columns(4)
metric_columns[0].metric("Records",f"{len(filtered):,}",f"of {len(netflix):,} total")
metric_columns[1].metric("Monthly revenue",f"${revenue:,.0f}")
metric_columns[2].metric("Average rating",f"{average_rating:.1f}" if pd.notna(average_rating) else "—")
metric_columns[3].metric("Regions",f"{unique_regions:,}" if unique_regions is not None else "—")

if filtered.empty:
    st.warning("No records match these filters. Adjust the selections in the sidebar.")
else:
    st.markdown("## Performance")
    chart_columns=st.columns(2)
    with chart_columns[0]:
        st.subheader("Revenue by region")
        if {"Region","Monthly_Revenue"}.issubset(filtered.columns):
            region_revenue=filtered.groupby("Region",dropna=False)["Monthly_Revenue"].sum().sort_values(ascending=False)
            st.bar_chart(region_revenue,color="#e50914",height=300)
        else: st.caption("Add Region and Monthly_Revenue columns to see this chart.")
    with chart_columns[1]:
        st.subheader("Revenue by category")
        if {"Category","Monthly_Revenue"}.issubset(filtered.columns):
            category_revenue=filtered.groupby("Category",dropna=False)["Monthly_Revenue"].sum().sort_values(ascending=False)
            st.bar_chart(category_revenue,color="#e50914",height=300)
        else: st.caption("Add Category and Monthly_Revenue columns to see this chart.")
    lower_columns=st.columns([1,1.35])
    with lower_columns[0]:
        st.subheader("Ratings by subscription")
        if {"Subscription_Plan","Rating"}.issubset(filtered.columns):
            plan_ratings=filtered.groupby("Subscription_Plan",dropna=False)["Rating"].mean().sort_values(ascending=False)
            st.bar_chart(plan_ratings,color="#e50914",height=280)
        else: st.caption("Add Subscription_Plan and Rating columns to see this chart.")
    with lower_columns[1]:
        st.subheader("Monthly revenue trend")
        if {"Watch_Date","Monthly_Revenue"}.issubset(filtered.columns):
            trend=filtered.dropna(subset=["Watch_Date","Monthly_Revenue"]).copy()
            if not trend.empty:
                trend["Month"]=trend["Watch_Date"].dt.to_period("M").astype(str)
                monthly_revenue=trend.groupby("Month")["Monthly_Revenue"].sum()
                st.line_chart(monthly_revenue,color="#e50914",height=280)
            else: st.caption("No valid date and revenue values are available for this range.")
        else: st.caption("Add Watch_Date and Monthly_Revenue columns to see this chart.")

st.markdown("## Viewing records")
st.dataframe(filtered,width="stretch",hide_index=True)
st.markdown('<div class="footer-note">Netflix Viewing Intelligence • Professional Analytics Dashboard</div>',unsafe_allow_html=True)
