from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Netflix | Viewing intelligence",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
        :root {
            --ink: #f5f5f1;
            --muted: #a8a8a8;
            --paper: #090909;
            --surface: #151515;
            --line: #303030;
            --red: #e50914;
        }
        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
        .stApp { background: var(--paper); color: var(--ink); }
        [data-testid="stSidebar"] {
            background: #101010;
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebar"] > div { padding-top: 1.4rem; }
        .block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1440px; }
        h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: var(--ink); letter-spacing: 0; }
        h1 { font-size: 2.35rem; margin-bottom: .2rem; }
        h2 { font-size: 1.2rem; }
        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-top: 3px solid var(--red);
            border-radius: 6px;
            padding: 1rem 1.1rem;
            min-height: 116px;
        }
        [data-testid="stMetricLabel"], [data-testid="stCaptionContainer"] { color: var(--muted); }
        [data-testid="stMetricValue"] { font-family: 'Space Grotesk', sans-serif; color: var(--ink); }
        .eyebrow { color: var(--red); text-transform: uppercase; font-size: .72rem; font-weight: 700; letter-spacing: .12em; }
        .brand-mark { color: var(--red); font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 700; letter-spacing: .08em; }
        .subhead { color: var(--muted); margin-top: 0; margin-bottom: 1.35rem; }
        .section-label { color: var(--red); text-transform: uppercase; font-size: .72rem; font-weight: 700; letter-spacing: .1em; }
        [data-testid="stVegaLiteChart"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: .5rem;
        }
        [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 6px; }
        [data-testid="stFileUploader"], [data-baseweb="select"], [data-testid="stDateInput"] {
            background: var(--surface);
            border-radius: 6px;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--muted); }
        @media (max-width: 700px) { h1 { font-size: 1.8rem; } .block-container { padding-top: 1.3rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_local_csv() -> pd.DataFrame | None:
    search_roots = [Path.cwd(), Path(__file__).resolve().parent]
    preferred_names = ["netflix.csv", "netflix_100_customers_dataset.csv", "netflix_100_customers_dataset (3).csv"]

    for root in search_roots:
        for candidate in [root / name for name in preferred_names]:
            if candidate.is_file():
                return pd.read_csv(candidate)

        for csv_path in sorted(root.glob("*.csv")):
            name = csv_path.name.lower()
            if "netflix" in name or "customer" in name:
                try:
                    return pd.read_csv(csv_path)
                except (OSError, pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError):
                    continue
    return None


st.sidebar.markdown('<div class="brand-mark">NETFLIX</div>', unsafe_allow_html=True)
st.sidebar.header("Your dataset")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

try:
    if uploaded_file is not None:
        netflix = pd.read_csv(uploaded_file)
        source_label = uploaded_file.name
    else:
        netflix = load_local_csv()
        source_label = "netflix.csv"
except (OSError, pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as error:
    st.error(f"Could not read the CSV file: {error}")
    st.stop()

if netflix is None:
    st.title("Viewing intelligence")
    st.markdown("Add your viewing data to explore revenue, ratings, and audience trends.")
    st.info("Upload a CSV from the sidebar, or place `netflix.csv` beside this app.")
    st.stop()

netflix = netflix.copy()
if "Watch_Date" in netflix.columns:
    netflix["Watch_Date"] = pd.to_datetime(netflix["Watch_Date"], errors="coerce")
if "Monthly_Revenue" in netflix.columns:
    netflix["Monthly_Revenue"] = pd.to_numeric(netflix["Monthly_Revenue"], errors="coerce")
if "Rating" in netflix.columns:
    netflix["Rating"] = pd.to_numeric(netflix["Rating"], errors="coerce")

st.sidebar.caption(f"Source: {source_label} · {len(netflix):,} rows")
st.sidebar.divider()
st.sidebar.subheader("Filters")

filtered = netflix.copy()
for column in ["Region", "Subscription_Plan", "Category"]:
    if column in filtered.columns:
        choices = sorted(filtered[column].dropna().astype(str).unique().tolist())
        selected = st.sidebar.multiselect(column.replace("_", " "), choices)
        if selected:
            filtered = filtered[filtered[column].astype(str).isin(selected)]

if "Watch_Date" in filtered.columns and filtered["Watch_Date"].notna().any():
    min_date = filtered["Watch_Date"].min().date()
    max_date = filtered["Watch_Date"].max().date()
    selected_dates = st.sidebar.date_input(
        "Watch date",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered = filtered[filtered["Watch_Date"].dt.date.between(start_date, end_date)]

st.markdown('<div class="eyebrow">Netflix audience report</div>', unsafe_allow_html=True)
st.title("Viewing intelligence")
st.markdown(
    "<p class='subhead'>A clear read on revenue, ratings, and what audiences watch.</p>",
    unsafe_allow_html=True,
)
st.markdown('<div class="section-label">At a glance</div>', unsafe_allow_html=True)

revenue = filtered["Monthly_Revenue"].sum() if "Monthly_Revenue" in filtered.columns else 0
average_rating = filtered["Rating"].mean() if "Rating" in filtered.columns else None
unique_regions = filtered["Region"].nunique() if "Region" in filtered.columns else None
metric_columns = st.columns(4)
metric_columns[0].metric("Records", f"{len(filtered):,}", f"of {len(netflix):,} total")
metric_columns[1].metric("Monthly revenue", f"${revenue:,.0f}")
metric_columns[2].metric("Average rating", f"{average_rating:.1f}" if pd.notna(average_rating) else "—")
metric_columns[3].metric("Regions", f"{unique_regions:,}" if unique_regions is not None else "—")

if filtered.empty:
    st.warning("No records match these filters. Adjust the selections in the sidebar.")
else:
    st.markdown("## Performance")
    chart_columns = st.columns(2)
    with chart_columns[0]:
        st.subheader("Revenue by region")
        if {"Region", "Monthly_Revenue"}.issubset(filtered.columns):
            region_revenue = filtered.groupby("Region", dropna=False)["Monthly_Revenue"].sum().sort_values(ascending=False)
            st.bar_chart(region_revenue, color="#e50914", height=300)
        else:
            st.caption("Add Region and Monthly_Revenue columns to see this chart.")

    with chart_columns[1]:
        st.subheader("Revenue by category")
        if {"Category", "Monthly_Revenue"}.issubset(filtered.columns):
            category_revenue = filtered.groupby("Category", dropna=False)["Monthly_Revenue"].sum().sort_values(ascending=False)
            st.bar_chart(category_revenue, color="#e50914", height=300)
        else:
            st.caption("Add Category and Monthly_Revenue columns to see this chart.")

    lower_columns = st.columns([1, 1.35])
    with lower_columns[0]:
        st.subheader("Ratings by subscription")
        if {"Subscription_Plan", "Rating"}.issubset(filtered.columns):
            plan_ratings = filtered.groupby("Subscription_Plan", dropna=False)["Rating"].mean().sort_values(ascending=False)
            st.bar_chart(plan_ratings, color="#e50914", height=280)
        else:
            st.caption("Add Subscription_Plan and Rating columns to see this chart.")

    with lower_columns[1]:
        st.subheader("Monthly revenue trend")
        if {"Watch_Date", "Monthly_Revenue"}.issubset(filtered.columns):
            trend = filtered.dropna(subset=["Watch_Date", "Monthly_Revenue"]).copy()
            if not trend.empty:
                trend["Month"] = trend["Watch_Date"].dt.to_period("M").astype(str)
                monthly_revenue = trend.groupby("Month")["Monthly_Revenue"].sum()
                st.line_chart(monthly_revenue, color="#e50914", height=280)
            else:
                st.caption("No valid date and revenue values are available for this range.")
        else:
            st.caption("Add Watch_Date and Monthly_Revenue columns to see this chart.")

st.markdown("## Viewing records")
st.dataframe(filtered, width="stretch", hide_index=True)
