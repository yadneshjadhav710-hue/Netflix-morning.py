from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Netflix • Insight Studio", page_icon="🎬", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--red:#e50914;--red2:#ff3340;--bg:#050505;--card:rgba(18,18,18,.82);--line:rgba(255,255,255,.09);--muted:#9d9d9d}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}.stApp{background:radial-gradient(circle at 12% 0%,rgba(229,9,20,.30),transparent 27%),radial-gradient(circle at 92% 35%,rgba(120,0,0,.18),transparent 25%),linear-gradient(135deg,#020202,#0b0b0b 50%,#030303);background-attachment:fixed;color:#f5f5f5}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.42;background-image:linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.018) 1px,transparent 1px);background-size:44px 44px;mask-image:linear-gradient(to bottom,#000,transparent 90%)}
.block-container{max-width:1480px;padding:1.8rem 2rem 3rem;position:relative;z-index:1}.stSidebar{background:#080808}.stSidebar [data-testid="stSidebar"]{background:linear-gradient(180deg,#0b0b0b,#030303);border-right:1px solid var(--line)}
.hero{position:relative;overflow:hidden;padding:2rem 2.2rem;margin-bottom:1.5rem;border:1px solid var(--line);border-radius:24px;background:linear-gradient(115deg,rgba(25,25,25,.96),rgba(8,8,8,.72));box-shadow:0 24px 70px rgba(0,0,0,.38)}
.hero:after{content:"N";position:absolute;right:35px;top:-55px;font-family:'Space Grotesk';font-size:230px;font-weight:700;color:rgba(229,9,20,.08);line-height:1}.eyebrow{color:var(--red2);font-size:.72rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase}.hero h1{font-family:'Space Grotesk';font-size:clamp(2rem,4vw,3.5rem);margin:.3rem 0 .4rem;letter-spacing:-.04em}.hero p{color:#aaa;max-width:650px;margin:0;font-size:1rem}.pill{display:inline-block;margin-top:1rem;padding:.35rem .7rem;border:1px solid rgba(229,9,20,.35);border-radius:999px;color:#ddd;background:rgba(229,9,20,.08);font-size:.75rem}
.brand{font-family:'Space Grotesk';font-size:1.25rem;font-weight:700;letter-spacing:.16em;color:var(--red);padding:.5rem 0}.side-note{color:#777;font-size:.78rem;line-height:1.5}
[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(29,29,29,.94),rgba(10,10,10,.82));border:1px solid var(--line);border-top:3px solid var(--red);border-radius:16px;padding:1rem 1.15rem;min-height:125px;box-shadow:0 16px 35px rgba(0,0,0,.22);transition:.2s}[data-testid="stMetric"]:hover{transform:translateY(-4px);box-shadow:0 20px 45px rgba(229,9,20,.12)}[data-testid="stMetricValue"]{font-family:'Space Grotesk';font-size:1.8rem}
.section{font-family:'Space Grotesk';font-size:1.2rem;font-weight:700;margin:1.5rem 0 .75rem}.section span{color:var(--red)}
[data-testid="stVegaLiteChart"],[data-testid="stDataFrame"]{background:var(--card);border:1px solid var(--line);border-radius:16px;box-shadow:0 14px 35px rgba(0,0,0,.18);overflow:hidden}.stButton button{border-radius:10px;border:1px solid rgba(229,9,20,.4)}
[data-baseweb="select"],[data-testid="stDateInput"],[data-testid="stFileUploader"]{border-radius:10px}.footer{text-align:center;color:#666;font-size:.75rem;margin-top:2.2rem;padding-top:1rem;border-top:1px solid var(--line)}
@media(max-width:700px){.block-container{padding:1rem}.hero{padding:1.4rem}.hero:after{font-size:150px}.hero h1{font-size:2rem}}
</style>
""", unsafe_allow_html=True)

def load_csv():
    roots=[Path.cwd(),Path(__file__).resolve().parent]
    preferred=["netflix.csv","netflix_100_customers_dataset.csv","netflix_100_customers_dataset (3).csv"]
    for root in roots:
        for name in preferred:
            p=root/name
            if p.is_file(): return pd.read_csv(p),p.name
        for p in sorted(root.glob('*.csv')):
            if 'netflix' in p.name.lower() or 'customer' in p.name.lower():
                try:return pd.read_csv(p),p.name
                except Exception:pass
    return None,None

st.sidebar.markdown('<div class="brand">NETFLIX</div>',unsafe_allow_html=True)
st.sidebar.markdown('<div class="side-note">INSIGHT STUDIO<br>Audience & revenue analytics</div>',unsafe_allow_html=True)
st.sidebar.divider()
up=st.sidebar.file_uploader('Upload viewing CSV',type=['csv'])
if up is not None:
    df=pd.read_csv(up); source=up.name
else:
    df,source=load_csv()
if df is None:
    st.markdown('<div class="hero"><div class="eyebrow">Netflix Insight Studio</div><h1>Bring your audience data to life.</h1><p>Upload a CSV to unlock the interactive analytics workspace.</p></div>',unsafe_allow_html=True);st.stop()

df=df.copy()
for c in ['Watch_Date']:
    if c in df: df[c]=pd.to_datetime(df[c],errors='coerce')
for c in ['Monthly_Revenue','Rating']:
    if c in df: df[c]=pd.to_numeric(df[c],errors='coerce')

st.sidebar.caption(f"Source: {source} • {len(df):,} records")
st.sidebar.divider();st.sidebar.subheader('Smart filters')
filtered=df.copy()
for c in ['Region','Subscription_Plan','Category']:
    if c in filtered.columns:
        vals=sorted(filtered[c].dropna().astype(str).unique())
        pick=st.sidebar.multiselect(c.replace('_',' '),vals)
        if pick: filtered=filtered[filtered[c].astype(str).isin(pick)]
if 'Watch_Date' in filtered and filtered['Watch_Date'].notna().any():
    lo,hi=filtered['Watch_Date'].min().date(),filtered['Watch_Date'].max().date()
    dates=st.sidebar.date_input('Watch period',value=(lo,hi),min_value=lo,max_value=hi)
    if isinstance(dates,tuple) and len(dates)==2: filtered=filtered[filtered['Watch_Date'].dt.date.between(dates[0],dates[1])]

st.markdown('<div class="hero"><div class="eyebrow">NETFLIX • AUDIENCE ANALYTICS</div><h1>Viewing Intelligence</h1><p>One premium workspace for revenue, ratings, regional performance and audience behaviour.</p><div class="pill">● LIVE DATA EXPLORATION</div></div>',unsafe_allow_html=True)

revenue=filtered['Monthly_Revenue'].sum() if 'Monthly_Revenue' in filtered else 0
rating=filtered['Rating'].mean() if 'Rating' in filtered else None
regions=filtered['Region'].nunique() if 'Region' in filtered else None
c=st.columns(4)
c[0].metric('👥 Audience records',f'{len(filtered):,}',f'{len(df):,} total')
c[1].metric('💰 Monthly revenue',f'${revenue:,.0f}')
c[2].metric('⭐ Average rating',f'{rating:.1f}' if pd.notna(rating) else '—')
c[3].metric('🌎 Active regions',f'{regions:,}' if regions is not None else '—')

if filtered.empty: st.warning('No records match the selected filters.');st.stop()
st.markdown('<div class="section"><span>01</span> Performance overview</div>',unsafe_allow_html=True)
a,b=st.columns(2)
with a:
    st.subheader('Revenue by region')
    if {'Region','Monthly_Revenue'}.issubset(filtered.columns): st.bar_chart(filtered.groupby('Region')['Monthly_Revenue'].sum().sort_values(ascending=False),color='#e50914',height=320)
with b:
    st.subheader('Revenue by category')
    if {'Category','Monthly_Revenue'}.issubset(filtered.columns): st.bar_chart(filtered.groupby('Category')['Monthly_Revenue'].sum().sort_values(ascending=False),color='#e50914',height=320)

st.markdown('<div class="section"><span>02</span> Audience intelligence</div>',unsafe_allow_html=True)
a,b=st.columns([1,1.35])
with a:
    st.subheader('Ratings by subscription')
    if {'Subscription_Plan','Rating'}.issubset(filtered.columns): st.bar_chart(filtered.groupby('Subscription_Plan')['Rating'].mean().sort_values(ascending=False),color='#e50914',height=300)
with b:
    st.subheader('Monthly revenue trend')
    if {'Watch_Date','Monthly_Revenue'}.issubset(filtered.columns):
        t=filtered.dropna(subset=['Watch_Date','Monthly_Revenue']).copy();t['Month']=t['Watch_Date'].dt.to_period('M').astype(str)
        st.line_chart(t.groupby('Month')['Monthly_Revenue'].sum(),color='#e50914',height=300)

st.markdown('<div class="section"><span>03</span> Data explorer</div>',unsafe_allow_html=True)
st.dataframe(filtered,width='stretch',hide_index=True)
st.markdown('<div class="footer">NETFLIX INSIGHT STUDIO • Built with Streamlit & Pandas • Interactive Analytics</div>',unsafe_allow_html=True)
