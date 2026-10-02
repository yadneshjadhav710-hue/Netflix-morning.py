from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Netflix • Insight Studio", page_icon="🎬", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--red:#e50914;--red2:#ff4050;--bg:#030304;--card:rgba(17,17,20,.78);--line:rgba(255,255,255,.10);--muted:#a6a6aa;--white:#f7f7f7}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:#030304;color:var(--white);overflow-x:hidden}
/* cinematic layered background */
.stApp:before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;background:radial-gradient(ellipse at 50% -12%,rgba(229,9,20,.34),transparent 42%),radial-gradient(circle at 8% 72%,rgba(229,9,20,.16),transparent 24%),radial-gradient(circle at 94% 24%,rgba(255,40,55,.12),transparent 22%),linear-gradient(145deg,#010102 0%,#09090c 42%,#020203 100%)}
.stApp:after{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.55;background:linear-gradient(120deg,transparent 0%,rgba(255,255,255,.025) 38%,transparent 55%),repeating-linear-gradient(135deg,rgba(255,255,255,.018) 0 1px,transparent 1px 70px);mask-image:linear-gradient(to bottom,black,transparent 92%)}
.block-container{max-width:1500px;padding:1.7rem 2rem 3.5rem;position:relative;z-index:2}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#09090b,#020203);border-right:1px solid var(--line);position:relative;z-index:3}
[data-testid="stSidebar"]:before{content:"";position:absolute;top:0;left:0;right:0;height:180px;background:radial-gradient(circle at 50% 0,rgba(229,9,20,.20),transparent 68%);pointer-events:none}
/* premium hero */
.hero{position:relative;overflow:hidden;padding:2.35rem 2.5rem;margin-bottom:1.5rem;border:1px solid rgba(255,255,255,.11);border-radius:26px;background:linear-gradient(115deg,rgba(19,19,22,.96),rgba(8,8,10,.72) 58%,rgba(35,4,7,.58));box-shadow:0 30px 90px rgba(0,0,0,.48),inset 0 1px 0 rgba(255,255,255,.05)}
.hero:before{content:"";position:absolute;width:420px;height:420px;right:-130px;top:-170px;border-radius:50%;background:radial-gradient(circle,rgba(229,9,20,.34),rgba(229,9,20,.06) 42%,transparent 70%);filter:blur(4px)}
.hero:after{content:"N";position:absolute;right:30px;bottom:-78px;font-family:'Space Grotesk';font-size:300px;font-weight:700;line-height:1;color:transparent;-webkit-text-stroke:2px rgba(229,9,20,.10);text-shadow:0 0 70px rgba(229,9,20,.10)}
.hero-line{position:absolute;left:0;top:0;width:6px;height:100%;background:linear-gradient(180deg,var(--red2),var(--red),transparent);box-shadow:0 0 25px rgba(229,9,20,.7)}
.eyebrow{color:var(--red2);font-size:.72rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;position:relative;z-index:2}.hero h1{font-family:'Space Grotesk';font-size:clamp(2.1rem,4vw,3.7rem);margin:.35rem 0 .45rem;letter-spacing:-.045em;position:relative;z-index:2}.hero p{color:#aaa;max-width:720px;margin:0;font-size:1rem;line-height:1.65;position:relative;z-index:2}.pill{display:inline-flex;align-items:center;gap:.45rem;margin-top:1.1rem;padding:.42rem .8rem;border:1px solid rgba(229,9,20,.38);border-radius:999px;color:#ddd;background:rgba(229,9,20,.09);font-size:.72rem;position:relative;z-index:2;box-shadow:0 0 25px rgba(229,9,20,.08)}
.brand{font-family:'Space Grotesk';font-size:1.28rem;font-weight:700;letter-spacing:.17em;color:var(--red);padding:.5rem 0;text-shadow:0 0 22px rgba(229,9,20,.35)}.side-note{color:#777;font-size:.78rem;line-height:1.5}
[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(27,27,31,.92),rgba(8,8,10,.78));border:1px solid var(--line);border-top:3px solid var(--red);border-radius:18px;padding:1rem 1.15rem;min-height:125px;box-shadow:0 18px 45px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.035);transition:transform .2s ease,box-shadow .2s ease}[data-testid="stMetric"]:hover{transform:translateY(-5px);box-shadow:0 24px 55px rgba(229,9,20,.13),inset 0 1px 0 rgba(255,255,255,.06)}[data-testid="stMetricValue"]{font-family:'Space Grotesk';font-size:1.85rem}
.section{font-family:'Space Grotesk';font-size:1.2rem;font-weight:700;margin:1.65rem 0 .8rem}.section span{color:var(--red);margin-right:.3rem}
[data-testid="stVegaLiteChart"],[data-testid="stDataFrame"]{background:var(--card);border:1px solid var(--line);border-radius:18px;box-shadow:0 18px 45px rgba(0,0,0,.22);overflow:hidden}
[data-testid="stVegaLiteChart"]{backdrop-filter:blur(12px)}
[data-baseweb="select"],[data-testid="stDateInput"],[data-testid="stFileUploader"]{border-radius:11px}
.stButton button{border-radius:11px;border:1px solid rgba(229,9,20,.45);background:rgba(229,9,20,.08)}
.footer{text-align:center;color:#666;font-size:.75rem;margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--line);letter-spacing:.04em}
@media(max-width:700px){.block-container{padding:1rem}.hero{padding:1.55rem 1.35rem}.hero:after{font-size:170px}.hero h1{font-size:2rem}.hero p{font-size:.9rem}}
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
    st.markdown('<div class="hero"><div class="hero-line"></div><div class="eyebrow">Netflix Insight Studio</div><h1>Bring your audience data to life.</h1><p>Upload a CSV to unlock the interactive analytics workspace.</p></div>',unsafe_allow_html=True);st.stop()

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

st.markdown('<div class="hero"><div class="hero-line"></div><div class="eyebrow">NETFLIX • AUDIENCE ANALYTICS</div><h1>Viewing Intelligence</h1><p>One premium workspace for revenue, ratings, regional performance and audience behaviour.</p><div class="pill">● LIVE DATA EXPLORATION</div></div>',unsafe_allow_html=True)

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
