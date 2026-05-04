import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="TRS Operations Dashboard", page_icon="🛢", layout="wide")

# ── Custom CSS ──────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252a3d);
        border: 1px solid #2d3353;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: center;
        margin: 4px;
    }
    .metric-value { font-size: 28px; font-weight: 800; color: #00d4ff; }
    .metric-label { font-size: 12px; color: #8892b0; margin-top: 4px; }
    .metric-sub { font-size: 11px; color: #64ffda; margin-top: 2px; }
    .section-header {
        background: linear-gradient(90deg, #1e2130, transparent);
        border-left: 4px solid #00d4ff;
        padding: 8px 16px;
        margin: 20px 0 12px 0;
        font-size: 16px; font-weight: 700; color: #ccd6f6;
    }
    .stDataFrame { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    raw = {
        "Date": ["4/1/26","4/1/26","4/1/26","4/2/26","4/2/26","4/3/26","4/4/26","4/4/26","4/5/26","4/5/26",
                  "4/5/26","4/6/26","4/6/26","4/6/26","4/7/26","4/7/26","4/8/26","4/8/26","4/9/26","4/9/26",
                  "4/9/26","4/10/26","4/11/26","4/11/26","4/12/26","4/12/26","4/12/26","4/13/26","4/13/26","4/14/26",
                  "4/14/26","4/14/26","4/15/26","4/16/26","4/16/26","4/16/26","4/17/26","4/18/26","4/18/26","4/19/26",
                  "4/20/26","4/20/26","4/20/26","4/21/26","4/21/26","4/21/26","4/22/26","4/23/26","4/23/26","4/23/26",
                  "4/24/26","4/24/26","4/24/26","4/25/26","4/26/26","4/26/26","4/27/26","4/27/26","4/28/26","4/28/26",
                  "4/29/26","4/29/26","4/29/26"],
        "Customer": ["A","A","C","A","D","B","B","D","E","D","A","C","A","E","A","B","E","D","B","A","E","C","C","C","D","B","D","B","A","E","D","E","C","B","A","B","C","E","D","C","E","B","D","D","C","B","C","C","E","B","A","D","C","C","E","B","E","E","D","A","E","B","B"],
        "Rig_ID": ["RIG-04","RIG-04","RIG-02","RIG-06","RIG-06","RIG-02","RIG-04","RIG-01","RIG-02","RIG-05","RIG-04","RIG-06","RIG-05","RIG-05","RIG-05","RIG-06","RIG-05","RIG-03","RIG-04","RIG-04","RIG-04","RIG-02","RIG-03","RIG-01","RIG-01","RIG-02","RIG-02","RIG-05","RIG-02","RIG-01","RIG-05","RIG-06","RIG-03","RIG-06","RIG-04","RIG-04","RIG-01","RIG-01","RIG-02","RIG-06","RIG-05","RIG-02","RIG-03","RIG-01","RIG-04","RIG-05","RIG-04","RIG-06","RIG-04","RIG-04","RIG-06","RIG-06","RIG-06","RIG-03","RIG-01","RIG-04","RIG-05","RIG-06","RIG-06","RIG-02","RIG-03","RIG-02","RIG-01"],
        "Service_Type": ["Casing","Casing","Combo","Casing","Casing","CDS","CDS","Tubing","Tubing","Combo","Casing","Combo","CDS","Combo","Casing","Tubing","PULD","Tubing","CDS","Casing","Casing","Combo","PULD","CDS","Casing","Casing","Casing","CDS","Combo","Combo","Tubing","Casing","Combo","PULD","CDS","CDS","CDS","Combo","PULD","Casing","Casing","PULD","Combo","CDS","Combo","Tubing","Tubing","Tubing","PULD","Tubing","Combo","Combo","Tubing","Tubing","Casing","Casing","Tubing","Combo","Casing","PULD","Combo","PULD","CDS"],
        "Tool_Type": ["PULD Tool","CDS System","PULD Tool","Manual Tong","Manual Tong","Power Tong","Power Tong","PULD Tool","Manual Tong","PULD Tool","Power Tong","PULD Tool","Manual Tong","Running Tool","PULD Tool","Manual Tong","Running Tool","Power Tong","Manual Tong","Manual Tong","CDS System","Power Tong","CDS System","Manual Tong","PULD Tool","Running Tool","Running Tool","Manual Tong","CDS System","Running Tool","PULD Tool","Power Tong","Manual Tong","CDS System","Running Tool","Manual Tong","PULD Tool","Manual Tong","PULD Tool","Running Tool","PULD Tool","Manual Tong","PULD Tool","Power Tong","Power Tong","Power Tong","Manual Tong","Manual Tong","Power Tong","Power Tong","Manual Tong","CDS System","Manual Tong","Power Tong","Manual Tong","Running Tool","Running Tool","Manual Tong","Running Tool","Manual Tong","Running Tool","Running Tool","PULD Tool"],
        "Size": ["5 1/2","5 1/2","4 1/2","4 1/2","4 1/2","5 1/2","13 3/8","4 1/2","9 5/8","13 3/8","5 1/2","13 3/8","5 1/2","5 1/2","7","13 3/8","9 5/8","4 1/2","5 1/2","7","5 1/2","4 1/2","9 5/8","13 3/8","4 1/2","4 1/2","4 1/2","7","13 3/8","4 1/2","7","9 5/8","13 3/8","4 1/2","9 5/8","5 1/2","5 1/2","13 3/8","7","13 3/8","13 3/8","5 1/2","9 5/8","5 1/2","9 5/8","4 1/2","13 3/8","9 5/8","7","9 5/8","9 5/8","9 5/8","5 1/2","7","4 1/2","5 1/2","13 3/8","9 5/8","4 1/2","4 1/2","9 5/8","13 3/8","7"],
        "Revenue": [5679,9064,12106,7308,9624,13398,10620,5749,13616,8141,10529,13329,8445,4834,5873,4982,4452,11494,9471,8083,5283,10826,13829,10942,3602,11103,8031,14148,6182,11014,10258,12952,3116,6699,14686,6202,5675,6974,8237,11242,6711,10386,8301,11074,7973,12341,14855,6110,5814,7891,3071,5633,14769,7549,11988,5863,14565,14298,7166,8202,8578,11018,6356],
        "Job_Hrs": [18.7,4.5,7.2,10.9,20.6,11.6,14.7,4.6,16.9,15.7,19.8,4.2,23.1,19.3,8.8,14.6,8.5,5.2,18.5,13.3,13.0,14.8,7.3,13.7,13.5,8.7,15.7,22.7,22.7,15.1,18.4,4.9,5.5,22.0,19.0,19.7,17.2,4.6,23.7,22.8,12.2,10.0,17.5,8.5,16.6,8.4,15.9,8.9,10.7,14.9,11.0,12.7,14.7,8.2,5.0,13.5,18.4,8.0,12.6,11.2,20.5,10.7,15.9],
        "Joints": [170,46,90,135,232,131,70,56,108,65,208,7,224,170,78,48,53,69,187,88,150,198,46,58,159,110,146,191,91,194,174,33,9,260,115,219,199,17,226,100,57,102,89,90,101,70,52,36,96,95,48,79,130,79,55,151,75,32,155,120,135,49,124],
        "NPT_Hrs": [3.6,0.0,0.0,0.0,3.4,0.0,0.0,0.0,0.0,0.0,0.0,2.7,1.1,3.1,0.3,3.9,0.0,0.0,2.3,2.7,0.0,0.0,0.0,0.0,2.1,0.0,3.7,0.0,3.5,0.4,0.0,0.0,3.6,3.4,0.9,0.0,0.0,1.0,0.0,0.8,0.0,0.0,3.2,0.0,0.0,2.8,3.6,3.1,0.3,0.0,3.4,0.0,2.4,0.0,0.9,0.0,0.7,3.3,0.0,1.8,1.3,0.0,2.2],
        "NPT_Category": ["Equipment","","","","Process","","","","","","","Process","Process","Process","Client/3rd","Process","","","Personnel","Equipment","","","","","Equipment","","Personnel","","Weather","Personnel","","","Process","Weather","Personnel","","","Process","","Client/3rd","","","Personnel","","","Client/3rd","Process","Process","Personnel","","Client/3rd","","Equipment","","Equipment","","Weather","Personnel","","Personnel","Personnel","","Process"],
        "Status": ["FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","OPEN","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","OPEN","FINISHED","FINISHED","FINISHED","OPEN","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","OPEN","FINISHED","FINISHED","OPEN","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","OPEN","FINISHED","FINISHED","FINISHED","FINISHED","FINISHED","OPEN","FINISHED","FINISHED","FINISHED"]
    }
    df = pd.DataFrame(raw)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%y")
    df["Jts_Hr"] = df["Joints"] / df["Job_Hrs"].replace(0, float("nan"))
    return df

df = load_data()

# ── Sidebar Filters ──────────────────────────────────────────
st.sidebar.markdown("## 🔍 Filters")
customers = ["All"] + sorted(df["Customer"].unique().tolist())
rigs = ["All"] + sorted(df["Rig_ID"].unique().tolist())
services = ["All"] + sorted(df["Service_Type"].unique().tolist())

sel_customer = st.sidebar.selectbox("Customer", customers)
sel_rig = st.sidebar.selectbox("Rig", rigs)
sel_service = st.sidebar.selectbox("Service Type", services)

fdf = df.copy()
if sel_customer != "All": fdf = fdf[fdf["Customer"] == sel_customer]
if sel_rig != "All": fdf = fdf[fdf["Rig_ID"] == sel_rig]
if sel_service != "All": fdf = fdf[fdf["Service_Type"] == sel_service]

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#0f1117,#1a1f30);border-bottom:2px solid #00d4ff;padding:20px 30px;margin-bottom:20px;border-radius:12px;">
  <h1 style="color:#00d4ff;margin:0;font-size:28px;">🛢 TRS Operations Dashboard</h1>
  <p style="color:#8892b0;margin:4px 0 0 0;font-size:13px;">Tubular Running Services · Eastern Province, KSA · April 2026</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ────────────────────────────────────────────────
total_rev = fdf["Revenue"].sum()
total_jobs = len(fdf)
npt_pct = (fdf["NPT_Hrs"].sum() / fdf["Job_Hrs"].sum() * 100) if fdf["Job_Hrs"].sum() > 0 else 0
avg_rev = fdf["Revenue"].mean()
completion = (fdf["Status"] == "FINISHED").sum() / len(fdf) * 100 if len(fdf) > 0 else 0
total_joints = fdf["Joints"].sum()

c1, c2, c3, c4, c5, c6 = st.columns(6)
kpis = [
    (c1, "💰 Total Revenue", f"${total_rev:,.0f}", "USD · Month to Date"),
    (c2, "📋 Total Jobs", f"{total_jobs}", f"{(fdf['Status']=='FINISHED').sum()} finished"),
    (c3, "⏱ NPT %", f"{npt_pct:.1f}%", f"{fdf['NPT_Hrs'].sum():.1f} hrs total"),
    (c4, "📈 Avg Rev/Job", f"${avg_rev:,.0f}", "USD per job"),
    (c5, "✅ Completion", f"{completion:.1f}%", "Jobs closed"),
    (c6, "🔩 Total Joints", f"{total_joints:,}", "All jobs"),
]
for col, label, val, sub in kpis:
    col.markdown(f'''<div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{val}</div>
        <div class="metric-sub">{sub}</div>
    </div>''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Revenue trend + NPT by Category ──────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="section-header">📅 Daily Revenue & Cumulative Trend</div>', unsafe_allow_html=True)
    daily = fdf.groupby("Date").agg(Revenue=("Revenue","sum"), Jobs=("Revenue","count"), NPT=("NPT_Hrs","sum")).reset_index()
    daily["Cumulative"] = daily["Revenue"].cumsum()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=daily["Date"], y=daily["Revenue"], name="Daily Revenue", marker_color="#00d4ff", opacity=0.7), secondary_y=False)
    fig.add_trace(go.Scatter(x=daily["Date"], y=daily["Cumulative"], name="Cumulative", line=dict(color="#64ffda", width=2.5)), secondary_y=True)
    fig.update_layout(paper_bgcolor="#1e2130", plot_bgcolor="#1e2130", font_color="#ccd6f6",
                      legend=dict(bgcolor="rgba(0,0,0,0)"), height=300, margin=dict(l=10,r=10,t=10,b=10))
    fig.update_xaxes(gridcolor="#2d3353"); fig.update_yaxes(gridcolor="#2d3353")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-header">⚠️ NPT by Root Cause</div>', unsafe_allow_html=True)
    npt_df = fdf[fdf["NPT_Category"] != ""].groupby("NPT_Category")["NPT_Hrs"].sum().reset_index()
    fig2 = px.pie(npt_df, names="NPT_Category", values="NPT_Hrs",
                  color_discrete_sequence=["#00d4ff","#64ffda","#ff6b6b","#ffd93d","#6c5ce7"],
                  hole=0.45)
    fig2.update_layout(paper_bgcolor="#1e2130", font_color="#ccd6f6",
                       legend=dict(bgcolor="rgba(0,0,0,0)"), height=300, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Revenue by Customer + Service Type ────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-header">👤 Revenue by Customer</div>', unsafe_allow_html=True)
    cust = fdf.groupby("Customer").agg(Revenue=("Revenue","sum"), Jobs=("Revenue","count"), NPT=("NPT_Hrs","sum")).reset_index()
    cust["NPT_Pct"] = (cust["NPT"] / fdf.groupby("Customer")["Job_Hrs"].sum().values * 100).round(1)
    fig3 = px.bar(cust.sort_values("Revenue", ascending=True), x="Revenue", y="Customer",
                  orientation="h", color="Revenue", color_continuous_scale=["#1e2130","#00d4ff"],
                  text="Revenue")
    fig3.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig3.update_layout(paper_bgcolor="#1e2130", plot_bgcolor="#1e2130", font_color="#ccd6f6",
                       coloraxis_showscale=False, height=280, margin=dict(l=10,r=80,t=10,b=10))
    fig3.update_xaxes(gridcolor="#2d3353"); fig3.update_yaxes(gridcolor="#2d3353")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown('<div class="section-header">🔧 Revenue by Service Type</div>', unsafe_allow_html=True)
    svc = fdf.groupby("Service_Type").agg(Revenue=("Revenue","sum"), Jobs=("Revenue","count")).reset_index()
    fig4 = px.bar(svc.sort_values("Revenue", ascending=True), x="Revenue", y="Service_Type",
                  orientation="h", color="Jobs", color_continuous_scale=["#1a1f30","#64ffda"],
                  text="Revenue")
    fig4.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig4.update_layout(paper_bgcolor="#1e2130", plot_bgcolor="#1e2130", font_color="#ccd6f6",
                       coloraxis_colorbar=dict(title="Jobs", tickfont=dict(color="#ccd6f6")),
                       height=280, margin=dict(l=10,r=80,t=10,b=10))
    fig4.update_xaxes(gridcolor="#2d3353"); fig4.update_yaxes(gridcolor="#2d3353")
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Rig Performance + Joints/Hr scatter ──────────────
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="section-header">🏭 NPT % by Rig</div>', unsafe_allow_html=True)
    rig = fdf.groupby("Rig_ID").agg(Revenue=("Revenue","sum"), Jobs=("Revenue","count"),
                                     NPT_Hrs=("NPT_Hrs","sum"), Job_Hrs=("Job_Hrs","sum")).reset_index()
    rig["NPT_Pct"] = (rig["NPT_Hrs"] / rig["Job_Hrs"] * 100).round(1)
    fig5 = px.bar(rig, x="Rig_ID", y="NPT_Pct", color="NPT_Pct",
                  color_continuous_scale=["#64ffda","#ffd93d","#ff6b6b"],
                  text="NPT_Pct")
    fig5.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig5.update_layout(paper_bgcolor="#1e2130", plot_bgcolor="#1e2130", font_color="#ccd6f6",
                       coloraxis_showscale=False, height=260, margin=dict(l=10,r=10,t=10,b=10))
    fig5.update_xaxes(gridcolor="#2d3353"); fig5.update_yaxes(gridcolor="#2d3353")
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.markdown('<div class="section-header">⚡ Revenue/Hr vs Joints/Hr</div>', unsafe_allow_html=True)
    fdf2 = fdf.copy()
    fdf2["Rev_Hr"] = fdf2["Revenue"] / fdf2["Job_Hrs"]
    fig6 = px.scatter(fdf2, x="Jts_Hr", y="Rev_Hr", color="Service_Type", size="Revenue",
                      color_discrete_sequence=["#00d4ff","#64ffda","#ff6b6b","#ffd93d","#6c5ce7"],
                      hover_data=["Customer","Rig_ID","Status"])
    fig6.update_layout(paper_bgcolor="#1e2130", plot_bgcolor="#1e2130", font_color="#ccd6f6",
                       legend=dict(bgcolor="rgba(0,0,0,0)"), height=260, margin=dict(l=10,r=10,t=10,b=10))
    fig6.update_xaxes(gridcolor="#2d3353", title="Joints/Hr"); fig6.update_yaxes(gridcolor="#2d3353", title="Revenue/Hr")
    st.plotly_chart(fig6, use_container_width=True)

# ── Data Table ───────────────────────────────────────────────
st.markdown('<div class="section-header">📋 Operations Log</div>', unsafe_allow_html=True)
display_df = fdf[["Date","Customer","Rig_ID","Service_Type","Tool_Type","Size","Revenue","Job_Hrs","Joints","NPT_Hrs","NPT_Category","Status"]].copy()
display_df["Date"] = display_df["Date"].dt.strftime("%d/%m/%y")
display_df["Revenue"] = display_df["Revenue"].apply(lambda x: f"${x:,}")
st.dataframe(display_df, use_container_width=True, height=350)

st.markdown("<br><div style='text-align:center;color:#4a5568;font-size:11px;'>CONFIDENTIAL · FOR MANAGEMENT USE ONLY · TRS Operations Dashboard · Eastern Province, KSA</div>", unsafe_allow_html=True)
