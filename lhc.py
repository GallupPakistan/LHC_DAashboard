import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Lahore High Court Analytics",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# THEME / CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --pk-green:   #014421;
    --pk-gold:    #C9A84C;
    --navy:       #1B2B4B;
    --navy-mid:   #2C3E6B;
    --cream:      #F5F0E8;
    --cream-dark: #EDE7D9;
    --text-dark:  #1A1A2E;
    --text-mid:   #4A4A6A;
    --accent-red: #8B1A1A;
    --white:      #FFFFFF;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: var(--cream);
    color: var(--text-dark);
}

/* Hide Streamlit default chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--navy) 0%, var(--navy-mid) 100%);
    border-right: 3px solid var(--pk-gold);
}
[data-testid="stSidebar"] * { color: #E8E4DA !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color: var(--pk-gold) !important; font-weight: 600; font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 { color: var(--pk-gold) !important; font-family: 'Playfair Display', serif; }

/* ── HEADER BANNER ── */
.lhc-header {
    background: linear-gradient(135deg, var(--navy) 0%, var(--pk-green) 60%, #01321A 100%);
    padding: 1.6rem 2rem 1.2rem;
    border-radius: 12px;
    margin-bottom: 1.4rem;
    border-bottom: 4px solid var(--pk-gold);
    display: flex;
    align-items: center;
    gap: 1.5rem;
    box-shadow: 0 8px 32px rgba(27,43,75,0.25);
}
.lhc-header-text h1 {
    font-family: 'Playfair Display', serif;
    font-size: 1.85rem;
    color: var(--white);
    margin: 0;
    line-height: 1.2;
}
.lhc-header-text p {
    color: var(--pk-gold);
    font-size: 0.82rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0.2rem 0 0;
}
.lhc-emblem {
    font-size: 3.5rem;
    filter: drop-shadow(0 2px 8px rgba(0,0,0,0.4));
}
.lhc-meta {
    margin-left: auto;
    text-align: right;
    color: #C8D4E8;
    font-size: 0.78rem;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── KPI CARDS ── */
.kpi-row { display: flex; gap: 1rem; margin-bottom: 1.4rem; }
.kpi-card {
    flex: 1;
    background: var(--white);
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    border-left: 5px solid var(--pk-gold);
    box-shadow: 0 2px 12px rgba(27,43,75,0.10);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: -20px; right: -20px;
    width: 80px; height: 80px;
    background: var(--cream);
    border-radius: 50%;
    opacity: 0.6;
}
.kpi-card.green { border-left-color: var(--pk-green); }
.kpi-card.navy  { border-left-color: var(--navy); }
.kpi-card.red   { border-left-color: var(--accent-red); }
.kpi-label { font-size: 0.73rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-mid); font-weight: 600; margin-bottom: 0.3rem; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 2.1rem; font-weight: 700; color: var(--navy); line-height: 1; }
.kpi-sub   { font-size: 0.72rem; color: var(--text-mid); margin-top: 0.2rem; font-family: 'IBM Plex Mono', monospace; }

/* ── SECTION HEADERS ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    color: var(--navy);
    border-bottom: 2px solid var(--pk-gold);
    padding-bottom: 0.4rem;
    margin: 1.2rem 0 0.8rem;
}

/* ── CHART CARDS ── */
.chart-card {
    background: var(--white);
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 2px 12px rgba(27,43,75,0.08);
    margin-bottom: 1rem;
}

/* ── TABS ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 600;
    font-size: 0.68rem;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    color: var(--text-mid);
    padding: 0.5rem 0.55rem;
    white-space: nowrap;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--navy) !important;
    border-bottom: 3px solid var(--pk-gold) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }

/* ── ALERT BOX ── */
.alert-box {
    background: #FFF8EC;
    border: 1.5px solid var(--pk-gold);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-bottom: 1rem;
    font-size: 0.82rem;
    color: var(--text-dark);
}

/* ── PAGE TABS ── */
.stTabs { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# COLOUR PALETTE (Plotly)
# ─────────────────────────────────────────────
NAVY    = "#1B2B4B"
GOLD    = "#C9A84C"
GREEN   = "#014421"
CREAM   = "#F5F0E8"
RED     = "#8B1A1A"
TEAL    = "#1A6B6B"
SAGE    = "#5A7A5A"
MID     = "#2C3E6B"

PALETTE = [NAVY, GOLD, GREEN, RED, TEAL, SAGE, MID, "#7B5EA7", "#B8860B", "#4A6FA5"]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Sans", color="#1A1A2E"),
)
_MARGIN = dict(l=10, r=10, t=40, b=10)   # default margin — override per chart as needed

LEGEND_DEFAULT = dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0)
LEGEND_H       = dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h")
_AX = dict(xaxis=dict(showgrid=False, zeroline=False),
           yaxis=dict(showgrid=True, gridcolor="#EDE7D9", zeroline=False))

# ─────────────────────────────────────────────
# DATA LOADING & PREPROCESSING
# ─────────────────────────────────────────────
@st.cache_data(show_spinner="Loading court data…")
def load_data():
    df = pd.read_excel("combined_data.xlsx")

    # Parse hearing date
    df["Hearing Date"] = pd.to_datetime(df["Hearing Date"], dayfirst=True, errors="coerce")
    df["Date_Str"] = df["Hearing Date"].dt.strftime("%d %b %Y")
    df["Month"]    = df["Hearing Date"].dt.strftime("%b %Y")
    df["YearMonth"] = df["Hearing Date"].dt.to_period("M").astype(str)
    df["Week"]     = df["Hearing Date"].dt.isocalendar().week.astype(str)

    # Clean up category groups
    df["Cat_Group"] = df["Category"].str.split(" - ").str[0].str.strip()
    df["Cat_Group"] = df["Cat_Group"].apply(lambda x:
        "Writ Petition"  if str(x).startswith("Writ") else
        "Civil"          if str(x).startswith("Civil") else
        "Criminal"       if str(x).startswith("Crl") or str(x).startswith("Criminal") else
        "Tax / Revenue"  if str(x).startswith("Tax") or str(x) in ["ITR (Income Tax Reference)", "STR (Sales Tax Reference)", "C.Ref. (Customs Reference)"] else
        "ICA"            if str(x).startswith("ICA") or str(x).startswith("I.C.A") else
        "Commercial"     if str(x).startswith("Commercial") or str(x).startswith("C.O.") else
        "First Appeal"   if str(x).startswith("RFA") or str(x).startswith("Regular First Appeal") or str(x).startswith("First Appeal") else
        "Murder Ref."    if str(x).startswith("Murder") else
        "Misc / Others"  if str(x) in ["PLA-Others", "Execution First Appeal", "Execution Application",
                                         "Review Application(Writ-Civil)-Others", "PSLA-Against Acquittal-PPC"] else
        "Misc / Others"
    )

    # Clean remarks - fully decoded
    def map_remark(x):
        raw = str(x).strip().upper() if pd.notna(x) else ""
        if raw == "" or raw == "NAN":               return "Not Specified"
        if raw.startswith("FC") or raw == "AUTO":   return "Final Category (FC)"
        if "STAY" in raw:                           return "Stay Order"
        if raw.startswith("SOC") or raw == "SC":    return "Show Cause"
        if "PART" in raw:                           return "Part-Heard"
        if raw in ["DR", "DAILY ROSTER"]:           return "Daily Roster"
        if raw == "D" or raw == "D*" or raw == "D:": return "Disposal (D)"
        if raw.startswith("RPFC"):                  return "RP + Final Category"
        if raw.startswith("RFC"):                   return "Returned for Compliance"
        if raw.startswith("RP"):                    return "Returned / Adjourned (RP)"
        if raw == "NOMINATED":                      return "Nominated Case"
        if raw == "LIFE":                           return "Life Imprisonment Matter"
        if raw in ["DEH", "DE.H", "E.H"]:          return "Death / Extreme Hardship"
        if raw == "LIMITATION":                     return "Limitation Matter"
        if raw == "WARRANTS":                       return "Warrants Issued"
        if raw in ["COMPROMISE", "COMROMISE"]:      return "Compromise"
        if raw == "RESTORATION":                    return "Restoration"
        if raw == "CITATION":                       return "Citation"
        if raw == "OFFICE REPORT":                  return "Office Report"
        return "Other Notation"

    df["Remark_Group"] = df["Remarks"].apply(map_remark)

    # Extract short justice name
    df["Justice_Short"] = df["Justice"].str.extract(r"Mr\. Justice (.+?) \|")[0]
    df["Justice_Short"] = df["Justice_Short"].fillna(df["Justice"].str[:40])

    # Lawyer count per case
    df["Lawyer_Count"] = df["Lawyer"].fillna("").apply(lambda x: len([l for l in str(x).split("]") if l.strip()]) if "[" in str(x) else (1 if x.strip() else 0))

    return df

df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 0.5rem 0 1.2rem;'>
        <div style='font-size:2.5rem;'>⚖️</div>
        <div style='font-family:"Playfair Display",serif; font-size:1.05rem; color:#C9A84C; font-weight:600;'>LHC Analytics</div>
        <div style='font-size:0.7rem; color:#8A9ABB; letter-spacing:0.1em; text-transform:uppercase;'>Gallup Pakistan</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 🔍 Filters")

    city_opts = ["All"] + sorted(df["Court Location"].dropna().unique().tolist())
    sel_city  = st.selectbox("City / Bench", city_opts)

    bench_opts = ["All"] + sorted(df["Bench Type"].dropna().unique().tolist())
    sel_bench  = st.selectbox("Bench Type", bench_opts)

    cat_opts = ["All"] + sorted(df["Cat_Group"].dropna().unique().tolist())
    sel_cat  = st.selectbox("Case Category", cat_opts)

    legend_opts = ["All"] + sorted(df["Legends"].dropna().unique().tolist())
    sel_legend  = st.selectbox("Cause List Type", legend_opts)

    dates = sorted(df["Hearing Date"].dropna().unique())
    date_min, date_max = dates[0], dates[-1]
    sel_dates = st.date_input(
        "Hearing Date Range",
        value=(date_min.date(), date_max.date()),
        min_value=date_min.date(),
        max_value=date_max.date()
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.68rem; color:#6A7A9B; line-height:1.7;'>
    📊 <b style='color:#C9A84C;'>Data Source</b><br>
    Lahore High Court<br>
    data.lhc.gov.pk<br><br>
    🗓 <b style='color:#C9A84C;'>Period</b><br>
    Feb – Mar 2026<br><br>
    🏢 <b style='color:#C9A84C;'>By</b><br>
    Gallup Pakistan<br>Digital Analytics
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
fdf = df.copy()
if sel_city   != "All": fdf = fdf[fdf["Court Location"] == sel_city]
if sel_bench  != "All": fdf = fdf[fdf["Bench Type"]     == sel_bench]
if sel_cat    != "All": fdf = fdf[fdf["Cat_Group"]       == sel_cat]
if sel_legend != "All": fdf = fdf[fdf["Legends"]         == sel_legend]
if len(sel_dates) == 2:
    d1 = pd.Timestamp(sel_dates[0])
    d2 = pd.Timestamp(sel_dates[1])
    fdf = fdf[(fdf["Hearing Date"] >= d1) & (fdf["Hearing Date"] <= d2)]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
last_updated = df["Hearing Date"].max().strftime("%d %b %Y")
st.markdown(f"""
<div class="lhc-header">
  <div class="lhc-emblem">⚖️</div>
  <div class="lhc-header-text">
    <h1>Lahore High Court<br>Analytics Dashboard</h1>
    <p>Judicial Intelligence Platform — Gallup Pakistan Digital Analytics</p>
  </div>
  <div class="lhc-meta">
    Last Updated<br><b style="color:#C9A84C; font-size:0.95rem;">{last_updated}</b><br><br>
    Filtered Records<br><b style="color:#C9A84C; font-size:0.95rem;">{len(fdf):,}</b>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
total_cases   = fdf["Case#"].nunique()
total_justices= fdf["Justice_Short"].nunique()
total_lawyers = len(set(",".join(fdf["Lawyer"].fillna("")).split(","))) 
total_courts  = fdf["Court"].nunique()
cities_count  = fdf["Court Location"].nunique()
avg_daily     = int(fdf.groupby("Hearing Date").size().mean()) if len(fdf) > 0 else 0

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-label">📁 Total Cases</div>
    <div class="kpi-value">{total_cases:,}</div>
    <div class="kpi-sub">Unique case numbers</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-label">👨‍⚖️ Justices</div>
    <div class="kpi-value">{total_justices}</div>
    <div class="kpi-sub">Active benches</div>
  </div>
  <div class="kpi-card navy">
    <div class="kpi-label">🏛️ Courts</div>
    <div class="kpi-value">{total_courts}</div>
    <div class="kpi-sub">Across {cities_count} cities</div>
  </div>
  <div class="kpi-card red">
    <div class="kpi-label">⚡ Avg Daily Load</div>
    <div class="kpi-value">{avg_daily:,}</div>
    <div class="kpi-sub">Cases per hearing day</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">📋 Stay Matters</div>
    <div class="kpi-value">{len(fdf[fdf['Legends']=='Stay Matters']):,}</div>
    <div class="kpi-sub">{round(len(fdf[fdf['Legends']=='Stay Matters'])/max(len(fdf),1)*100,1)}% of total</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-label">🔁 Old Cases</div>
    <div class="kpi-value">{len(fdf[fdf['Legends']=='Old Cause List']):,}</div>
    <div class="kpi-sub">Pending old cause list</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────
tabs = st.tabs([
    "📊 Overview",
    "📅 Daily Cause List",
    "⚖️ Judge Analysis",
    "📂 Category Deep Dive",
    "🏛️ Court Infrastructure",
    "🌆 City Comparison",
    "👨‍💼 Lawyer Intelligence",
    "🔎 Case Search"
])

# ══════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-title">Case Volume Over Time</div>', unsafe_allow_html=True)

    daily = fdf.groupby("Hearing Date").size().reset_index(name="Cases")
    daily["MA7"] = daily["Cases"].rolling(3, min_periods=1).mean().round(0)

    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Bar(
        x=daily["Hearing Date"], y=daily["Cases"],
        name="Daily Cases", marker_color=NAVY, opacity=0.7
    ))
    fig_timeline.add_trace(go.Scatter(
        x=daily["Hearing Date"], y=daily["MA7"],
        name="3-Day Avg", line=dict(color=GOLD, width=2.5), mode="lines+markers",
        marker=dict(size=5)
    ))
    fig_timeline.update_layout(**CHART_LAYOUT, **_AX, height=280, margin=_MARGIN, title="", showlegend=True,
                                 legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=1.08))
    st.plotly_chart(fig_timeline, width='stretch')

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="section-title">Case Category Mix</div>', unsafe_allow_html=True)
        cat_data = fdf["Cat_Group"].value_counts().reset_index()
        cat_data.columns = ["Category", "Count"]
        cat_data["Pct"] = (cat_data["Count"] / cat_data["Count"].sum() * 100).round(1)
        cat_data["Label"] = cat_data.apply(lambda r: f"{r['Count']:,}  ({r['Pct']}%)", axis=1)
        fig_cat = px.bar(cat_data, x="Count", y="Category", orientation="h",
                         color="Count", color_continuous_scale=[[0, "#C8D4E8"], [1, NAVY]],
                         text="Label",
                         hover_data={"Count": True, "Pct": True})
        fig_cat.update_traces(textposition="outside", cliponaxis=False)
        fig_cat.update_layout(**CHART_LAYOUT, height=320, coloraxis_showscale=False,
                               legend=LEGEND_DEFAULT, margin=dict(l=10, r=180, t=30, b=10))
        fig_cat.update_xaxes(showgrid=False, zeroline=False)
        fig_cat.update_yaxes(categoryorder="total ascending", showgrid=False, zeroline=False)
        st.plotly_chart(fig_cat, width='stretch')

    with c2:
        st.markdown('<div class="section-title">Cause List Distribution</div>', unsafe_allow_html=True)
        leg_data = fdf["Legends"].value_counts().reset_index()
        leg_data.columns = ["Type", "Count"]
        leg_data["Pct"] = (leg_data["Count"] / leg_data["Count"].sum() * 100).round(1)
        # Rename "Unknown" and "Judgement Reserved Cases" for clarity
        leg_data["Type"] = leg_data["Type"].replace({
            "Unknown": "Unclassified",
            "Judgement Reserved Cases": "Judgement Reserved"
        })
        fig_leg = px.pie(leg_data, values="Count", names="Type",
                         color_discrete_sequence=PALETTE, hole=0.52)
        fig_leg.update_traces(
            textposition="inside",
            textinfo="percent",
            textfont_size=11,
            pull=[0.03, 0.02, 0.02, 0.02, 0.05, 0.05],
            insidetextorientation="radial"
        )
        fig_leg.update_layout(**CHART_LAYOUT, height=360, showlegend=True,
                               legend=dict(
                                   bgcolor="rgba(255,255,255,0.85)", borderwidth=0,
                                   orientation="h",
                                   x=0.5, xanchor="center",
                                   y=-0.15, yanchor="top",
                                   font=dict(size=10),
                                   itemwidth=80,
                               ),
                               margin=dict(l=10, r=10, t=20, b=80))
        st.plotly_chart(fig_leg, width='stretch')

    with c3:
        st.markdown('<div class="section-title">Bench Type Breakdown</div>', unsafe_allow_html=True)
        bench_data = fdf["Bench Type"].value_counts().reset_index()
        bench_data.columns = ["Bench", "Count"]
        bench_data["Pct"] = (bench_data["Count"] / bench_data["Count"].sum() * 100).round(1)
        bench_data["Label"] = bench_data.apply(lambda r: f"{r['Count']:,}", axis=1)
        # Shorten bench labels for display
        bench_data["Bench_Short"] = bench_data["Bench"].str.replace(" Bench", "").str.replace("Divisional", "Divisional").str.replace("Special Division", "Sp. Division")
        fig_bench = px.bar(bench_data, x="Bench_Short", y="Count",
                           color="Bench_Short", color_discrete_sequence=PALETTE,
                           text="Label",
                           hover_data={"Bench": True, "Pct": True, "Count": True, "Bench_Short": False})
        fig_bench.update_traces(texttemplate="%{text}", textposition="outside", cliponaxis=False)
        fig_bench.update_layout(**CHART_LAYOUT, height=320, showlegend=False, legend=LEGEND_DEFAULT,
                                 margin=dict(l=10, r=10, t=30, b=60))
        fig_bench.update_xaxes(showgrid=False, zeroline=False, tickangle=-15)
        fig_bench.update_yaxes(showgrid=True, gridcolor="#EDE7D9", zeroline=False)
        st.plotly_chart(fig_bench, width='stretch')

    c4, c5 = st.columns(2)
    with c4:
        st.markdown('<div class="section-title">Case Remarks / Status Breakdown</div>', unsafe_allow_html=True)
        rem_data = fdf["Remark_Group"].value_counts().reset_index()
        rem_data.columns = ["Remark", "Count"]

        # Merge "Other Notation" (from map_remark) into one clean bucket before display
        rem_data["Remark"] = rem_data["Remark"].replace({
            "Other Notation":  "Misc. Notations",
            "Other Notations": "Misc. Notations",
        })
        rem_data = rem_data.groupby("Remark", as_index=False)["Count"].sum()
        rem_data = rem_data.sort_values("Count", ascending=False).reset_index(drop=True)

        rem_data["Pct"] = (rem_data["Count"] / rem_data["Count"].sum() * 100).round(1)
        rem_data["Label"] = rem_data["Pct"].apply(lambda x: f"{x}%")

        # Keep top 8, group any remainder into Misc. Notations
        if len(rem_data) > 8:
            top8 = rem_data.head(8).copy()
            rest = rem_data.iloc[8:]
            misc_row = top8[top8["Remark"] == "Misc. Notations"]
            if len(misc_row):
                # Already in top 8 — just add the rest to it
                idx = misc_row.index[0]
                top8.at[idx, "Count"] += rest["Count"].sum()
            else:
                extra = rest["Count"].sum()
                extra_pct = rest["Pct"].sum().round(1)
                top8 = pd.concat([top8, pd.DataFrame([{
                    "Remark": "Misc. Notations", "Count": extra,
                    "Pct": extra_pct, "Label": f"{extra_pct}%"
                }])], ignore_index=True)
            # Recalculate pct and label after merging
            top8["Pct"]  = (top8["Count"] / top8["Count"].sum() * 100).round(1)
            top8["Label"] = top8["Pct"].apply(lambda x: f"{x}%")
            rem_data = top8

        fig_rem = px.bar(rem_data, x="Remark", y="Pct",
                         color="Remark", color_discrete_sequence=PALETTE,
                         text="Label",
                         labels={"Pct": "% of Cases", "Count": "Cases", "Remark": ""},
                         hover_data={"Count": True, "Pct": True})
        fig_rem.update_traces(textposition="outside", cliponaxis=False,
                               textfont=dict(size=10))
        fig_rem.update_layout(**CHART_LAYOUT, height=380, showlegend=False, legend=LEGEND_DEFAULT,
                               margin=dict(l=10, r=10, t=50, b=160))
        fig_rem.update_xaxes(showgrid=False, zeroline=False,
                              tickangle=-40, tickfont=dict(size=9),
                              automargin=True, title_text="")
        fig_rem.update_yaxes(showgrid=True, gridcolor="#EDE7D9", zeroline=False)
        fig_rem.add_annotation(
            text="<b>Key:</b>  FC = Final Category  |  D = Disposal  |  RP = Returned/Adjourned  |  SOC = Show Cause  |  Misc. = Low-frequency notations grouped",
            xref="paper", yref="paper", x=0, y=-0.62,
            showarrow=False, font=dict(size=8.5, color="#777"), align="left"
        )
        st.plotly_chart(fig_rem, width='stretch')

    with c5:
        st.markdown('<div class="section-title">Hearing Day Patterns</div>', unsafe_allow_html=True)
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        day_data = fdf["Hearing Day"].value_counts().reindex(day_order).fillna(0).reset_index()
        day_data.columns = ["Day", "Count"]
        day_data["Pct"] = (day_data["Count"] / day_data["Count"].sum() * 100).round(1)
        day_data["Label"] = day_data.apply(lambda r: f"{int(r['Count']):,}\n({r['Pct']}%)", axis=1)
        day_data["Day_Short"] = day_data["Day"].str[:3]  # Mon, Tue etc.
        fig_day = px.bar(day_data, x="Day", y="Count",
                         color="Count", color_continuous_scale=[[0, "#C8D4E8"], [1, NAVY]],
                         text="Label",
                         hover_data={"Day": True, "Count": True, "Pct": True})
        fig_day.update_traces(textposition="outside", cliponaxis=False,
                               textfont=dict(size=10))
        fig_day.update_layout(**CHART_LAYOUT, height=340, coloraxis_showscale=False,
                               legend=LEGEND_DEFAULT, margin=dict(l=10, r=10, t=40, b=20))
        fig_day.update_xaxes(showgrid=False, zeroline=False)
        fig_day.update_yaxes(showgrid=True, gridcolor="#EDE7D9", zeroline=False,
                              title="Number of Cases")
        st.plotly_chart(fig_day, width='stretch')

# ══════════════════════════════════════════════
# TAB 2 — DAILY CAUSE LIST
# ══════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-title">📋 Daily Hearing Schedule</div>', unsafe_allow_html=True)

    col_d1, col_d2, col_d3 = st.columns([2, 2, 2])
    with col_d1:
        avail_dates = sorted(fdf["Hearing Date"].dropna().unique())
        if avail_dates:
            sel_day = st.selectbox("Select Hearing Date",
                                   options=avail_dates,
                                   format_func=lambda x: x.strftime("%A, %d %b %Y"),
                                   index=len(avail_dates)-1)
        else:
            st.warning("No dates in current filter."); sel_day = None
    with col_d2:
        city_f = st.selectbox("Filter by City", ["All"] + sorted(fdf["Court Location"].unique().tolist()), key="dl_city")
    with col_d3:
        bench_f = st.selectbox("Filter by Bench", ["All"] + sorted(fdf["Bench Type"].unique().tolist()), key="dl_bench")

    if sel_day:
        day_df = fdf[fdf["Hearing Date"] == sel_day].copy()
        if city_f  != "All": day_df = day_df[day_df["Court Location"] == city_f]
        if bench_f != "All": day_df = day_df[day_df["Bench Type"] == bench_f]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Cases", f"{len(day_df):,}")
        m2.metric("Courts Active", f"{day_df['Court'].nunique()}")
        m3.metric("Justices on Bench", f"{day_df['Justice_Short'].nunique()}")
        m4.metric("Stay Matters", f"{len(day_df[day_df['Legends']=='Stay Matters']):,}")

        cl1, cl2 = st.columns(2)
        with cl1:
            st.markdown('<div class="section-title">Cases by Court Room</div>', unsafe_allow_html=True)
            court_day = day_df["Justice_Short"].value_counts().head(15).reset_index()
            court_day.columns = ["Justice", "Cases"]
            fig_cd = px.bar(court_day, y="Justice", x="Cases", orientation="h",
                            color="Cases", color_continuous_scale=[[0,"#C8D4E8"],[1,NAVY]],
                            text="Cases")
            fig_cd.update_traces(textposition="outside")
            fig_cd.update_layout(**CHART_LAYOUT, **_AX, height=380, margin=_MARGIN, coloraxis_showscale=False, legend=LEGEND_DEFAULT)
            fig_cd.update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_cd, width='stretch')

        with cl2:
            st.markdown('<div class="section-title">Case Type Breakdown</div>', unsafe_allow_html=True)
            type_day = day_df["Legends"].value_counts().reset_index()
            type_day.columns = ["Type", "Count"]
            fig_td = px.pie(type_day, values="Count", names="Type",
                            color_discrete_sequence=PALETTE, hole=0.5)
            fig_td.update_traces(textinfo="label+value", pull=[0.04]*len(type_day))
            fig_td.update_layout(**CHART_LAYOUT, **_AX, height=380, margin=_MARGIN, showlegend=True, legend=LEGEND_DEFAULT)
            st.plotly_chart(fig_td, width='stretch')

        st.markdown('<div class="section-title">Hearing Schedule Detail</div>', unsafe_allow_html=True)
        display_cols = ["Court Location", "Bench Type", "Justice_Short", "Court", "Legends", "Cat_Group", "Case#", "Title", "Lawyer", "Remark_Group"]
        show = day_df[display_cols].rename(columns={
            "Court Location": "City", "Justice_Short": "Justice",
            "Cat_Group": "Category", "Remark_Group": "Status"
        }).reset_index(drop=True)
        st.dataframe(show, width='stretch', height=350)

# ══════════════════════════════════════════════
# TAB 3 — JUDGE ANALYSIS
# ══════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-title">⚖️ Judicial Workload & Performance</div>', unsafe_allow_html=True)

    judge_df = fdf.groupby("Justice_Short").agg(
        Total_Cases=("Case#", "count"),
        Unique_Cases=("Case#", "nunique"),
        Hearing_Days=("Hearing Date", "nunique"),
        Cities=("Court Location", "nunique"),
        Stay_Matters=("Legends", lambda x: (x=="Stay Matters").sum()),
        Old_Cases=("Legends", lambda x: (x=="Old Cause List").sum()),
    ).reset_index()
    judge_df["Cases_Per_Day"] = (judge_df["Total_Cases"] / judge_df["Hearing_Days"]).round(1)
    judge_df["Stay_Pct"] = (judge_df["Stay_Matters"] / judge_df["Total_Cases"] * 100).round(1)

    jc1, jc2 = st.columns([3, 2])
    with jc1:
        st.markdown('<div class="section-title">Top 20 Judges by Caseload</div>', unsafe_allow_html=True)
        top_j = judge_df.nlargest(20, "Total_Cases")
        fig_j = px.bar(top_j, y="Justice_Short", x="Total_Cases", orientation="h",
                       color="Cases_Per_Day",
                       color_continuous_scale=[[0,"#C8D4E8"],[0.5,GOLD],[1,RED]],
                       text="Total_Cases",
                       labels={"Total_Cases": "Total Cases", "Cases_Per_Day": "Avg/Day"},
                       hover_data=["Hearing_Days", "Stay_Pct"])
        fig_j.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_j.update_layout(**CHART_LAYOUT, **_AX, height=520, margin=_MARGIN, coloraxis_colorbar=dict(title="Avg/Day"),
                             legend=LEGEND_DEFAULT)
        fig_j.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_j, width='stretch')

    with jc2:
        st.markdown('<div class="section-title">Workload Efficiency Bubble</div>', unsafe_allow_html=True)
        top20 = judge_df.nlargest(20, "Total_Cases")
        fig_bub = px.scatter(top20, x="Hearing_Days", y="Cases_Per_Day",
                             size="Total_Cases", color="Stay_Pct",
                             hover_name="Justice_Short",
                             color_continuous_scale=[[0,GREEN],[0.5,GOLD],[1,RED]],
                             labels={"Hearing_Days": "Hearing Days",
                                     "Cases_Per_Day": "Cases per Day",
                                     "Stay_Pct": "Stay %"})
        fig_bub.update_layout(**CHART_LAYOUT, **_AX, height=520, margin=_MARGIN, legend=LEGEND_DEFAULT)
        st.plotly_chart(fig_bub, width='stretch')

    st.markdown('<div class="section-title">Judge-wise Case Category Distribution (Top 10)</div>', unsafe_allow_html=True)
    top10_j = judge_df.nlargest(10, "Total_Cases")["Justice_Short"].tolist()
    jcat = fdf[fdf["Justice_Short"].isin(top10_j)].groupby(["Justice_Short","Cat_Group"]).size().reset_index(name="Count")
    fig_jcat = px.bar(jcat, x="Justice_Short", y="Count", color="Cat_Group",
                      barmode="stack", color_discrete_sequence=PALETTE,
                      labels={"Justice_Short": "Justice", "Count": "Cases", "Cat_Group": "Category"})
    fig_jcat.update_layout(**CHART_LAYOUT, **_AX, height=360, margin=_MARGIN, xaxis_tickangle=-25,
                            legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=-0.25))
    st.plotly_chart(fig_jcat, width='stretch')

    st.markdown('<div class="section-title">Most Repeatedly Heard Cases (Per Justice)</div>', unsafe_allow_html=True)
    rep_cases = fdf.groupby(["Title", "Justice_Short"]).size().reset_index(name="Hearings")
    rep_cases = rep_cases.nlargest(15, "Hearings")
    rep_cases["Short_Title"] = rep_cases["Title"].str[:55] + "…"
    fig_rep = px.bar(rep_cases, y="Short_Title", x="Hearings", orientation="h",
                     color="Justice_Short", color_discrete_sequence=PALETTE,
                     text="Hearings")
    fig_rep.update_traces(textposition="outside")
    fig_rep.update_layout(**CHART_LAYOUT, **_AX, height=450, margin=_MARGIN,
                           showlegend=True, legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=-0.22))
    fig_rep.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig_rep, width='stretch')

    with st.expander("📊 Full Judge Statistics Table"):
        st.dataframe(judge_df.sort_values("Total_Cases", ascending=False).reset_index(drop=True),
                     width='stretch')

# ══════════════════════════════════════════════
# TAB 4 — CATEGORY DEEP DIVE
# ══════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-title">📂 Case Category Intelligence</div>', unsafe_allow_html=True)

    # ── Top-level category volume
    st.markdown('<div class="section-title">Category Volume Overview</div>', unsafe_allow_html=True)
    cat_vol = fdf["Cat_Group"].value_counts().reset_index()
    cat_vol.columns = ["Category", "Count"]
    cat_vol["Pct"] = (cat_vol["Count"] / cat_vol["Count"].sum() * 100).round(1)
    cat_vol["Label"] = cat_vol.apply(lambda r: f"{r['Count']:,}  ({r['Pct']}%)", axis=1)

    fig_cat_vol = px.bar(cat_vol, x="Count", y="Category", orientation="h",
                         color="Count", color_continuous_scale=[[0, "#C8D4E8"], [1, NAVY]],
                         text="Label")
    fig_cat_vol.update_traces(textposition="outside", cliponaxis=False)
    fig_cat_vol.update_layout(**CHART_LAYOUT, height=340, coloraxis_showscale=False,
                               margin=dict(l=10, r=210, t=30, b=10))
    fig_cat_vol.update_xaxes(showgrid=False, zeroline=False)
    fig_cat_vol.update_yaxes(categoryorder="total ascending", showgrid=False, zeroline=False)
    st.plotly_chart(fig_cat_vol, width='stretch')

    # ── Writ vs Other: Proportion over time
    st.markdown('<div class="section-title">Writ vs Other Cases — Proportion Over Time</div>', unsafe_allow_html=True)

    # Use a local copy to avoid SettingWithCopyWarning on filtered fdf
    _writ_df = fdf.copy()
    _writ_df["Writ_Flag"] = _writ_df["Cat_Group"].apply(lambda x: "Writ Petition" if x == "Writ Petition" else "Other")
    writ_time = _writ_df.groupby(["Hearing Date", "Writ_Flag"]).size().reset_index(name="Count")
    writ_pivot = writ_time.pivot(index="Hearing Date", columns="Writ_Flag", values="Count").fillna(0)
    if "Writ Petition" not in writ_pivot.columns: writ_pivot["Writ Petition"] = 0
    if "Other" not in writ_pivot.columns: writ_pivot["Other"] = 0
    writ_pivot["Total"] = writ_pivot["Writ Petition"] + writ_pivot["Other"]
    writ_pivot["Writ_Pct"] = (writ_pivot["Writ Petition"] / writ_pivot["Total"] * 100).round(1)
    writ_pivot["Other_Pct"] = (writ_pivot["Other"] / writ_pivot["Total"] * 100).round(1)
    writ_pivot = writ_pivot.reset_index()

    fig_writ_trend = go.Figure()
    fig_writ_trend.add_trace(go.Scatter(
        x=writ_pivot["Hearing Date"], y=writ_pivot["Writ_Pct"],
        name="Writ Petition %", fill="tozeroy",
        line=dict(color=NAVY, width=2), fillcolor="rgba(27,43,75,0.18)",
        mode="lines+markers", marker=dict(size=5)
    ))
    fig_writ_trend.add_trace(go.Scatter(
        x=writ_pivot["Hearing Date"], y=writ_pivot["Other_Pct"],
        name="Other Cases %", fill="tozeroy",
        line=dict(color=GOLD, width=2), fillcolor="rgba(201,168,76,0.15)",
        mode="lines+markers", marker=dict(size=5)
    ))
    fig_writ_trend.update_layout(**CHART_LAYOUT, **_AX, height=280, margin=_MARGIN,
                                  yaxis_title="% of Daily Cases",
                                  legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=1.08))
    st.plotly_chart(fig_writ_trend, width='stretch')

    # ── Writ vs Other stacked bar over time (absolute count)
    fig_writ_stack = go.Figure()
    fig_writ_stack.add_trace(go.Bar(
        x=writ_pivot["Hearing Date"], y=writ_pivot["Writ Petition"],
        name="Writ Petition", marker_color=NAVY
    ))
    fig_writ_stack.add_trace(go.Bar(
        x=writ_pivot["Hearing Date"], y=writ_pivot["Other"],
        name="Other Cases", marker_color=GOLD
    ))
    fig_writ_stack.update_layout(**CHART_LAYOUT, **_AX, height=250, margin=_MARGIN,
                                  barmode="stack", yaxis_title="Cases",
                                  legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=1.08))
    st.plotly_chart(fig_writ_stack, width='stretch')

    # ── Which judge hears most Writ Petitions
    st.markdown('<div class="section-title">Which Judge Hears Most Writ Petitions</div>', unsafe_allow_html=True)

    writ_judge = fdf[fdf["Cat_Group"] == "Writ Petition"].groupby("Justice_Short").size().reset_index(name="Writ_Cases")
    all_judge  = fdf.groupby("Justice_Short").size().reset_index(name="Total_Cases")
    judge_writ = writ_judge.merge(all_judge, on="Justice_Short")
    judge_writ["Writ_Pct"] = (judge_writ["Writ_Cases"] / judge_writ["Total_Cases"] * 100).round(1)
    judge_writ = judge_writ.sort_values("Writ_Cases", ascending=False).head(20)

    wc1, wc2 = st.columns(2)
    with wc1:
        st.markdown("**Top 20 Judges by Writ Volume**", unsafe_allow_html=False)
        fig_wj_vol = px.bar(judge_writ, y="Justice_Short", x="Writ_Cases", orientation="h",
                            color="Writ_Cases",
                            color_continuous_scale=[[0, "#C8D4E8"], [1, NAVY]],
                            text="Writ_Cases")
        fig_wj_vol.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_wj_vol.update_layout(**CHART_LAYOUT, **_AX, height=500, margin=_MARGIN,
                                  coloraxis_showscale=False)
        fig_wj_vol.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_wj_vol, width='stretch')

    with wc2:
        st.markdown("**Writ % of Total Caseload (Top 20 by Writ Volume)**", unsafe_allow_html=False)
        fig_wj_pct = px.bar(judge_writ.sort_values("Writ_Pct", ascending=False),
                            y="Justice_Short", x="Writ_Pct", orientation="h",
                            color="Writ_Pct",
                            color_continuous_scale=[[0, "#C8D4E8"], [0.6, GOLD], [1, RED]],
                            text="Writ_Pct",
                            labels={"Writ_Pct": "% Writ"})
        fig_wj_pct.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_wj_pct.update_layout(**CHART_LAYOUT, **_AX, height=500, margin=_MARGIN,
                                  coloraxis_showscale=False)
        fig_wj_pct.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_wj_pct, width='stretch')

    # ── Bench differences for Writ vs Other
    st.markdown('<div class="section-title">Bench Type Differences — Writ vs Other Cases</div>', unsafe_allow_html=True)

    bench_writ = _writ_df.groupby(["Bench Type", "Writ_Flag"]).size().reset_index(name="Count")
    bench_writ_pct = bench_writ.copy()
    bench_writ_pct["Pct"] = bench_writ_pct.groupby("Bench Type")["Count"].transform(lambda x: x / x.sum() * 100).round(1)

    bc1, bc2 = st.columns(2)
    with bc1:
        fig_bw_abs = px.bar(bench_writ, x="Bench Type", y="Count", color="Writ_Flag",
                            barmode="group", color_discrete_map={"Writ Petition": NAVY, "Other": GOLD},
                            text="Count",
                            labels={"Writ_Flag": "Type"})
        fig_bw_abs.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_bw_abs.update_layout(**CHART_LAYOUT, **_AX, height=320, margin=dict(l=10,r=10,t=40,b=80),
                                  title="Absolute Count by Bench",
                                  legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=-0.3),
                                  xaxis_tickangle=-15)
        st.plotly_chart(fig_bw_abs, width='stretch')

    with bc2:
        fig_bw_pct = px.bar(bench_writ_pct, x="Bench Type", y="Pct", color="Writ_Flag",
                            barmode="stack", color_discrete_map={"Writ Petition": NAVY, "Other": GOLD},
                            text="Pct",
                            labels={"Writ_Flag": "Type", "Pct": "%"})
        fig_bw_pct.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
        fig_bw_pct.update_layout(**CHART_LAYOUT, **_AX, height=320, margin=dict(l=10,r=10,t=40,b=80),
                                  title="% Composition by Bench",
                                  legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=-0.3),
                                  xaxis_tickangle=-15)
        st.plotly_chart(fig_bw_pct, width='stretch')

    # ── Sub-category drill down (Writ types)
    st.markdown('<div class="section-title">Writ Petition Sub-categories (Top 20)</div>', unsafe_allow_html=True)
    writ_sub = fdf[fdf["Cat_Group"] == "Writ Petition"]["Category"].value_counts().head(20).reset_index()
    writ_sub.columns = ["Sub-Category", "Count"]
    writ_sub["Pct"] = (writ_sub["Count"] / writ_sub["Count"].sum() * 100).round(1)
    writ_sub["Label"] = writ_sub.apply(lambda r: f"{r['Count']:,} ({r['Pct']}%)", axis=1)
    fig_wsub = px.bar(writ_sub, x="Count", y="Sub-Category", orientation="h",
                      color="Count", color_continuous_scale=[[0, "#C8D4E8"], [1, NAVY]],
                      text="Label")
    fig_wsub.update_traces(textposition="outside", cliponaxis=False)
    fig_wsub.update_layout(**CHART_LAYOUT, height=520, coloraxis_showscale=False,
                            margin=dict(l=10, r=220, t=30, b=10))
    fig_wsub.update_xaxes(showgrid=False, zeroline=False)
    fig_wsub.update_yaxes(categoryorder="total ascending", showgrid=False, zeroline=False, tickfont=dict(size=10))
    st.plotly_chart(fig_wsub, width='stretch')

    # ── Other top sub-categories selector
    st.markdown('<div class="section-title">Drill into Any Category — Sub-type Breakdown</div>', unsafe_allow_html=True)
    sel_drill_cat = st.selectbox("Select Category to Drill Down", sorted(fdf["Cat_Group"].dropna().unique()), key="drill_cat")
    drill_sub = fdf[fdf["Cat_Group"] == sel_drill_cat]["Category"].value_counts().head(15).reset_index()
    drill_sub.columns = ["Sub-Category", "Count"]
    drill_sub["Pct"] = (drill_sub["Count"] / drill_sub["Count"].sum() * 100).round(1)
    drill_sub["Label"] = drill_sub.apply(lambda r: f"{r['Count']:,} ({r['Pct']}%)", axis=1)
    fig_drill = px.bar(drill_sub, x="Count", y="Sub-Category", orientation="h",
                       color="Count", color_continuous_scale=[[0, "#C8D4E8"], [1, GREEN]],
                       text="Label")
    fig_drill.update_traces(textposition="outside", cliponaxis=False)
    fig_drill.update_layout(**CHART_LAYOUT, height=max(300, len(drill_sub) * 28 + 60),
                             coloraxis_showscale=False, margin=dict(l=10, r=220, t=30, b=10))
    fig_drill.update_xaxes(showgrid=False, zeroline=False)
    fig_drill.update_yaxes(categoryorder="total ascending", showgrid=False, zeroline=False, tickfont=dict(size=10))
    st.plotly_chart(fig_drill, width='stretch')

    # ── Category by City heatmap (% within city)
    st.markdown('<div class="section-title">Category Mix by City (% within each city)</div>', unsafe_allow_html=True)
    cat_city_pct = fdf.groupby(["Court Location", "Cat_Group"]).size().unstack(fill_value=0)
    cat_city_pct = cat_city_pct.div(cat_city_pct.sum(axis=1), axis=0) * 100
    cat_city_pct = cat_city_pct.round(1)
    fig_cc_heat = px.imshow(cat_city_pct,
                             color_continuous_scale=[[0, CREAM], [0.4, GOLD], [1, NAVY]],
                             aspect="auto", text_auto=True,
                             labels=dict(color="% of Cases"))
    fig_cc_heat.update_layout(**CHART_LAYOUT, height=300, margin=_MARGIN)
    st.plotly_chart(fig_cc_heat, width='stretch')

    # ── Monthly category trend
    st.markdown('<div class="section-title">Category Trend by Month</div>', unsafe_allow_html=True)
    cat_monthly = fdf.groupby(["YearMonth", "Cat_Group"]).size().reset_index(name="Count")
    fig_cat_month = px.line(cat_monthly, x="YearMonth", y="Count", color="Cat_Group",
                             color_discrete_sequence=PALETTE, markers=True,
                             labels={"YearMonth": "Month", "Cat_Group": "Category"})
    fig_cat_month.update_layout(**CHART_LAYOUT, **_AX, height=360, margin=_MARGIN,
                                  legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=-0.2))
    fig_cat_month.update_xaxes(tickangle=-20)
    st.plotly_chart(fig_cat_month, width='stretch')


# ══════════════════════════════════════════════
# TAB 5 — COURT INFRASTRUCTURE  (was tab 4)
# ══════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-title">🏛️ Court Block & Room Utilization</div>', unsafe_allow_html=True)

    ic1, ic2 = st.columns(2)
    with ic1:
        st.markdown('<div class="section-title">Cases by City</div>', unsafe_allow_html=True)
        city_data = fdf["Court Location"].value_counts().reset_index()
        city_data.columns = ["City", "Cases"]
        city_data["Pct"] = (city_data["Cases"]/city_data["Cases"].sum()*100).round(1)
        fig_city_inf = px.pie(city_data, values="Cases", names="City",
                              color_discrete_map={"Lahore": NAVY, "Multan": GOLD,
                                                  "Bahawalpur": GREEN, "Rawalpindi": RED},
                              hole=0.55)
        fig_city_inf.update_traces(textinfo="label+percent+value", pull=[0.04]*4)
        fig_city_inf.update_layout(**CHART_LAYOUT, **_AX, height=340, margin=_MARGIN, showlegend=False, legend=LEGEND_DEFAULT)
        st.plotly_chart(fig_city_inf, width='stretch')

    with ic2:
        st.markdown('<div class="section-title">Bench Type by City</div>', unsafe_allow_html=True)
        bench_city = fdf.groupby(["Court Location","Bench Type"]).size().reset_index(name="Count")
        fig_bc = px.bar(bench_city, x="Court Location", y="Count", color="Bench Type",
                        barmode="group", color_discrete_sequence=PALETTE,
                        text="Count")
        fig_bc.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_bc.update_layout(**CHART_LAYOUT, **_AX, height=340, margin=_MARGIN, legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=-0.25))
        st.plotly_chart(fig_bc, width='stretch')

    st.markdown('<div class="section-title">Top 15 Busiest Courts</div>', unsafe_allow_html=True)
    court_load = fdf.groupby(["Court Location","Court"]).agg(
        Cases=("Case#","count"),
        Justices=("Justice_Short","nunique"),
        Hearing_Days=("Hearing Date","nunique")
    ).reset_index()
    court_load["Cases_Per_Day"] = (court_load["Cases"]/court_load["Hearing_Days"]).round(1)
    top_courts = court_load.nlargest(15,"Cases")
    top_courts["Short_Court"] = top_courts["Court"].str[:40]

    fig_courts = px.bar(top_courts, y="Short_Court", x="Cases", orientation="h",
                        color="Court Location",
                        color_discrete_map={"Lahore": NAVY,"Multan": GOLD,"Bahawalpur": GREEN,"Rawalpindi": RED},
                        text="Cases", hover_data=["Cases_Per_Day","Justices"])
    fig_courts.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig_courts.update_layout(**CHART_LAYOUT, **_AX, height=450, margin=_MARGIN,
                              legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, title="City", orientation="h", y=-0.15))
    fig_courts.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig_courts, width='stretch')

    st.markdown('<div class="section-title">Category Heatmap by City & Bench</div>', unsafe_allow_html=True)
    heat = fdf.groupby(["Court Location","Cat_Group"]).size().unstack(fill_value=0)
    fig_heat = px.imshow(heat, color_continuous_scale=[[0,CREAM],[0.4,GOLD],[1,NAVY]],
                         aspect="auto", text_auto=True)
    fig_heat.update_layout(**CHART_LAYOUT, **_AX, height=280, margin=_MARGIN, legend=LEGEND_DEFAULT)
    st.plotly_chart(fig_heat, width='stretch')

# ══════════════════════════════════════════════
# TAB 6 — CITY COMPARISON  (was tab 5)
# ══════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-title">🌆 City-wise Comparative Analysis</div>', unsafe_allow_html=True)

    city_summary = fdf.groupby("Court Location").agg(
        Total_Cases=("Case#","count"),
        Unique_Cases=("Case#","nunique"),
        Justices=("Justice_Short","nunique"),
        Courts=("Court","nunique"),
        Hearing_Days=("Hearing Date","nunique"),
        Stay=("Legends", lambda x: (x=="Stay Matters").sum()),
        Old=("Legends",  lambda x: (x=="Old Cause List").sum()),
    ).reset_index()
    city_summary["Avg_Daily"] = (city_summary["Total_Cases"]/city_summary["Hearing_Days"]).round(0)
    city_summary["Stay_Pct"] = (city_summary["Stay"]/city_summary["Total_Cases"]*100).round(1)

    for _, row in city_summary.iterrows():
        pass  # just pre-compute

    cc1, cc2 = st.columns(2)
    with cc1:
        fig_ccomp = px.bar(city_summary, x="Court Location", y=["Total_Cases","Stay","Old"],
                           barmode="group", color_discrete_sequence=[NAVY, GOLD, GREEN],
                           labels={"value":"Cases","variable":"Type","Court Location":"City"})
        fig_ccomp.update_layout(**CHART_LAYOUT, **_AX, height=300, margin=_MARGIN, title="Case Volume Comparison",
                                  legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=-0.25))
        st.plotly_chart(fig_ccomp, width='stretch')

    with cc2:
        fig_radar_data = city_summary.set_index("Court Location")[["Justices","Courts","Hearing_Days","Stay_Pct"]].T
        fig_cbar2 = px.bar(city_summary, x="Court Location", y="Avg_Daily",
                           color="Court Location",
                           color_discrete_map={"Lahore":NAVY,"Multan":GOLD,"Bahawalpur":GREEN,"Rawalpindi":RED},
                           text="Avg_Daily")
        fig_cbar2.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig_cbar2.update_layout(**CHART_LAYOUT, **_AX, height=300, margin=_MARGIN, title="Avg Cases Per Hearing Day", showlegend=False, legend=LEGEND_DEFAULT)
        st.plotly_chart(fig_cbar2, width='stretch')

    st.markdown('<div class="section-title">Timeline by City</div>', unsafe_allow_html=True)
    city_time = fdf.groupby(["Hearing Date","Court Location"]).size().reset_index(name="Cases")
    fig_city_time = px.line(city_time, x="Hearing Date", y="Cases", color="Court Location",
                            color_discrete_map={"Lahore":NAVY,"Multan":GOLD,"Bahawalpur":GREEN,"Rawalpindi":RED},
                            markers=True)
    fig_city_time.update_layout(**CHART_LAYOUT, **_AX, height=320, margin=_MARGIN,
                                  legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=-0.2))
    st.plotly_chart(fig_city_time, width='stretch')

    st.markdown('<div class="section-title">Category Distribution by City</div>', unsafe_allow_html=True)
    city_cat = fdf.groupby(["Court Location","Cat_Group"]).size().reset_index(name="Count")
    city_cat["Pct"] = city_cat.groupby("Court Location")["Count"].transform(lambda x: x/x.sum()*100).round(1)
    fig_city_cat = px.bar(city_cat, x="Court Location", y="Pct", color="Cat_Group",
                          barmode="stack", color_discrete_sequence=PALETTE,
                          text="Pct", labels={"Pct":"%","Court Location":"City","Cat_Group":"Category"})
    fig_city_cat.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    fig_city_cat.update_layout(**CHART_LAYOUT, **_AX, height=320, margin=_MARGIN, legend=dict(bgcolor="rgba(255,255,255,0.85)", borderwidth=0, orientation="h", y=-0.2))
    st.plotly_chart(fig_city_cat, width='stretch')

    st.markdown('<div class="section-title">City Summary Table</div>', unsafe_allow_html=True)
    st.dataframe(city_summary.rename(columns={
        "Court Location":"City","Total_Cases":"Total Cases","Unique_Cases":"Unique Cases",
        "Hearing_Days":"Hearing Days","Avg_Daily":"Avg/Day","Stay_Pct":"Stay %"
    }), width='stretch')

# ══════════════════════════════════════════════
# TAB 7 — LAWYER INTELLIGENCE  (was tab 6)
# ══════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-title">👨‍💼 Lawyer Activity Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-box">⚠️ Lawyer data may include multiple lawyers per row. Counts reflect case appearances, not unique individuals.</div>', unsafe_allow_html=True)

    lawyer_exp = fdf[["Lawyer","Court Location","Cat_Group","Legends","Hearing Date","Justice_Short"]].copy()
    lawyer_exp = lawyer_exp.dropna(subset=["Lawyer"])
    lawyer_exp = lawyer_exp[lawyer_exp["Lawyer"].str.strip() != ""]

    # Simple single-lawyer extraction (first named lawyer per row)
    lawyer_exp["Primary_Lawyer"] = lawyer_exp["Lawyer"].apply(
        lambda x: str(x).split("]")[-1].strip() if "]" in str(x) else str(x).split(",")[0].strip()
    )
    lawyer_exp["Primary_Lawyer"] = lawyer_exp["Primary_Lawyer"].str.strip().str[:60]
    lawyer_exp = lawyer_exp[lawyer_exp["Primary_Lawyer"].str.len() > 2]

    top_lawyers = lawyer_exp["Primary_Lawyer"].value_counts().head(25).reset_index()
    top_lawyers.columns = ["Lawyer", "Cases"]

    lc1, lc2 = st.columns([3,2])
    with lc1:
        st.markdown('<div class="section-title">Top 25 Most Active Lawyers</div>', unsafe_allow_html=True)
        fig_law = px.bar(top_lawyers.head(20), y="Lawyer", x="Cases", orientation="h",
                         color="Cases", color_continuous_scale=[[0,"#C8D4E8"],[1,NAVY]],
                         text="Cases")
        fig_law.update_traces(textposition="outside")
        fig_law.update_layout(**CHART_LAYOUT, **_AX, height=550, margin=_MARGIN, coloraxis_showscale=False, legend=LEGEND_DEFAULT)
        fig_law.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_law, width='stretch')

    with lc2:
        st.markdown('<div class="section-title">Lawyer Activity by City</div>', unsafe_allow_html=True)
        law_city = lawyer_exp.groupby("Court Location")["Primary_Lawyer"].nunique().reset_index()
        law_city.columns = ["City", "Unique Lawyers"]
        fig_lc = px.bar(law_city, x="City", y="Unique Lawyers",
                        color="City",
                        color_discrete_map={"Lahore":NAVY,"Multan":GOLD,"Bahawalpur":GREEN,"Rawalpindi":RED},
                        text="Unique Lawyers")
        fig_lc.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_lc.update_layout(**CHART_LAYOUT, **_AX, height=280, margin=_MARGIN, showlegend=False, legend=LEGEND_DEFAULT)
        st.plotly_chart(fig_lc, width='stretch')

        st.markdown('<div class="section-title">Category Focus (Top Lawyers)</div>', unsafe_allow_html=True)
        top5_lawyers = top_lawyers["Lawyer"].head(5).tolist()
        law_cat = lawyer_exp[lawyer_exp["Primary_Lawyer"].isin(top5_lawyers)].groupby(
            ["Primary_Lawyer","Cat_Group"]).size().reset_index(name="Count")
        fig_lcat = px.bar(law_cat, x="Primary_Lawyer", y="Count", color="Cat_Group",
                          barmode="stack", color_discrete_sequence=PALETTE,
                          labels={"Primary_Lawyer": "", "Cat_Group": "Category"})  # empty x-axis title
        fig_lcat.update_layout(**CHART_LAYOUT, **_AX, height=400,
                                margin=dict(l=10, r=10, t=30, b=200),
                                xaxis_tickangle=-40,
                                legend=dict(bgcolor="rgba(255,255,255,0.9)", borderwidth=1,
                                            bordercolor="#DDD",
                                            orientation="h", x=0.5, xanchor="center",
                                            y=-0.72, yanchor="top", font=dict(size=9),
                                            title=dict(text="Category  ", side="left", font=dict(size=9))))
        fig_lcat.update_xaxes(title_text="")   # remove "Lawyer" axis label entirely
        st.plotly_chart(fig_lcat, width='stretch')

    st.markdown('<div class="section-title">Lawyer Search</div>', unsafe_allow_html=True)
    search_name = st.text_input("🔍 Search Lawyer by Name (partial match OK)", placeholder="e.g. Muhammad Azhar")
    if search_name:
        res = lawyer_exp[lawyer_exp["Primary_Lawyer"].str.contains(search_name, case=False, na=False)]
        if len(res):
            st.success(f"Found {len(res):,} cases for lawyers matching '{search_name}'")
            by_date = res.groupby(["Hearing Date","Primary_Lawyer","Court Location"]).size().reset_index(name="Cases")
            st.dataframe(by_date.sort_values("Hearing Date", ascending=False), width='stretch')
        else:
            st.warning("No lawyer found with that name.")

# ══════════════════════════════════════════════
# TAB 8 — CASE SEARCH  (was tab 7)
# ══════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-title">🔎 Case Lookup & Search</div>', unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        case_query = st.text_input("Case Number", placeholder="e.g. W.P. 12345/2025")
    with sc2:
        party_query = st.text_input("Party / Title", placeholder="e.g. Collector of Customs")
    with sc3:
        justice_query = st.selectbox("Justice", ["All"] + sorted(fdf["Justice_Short"].dropna().unique().tolist()))

    s_city   = st.selectbox("City", ["All"] + sorted(fdf["Court Location"].unique().tolist()), key="s_city")
    s_legend = st.selectbox("Cause List", ["All"] + sorted(fdf["Legends"].unique().tolist()), key="s_leg")

    result_df = fdf.copy()
    if case_query:
        result_df = result_df[result_df["Case#"].str.contains(case_query, case=False, na=False)]
    if party_query:
        result_df = result_df[result_df["Title"].fillna("").str.contains(party_query, case=False, na=False)]
    if justice_query != "All":
        result_df = result_df[result_df["Justice_Short"] == justice_query]
    if s_city != "All":
        result_df = result_df[result_df["Court Location"] == s_city]
    if s_legend != "All":
        result_df = result_df[result_df["Legends"] == s_legend]

    st.markdown(f"**{len(result_df):,} records found**")

    if len(result_df):
        show_cols = ["Hearing Date","Hearing Day","Court Location","Bench Type","Justice_Short",
                     "Court","Legends","Cat_Group","Case#","Title","Lawyer","Remark_Group"]
        st.dataframe(
            result_df[show_cols].rename(columns={
                "Justice_Short":"Justice","Cat_Group":"Category","Remark_Group":"Status",
                "Court Location":"City","Hearing Date":"Date","Hearing Day":"Day"
            }).sort_values("Date", ascending=False).reset_index(drop=True),
            width='stretch', height=500
        )

        # Repeated hearings
        repeat = result_df.groupby(["Case#","Title"]).size().reset_index(name="Hearing Count")
        repeat = repeat[repeat["Hearing Count"] > 1].sort_values("Hearing Count", ascending=False)
        if len(repeat):
            st.markdown('<div class="section-title">⚠️ Repeatedly Heard Cases (Possible Delays)</div>', unsafe_allow_html=True)
            st.dataframe(repeat.head(20), width='stretch')
    else:
        st.info("No matching cases found. Try adjusting your search criteria.")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style='text-align:center; padding: 1rem; color: #6A7A9B; font-size:0.75rem; font-family:"IBM Plex Mono",monospace;'>
  ⚖️ <b style='color:#1B2B4B;'>Lahore High Court Analytics Dashboard</b> &nbsp;|&nbsp;
  Gallup Pakistan Digital Analytics &nbsp;|&nbsp;
  Data: data.lhc.gov.pk &nbsp;|&nbsp;
  Period: Feb–Mar 2026 &nbsp;|&nbsp;
  {len(df):,} total records
</div>
""", unsafe_allow_html=True)
