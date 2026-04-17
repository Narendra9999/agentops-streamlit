import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mastercard AgentOps",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .stApp { background-color: #0e0e10; color: #f0f2f8; }

  /* hide default streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 1.5rem 2rem 2rem; max-width: 100%; }

  /* ── persona pills ── */
  div[data-testid="stHorizontalBlock"] > div { gap: 8px; }

  /* ── section label ── */
  .section-label {
    font-size: 11px; color: #555; text-transform: uppercase;
    letter-spacing: 0.09em; font-weight: 500; margin-bottom: 10px;
    margin-top: 20px;
  }

  /* ── metric card ── */
  .metric-card {
    background: #16161a; border-radius: 12px;
    border: 0.5px solid #252530; padding: 14px 16px;
  }
  .metric-card .label { font-size: 11px; color: #555; margin-bottom: 4px; }
  .metric-card .value { font-size: 22px; font-weight: 500; color: #f0f2f8; line-height: 1; }
  .metric-card .sub   { font-size: 11px; margin-top: 4px; }

  /* ── status badge ── */
  .badge {
    display: inline-block; font-size: 10px; padding: 2px 9px;
    border-radius: 20px; font-weight: 500;
  }
  .badge-healthy  { background:#0d2218; color:#22c55e; border:0.5px solid #1a4a30; }
  .badge-degraded { background:#2a1e0a; color:#f0a500; border:0.5px solid #4a3000; }
  .badge-down     { background:#2a1212; color:#ff6b6b; border:0.5px solid #4a1515; }
  .badge-prod     { background:#0d2218; color:#22c55e; border:0.5px solid #1a4a30; }
  .badge-staging  { background:#2a1e0a; color:#f0a500; border:0.5px solid #4a3000; }
  .badge-dev      { background:#0a1525; color:#6fa8f0; border:0.5px solid #1a3050; }
  .badge-success  { background:#0d2218; color:#22c55e; border:0.5px solid #1a4a30; }
  .badge-unstable { background:#2a1e0a; color:#f0a500; border:0.5px solid #4a3000; }
  .badge-failed   { background:#2a1212; color:#ff6b6b; border:0.5px solid #4a1515; }
  .badge-critical { background:#2a1212; color:#ff6b6b; }
  .badge-warning  { background:#2a1e0a; color:#f0a500; }
  .badge-info     { background:#1a1e2a; color:#6fa8f0; }
  .badge-live     { background:#0d2218; color:#22c55e; border:0.5px solid #1a4a30; font-size:11px; padding:3px 10px; border-radius:20px; }

  /* ── agent row card ── */
  .agent-card {
    background: #16161a; border-radius: 12px;
    border: 0.5px solid #252530; padding: 12px 16px; margin-bottom: 8px;
  }
  .agent-card-healthy  { border-color: #1a4a30; background: #0d2218; }
  .agent-card-degraded { border-color: #4a3000; background: #2a1e0a; }
  .agent-card-down     { border-color: #4a1515; background: #2a1212; }

  .agent-name  { font-size: 13px; font-weight: 500; color: #f0f2f8; }
  .agent-meta  { font-size: 11px; color: #888; margin-top: 2px; }
  .status-dot  { width:8px; height:8px; border-radius:50%; display:inline-block; margin-right:6px; vertical-align:middle; }
  .dot-healthy  { background:#22c55e; box-shadow:0 0 5px #22c55e55; }
  .dot-degraded { background:#f0a500; box-shadow:0 0 5px #f0a50055; }
  .dot-down     { background:#ff6b6b; box-shadow:0 0 5px #ff6b6b55; }

  /* ── topbar ── */
  .topbar {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 20px;
  }
  .logo-box {
    width:32px; height:32px; border-radius:10px; background:#c1ff72;
    display:inline-flex; align-items:center; justify-content:center;
    margin-right: 10px; vertical-align: middle;
  }
  .topbar-title { font-size:15px; font-weight:500; color:#f0f2f8; display:inline; }
  .topbar-sub   { font-size:11px; color:#888; }

  /* ── build stage pill ── */
  .stage-success { background:#0d2218; color:#22c55e; font-size:10px; padding:2px 7px; border-radius:6px; }
  .stage-failed  { background:#2a1212; color:#ff6b6b; font-size:10px; padding:2px 7px; border-radius:6px; }
  .stage-unstable{ background:#2a1e0a; color:#f0a500; font-size:10px; padding:2px 7px; border-radius:6px; }
  .stage-skipped { background:#1a1a1e; color:#555;    font-size:10px; padding:2px 7px; border-radius:6px; }

  /* ── alert card ── */
  .alert-critical { background:#2a1212; border:0.5px solid #4a1515; border-radius:12px; padding:12px 14px; margin-bottom:8px; }
  .alert-warning  { background:#2a1e0a; border:0.5px solid #4a3000; border-radius:12px; padding:12px 14px; margin-bottom:8px; }
  .alert-info     { background:#1a1e2a; border:0.5px solid #1a3050; border-radius:12px; padding:12px 14px; margin-bottom:8px; }

  /* ── cost bar ── */
  .cost-bar-track { background:#1e1e2a; border-radius:4px; height:5px; overflow:hidden; margin:4px 0; }
  .cost-bar-fill  { height:100%; border-radius:4px; }

  /* ── divider ── */
  hr { border-color: #252530; margin: 16px 0; }

  /* ── streamlit button overrides ── */
  .stButton > button {
    background: #16161a !important; color: #888 !important;
    border: 0.5px solid #252530 !important; border-radius: 10px !important;
    font-size: 12px !important; padding: 6px 0 !important;
    width: 100% !important; transition: all .15s;
  }
  .stButton > button:hover { border-color: #3a3f5a !important; color: #f0f2f8 !important; }

  /* ── selectbox / radio ── */
  .stSelectbox > div > div { background:#16161a !important; border-color:#252530 !important; color:#f0f2f8 !important; }
  .stRadio > div { gap: 6px; }
  .stRadio label { color: #888 !important; font-size: 12px !important; }

  /* streamlit tabs */
  .stTabs [data-baseweb="tab-list"] { background:#16161a; border-radius:12px; border:0.5px solid #252530; gap:4px; padding:6px; }
  .stTabs [data-baseweb="tab"] { background:transparent !important; color:#555 !important; border-radius:8px !important; font-size:12px !important; padding:6px 16px !important; }
  .stTabs [aria-selected="true"] { background:#252535 !important; color:#f0f2f8 !important; }
  .stTabs [data-baseweb="tab-border"] { display:none; }
  .stTabs [data-baseweb="tab-panel"] { padding-top: 16px; }

  /* expander */
  .streamlit-expanderHeader { background:#16161a !important; border-color:#252530 !important; color:#888 !important; border-radius:10px !important; }
  .streamlit-expanderContent { background:#16161a !important; border-color:#252530 !important; }

  /* progress bar */
  .stProgress > div > div { background:#1e1e2a !important; border-radius:4px; }
  .stProgress > div > div > div { border-radius:4px !important; }
</style>
""", unsafe_allow_html=True)


# ── Data ─────────────────────────────────────────────────────────────────────
AGENTS = [
    dict(id="fraud-detection-agent", name="Fraud Detection Agent", version="v2.4.1", env="prod",
         workspace="adb-prod-mastercard-us", status="healthy", owner="Daniel K.", team="Risk AI",
         deployed="2025-04-15 09:12 UTC", jenkins_job="fraud-agent-deploy", jenkins_build="#142",
         jenkins_url="https://jenkins.mc.internal/job/fraud-agent-deploy/142",
         workspace_url="https://adb-prod-mc.azuredatabricks.net",
         p50=184, p95=312, p99=580, success=99.1, calls=48200, errors=43,
         mlflow_url="https://adb-prod-mc.azuredatabricks.net/ml/experiments/fraud-agent",
         traces=[180,195,170,200,185,188,184,190,182,184],
         mcp_status="healthy", mcp_latency=42, mcp_version="1.3.0",
         mcp_url="https://adb-prod-mc.azuredatabricks.net/mcp/fraud",
         vs_status="healthy", vs_latency=28, vs_index="fraud-embeddings-v3", vs_docs=4200000,
         vs_url="https://adb-prod-mc.azuredatabricks.net/vs/fraud",
         gr_status="healthy", gr_rules=14, gr_blocked=12,
         gr_url="https://adb-prod-mc.azuredatabricks.net/guardrails/fraud",
         tools=[dict(name="transaction-lookup",status="healthy",calls=12400,latency=38),
                dict(name="risk-scorer",       status="healthy",calls=11800,latency=52),
                dict(name="alert-notifier",    status="healthy",calls=980,  latency=110)],
         env_total=18, env_set=18,
    ),
    dict(id="kyc-agent", name="KYC Verification Agent", version="v1.8.3", env="prod",
         workspace="adb-prod-mastercard-eu", status="degraded", owner="Priya S.", team="Compliance AI",
         deployed="2025-04-14 14:30 UTC", jenkins_job="kyc-agent-deploy", jenkins_build="#98",
         jenkins_url="https://jenkins.mc.internal/job/kyc-agent-deploy/98",
         workspace_url="https://adb-prod-mc-eu.azuredatabricks.net",
         p50=410, p95=1240, p99=3100, success=94.2, calls=18700, errors=1084,
         mlflow_url="https://adb-prod-mc-eu.azuredatabricks.net/ml/experiments/kyc-agent",
         traces=[380,420,510,890,1100,750,600,550,420,410],
         mcp_status="degraded", mcp_latency=210, mcp_version="1.2.1",
         mcp_url="https://adb-prod-mc-eu.azuredatabricks.net/mcp/kyc",
         vs_status="healthy", vs_latency=44, vs_index="kyc-docs-v2", vs_docs=920000,
         vs_url="https://adb-prod-mc-eu.azuredatabricks.net/vs/kyc",
         gr_status="healthy", gr_rules=22, gr_blocked=88,
         gr_url="https://adb-prod-mc-eu.azuredatabricks.net/guardrails/kyc",
         tools=[dict(name="id-verifier",    status="degraded",calls=8200,latency=820),
                dict(name="sanctions-check",status="healthy", calls=7400,latency=65),
                dict(name="doc-parser",     status="down",   calls=0,   latency=None)],
         env_total=24, env_set=22,
    ),
    dict(id="customer-assist-agent", name="Customer Assist Agent", version="v3.1.0", env="staging",
         workspace="adb-staging-mastercard-us", status="healthy", owner="Maya R.", team="CX AI",
         deployed="2025-04-16 11:45 UTC", jenkins_job="cx-agent-deploy", jenkins_build="#61",
         jenkins_url="https://jenkins.mc.internal/job/cx-agent-deploy/61",
         workspace_url="https://adb-staging-mc.azuredatabricks.net",
         p50=122, p95=280, p99=420, success=98.8, calls=7800, errors=94,
         mlflow_url="https://adb-staging-mc.azuredatabricks.net/ml/experiments/cx-agent",
         traces=[130,118,125,122,128,120,122,119,121,122],
         mcp_status="healthy", mcp_latency=38, mcp_version="1.3.0",
         mcp_url="https://adb-staging-mc.azuredatabricks.net/mcp/cx",
         vs_status="healthy", vs_latency=22, vs_index="cx-kb-v4", vs_docs=280000,
         vs_url="https://adb-staging-mc.azuredatabricks.net/vs/cx",
         gr_status="healthy", gr_rules=9, gr_blocked=31,
         gr_url="https://adb-staging-mc.azuredatabricks.net/guardrails/cx",
         tools=[dict(name="account-lookup",      status="healthy",calls=4100,latency=44),
                dict(name="transaction-history",  status="healthy",calls=2800,latency=72),
                dict(name="escalation-router",    status="healthy",calls=340, latency=88)],
         env_total=16, env_set=16,
    ),
    dict(id="credit-risk-agent", name="Credit Risk Agent", version="v1.2.0", env="dev",
         workspace="adb-dev-mastercard-us", status="down", owner="Tom W.", team="Risk AI",
         deployed="2025-04-17 08:00 UTC", jenkins_job="credit-agent-deploy", jenkins_build="#14",
         jenkins_url="https://jenkins.mc.internal/job/credit-agent-deploy/14",
         workspace_url="https://adb-dev-mc.azuredatabricks.net",
         p50=None, p95=None, p99=None, success=0, calls=220, errors=220,
         mlflow_url="https://adb-dev-mc.azuredatabricks.net/ml/experiments/credit-agent",
         traces=[200,320,580,900,None,None,None,None,None,None],
         mcp_status="down", mcp_latency=None, mcp_version="1.1.0",
         mcp_url="https://adb-dev-mc.azuredatabricks.net/mcp/credit",
         vs_status="down", vs_latency=None, vs_index="credit-data-v1", vs_docs=0,
         vs_url="https://adb-dev-mc.azuredatabricks.net/vs/credit",
         gr_status="healthy", gr_rules=8, gr_blocked=0,
         gr_url="https://adb-dev-mc.azuredatabricks.net/guardrails/credit",
         tools=[dict(name="credit-scorer",    status="down",   calls=0,latency=None),
                dict(name="bureau-fetch",     status="down",   calls=0,latency=None),
                dict(name="limit-calculator", status="healthy",calls=0,latency=None)],
         env_total=20, env_set=14,
    ),
]

BUILDS = [
    dict(agent="Fraud Detection Agent", job="fraud-agent-deploy", build="#142", status="success",
         env="prod", duration="4m 12s", triggered="auto · PR merge", time="Apr 15, 09:08 UTC",
         url="https://jenkins.mc.internal/job/fraud-agent-deploy/142",
         stages=["Checkout","Unit Tests","Build Image","Deploy","Health Check"],
         stage_status=["success","success","success","success","success"]),
    dict(agent="KYC Verification Agent", job="kyc-agent-deploy", build="#98", status="unstable",
         env="prod", duration="6m 38s", triggered="auto · PR merge", time="Apr 14, 14:24 UTC",
         url="https://jenkins.mc.internal/job/kyc-agent-deploy/98",
         stages=["Checkout","Unit Tests","Build Image","Deploy","Health Check"],
         stage_status=["success","success","success","success","unstable"]),
    dict(agent="Customer Assist Agent", job="cx-agent-deploy", build="#61", status="success",
         env="staging", duration="3m 55s", triggered="manual · Maya R.", time="Apr 16, 11:40 UTC",
         url="https://jenkins.mc.internal/job/cx-agent-deploy/61",
         stages=["Checkout","Unit Tests","Build Image","Deploy","Health Check"],
         stage_status=["success","success","success","success","success"]),
    dict(agent="Credit Risk Agent", job="credit-agent-deploy", build="#14", status="failed",
         env="dev", duration="2m 11s", triggered="auto · commit push", time="Apr 17, 07:55 UTC",
         url="https://jenkins.mc.internal/job/credit-agent-deploy/14",
         stages=["Checkout","Unit Tests","Build Image","Deploy","Health Check"],
         stage_status=["success","success","success","failed","skipped"]),
]

ALERTS = [
    dict(id=1, sev="critical", agent="Credit Risk Agent", component="MCP Server", env="dev",
         resolved=False, time="17m ago", msg="MCP server unresponsive — all requests failing.",
         rca="Check Databricks cluster logs. MCP endpoint may not have started after deploy #14."),
    dict(id=2, sev="critical", agent="Credit Risk Agent", component="Vector Search", env="dev",
         resolved=False, time="19m ago", msg="Vector search index unavailable — 0 docs indexed.",
         rca="VECTOR_SEARCH_ENDPOINT env var not set. Configure via Databricks secrets scope."),
    dict(id=3, sev="warning", agent="KYC Verification Agent", component="doc-parser", env="prod",
         resolved=False, time="1h 4m ago", msg="doc-parser tool returning 503 — 0 calls in last 30m.",
         rca="Likely upstream dependency outage. Check MCP server EU region logs."),
    dict(id=4, sev="warning", agent="KYC Verification Agent", component="MCP Server", env="prod",
         resolved=False, time="1h 10m ago", msg="MCP server latency degraded — avg 210ms vs 45ms.",
         rca="EU region CPU spike. Consider horizontal scaling of MCP server."),
    dict(id=5, sev="info", agent="KYC Verification Agent", component="Env Config", env="prod",
         resolved=False, time="1h 30m ago", msg="2 environment variables not set.",
         rca="Set missing vars in Databricks secrets scope: /secrets/agentops."),
    dict(id=6, sev="info", agent="Fraud Detection Agent", component="Guardrails", env="prod",
         resolved=True, time="3h ago", msg="12 requests blocked by guardrails — above 7-day avg.",
         rca="Review blocked prompt patterns. May indicate prompt injection attempts."),
]

AGENT_COSTS = [
    dict(name="Fraud Detection", dbu=142, usd=8.52, tokens="1.8M", pct=30, env="prod",  trend=[120,130,118,140,135,142]),
    dict(name="KYC Verification",dbu=198, usd=11.88,tokens="2.4M", pct=41, env="prod",  trend=[160,175,190,185,200,198]),
    dict(name="Customer Assist", dbu=68,  usd=4.08, tokens="0.9M", pct=14, env="staging",trend=[50,60,65,62,70,68]),
    dict(name="Credit Risk",     dbu=70,  usd=4.20, tokens="0.3M", pct=15, env="dev",   trend=[0,0,20,60,80,70]),
]
WEEKLY_DBU  = [310,380,295,420,365,440,478]
WEEK_DAYS   = ["Mon","Tue","Wed","Thu","Fri","Sat","Today"]


# ── Colour helpers ────────────────────────────────────────────────────────────
STATUS_COLOR = {"healthy":"#22c55e","degraded":"#f0a500","down":"#ff6b6b"}
SEV_COLOR    = {"critical":"#ff6b6b","warning":"#f0a500","info":"#6fa8f0"}

def sc(s): return STATUS_COLOR.get(s,"#888")
def badge(text, cls): return f'<span class="badge badge-{cls}">{text}</span>'
def dot(s): return f'<span class="status-dot dot-{s}"></span>'


# ── Plotly theme ──────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#888", family="Inter"),
    margin=dict(l=0, r=0, t=8, b=0),
    xaxis=dict(showgrid=False, color="#444", tickfont=dict(size=10, color="#444")),
    yaxis=dict(gridcolor="#1e1e2a", color="#444", tickfont=dict(size=10, color="#444")),
    showlegend=False,
)

def ring_chart(value, color, track, label):
    fig = go.Figure(go.Pie(
        values=[value, 100-value],
        hole=0.72,
        marker_colors=[color, track],
        textinfo="none",
        sort=False,
        direction="clockwise",
        rotation=90,
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        annotations=[dict(text=f"<b>{value}</b>", x=0.5, y=0.5,
                          font=dict(size=22, color="#f0f2f8", family="Inter"),
                          showarrow=False)],
        height=160, margin=dict(l=8, r=8, t=8, b=8),
    )
    return fig

def spark_chart(data, color="#6fa8f0", height=80):
    valid = [(i, v) for i, v in enumerate(data) if v is not None]
    if not valid:
        return go.Figure().update_layout(**PLOTLY_LAYOUT, height=height)
    xs, ys = zip(*valid)
    fig = go.Figure(go.Scatter(
        x=list(xs), y=list(ys), mode="lines",
        line=dict(color=color, width=2),
        fill="tozeroy", fillcolor=color.replace(")", ",0.08)").replace("rgb","rgba") if "rgb" in color else color+"18",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig

def bar_chart(labels, values, colors, height=160):
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color=colors, marker=dict(cornerradius=4)))
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    return fig


# ── Shared components ─────────────────────────────────────────────────────────
def render_topbar(persona, tab):
    persona_labels = {"pm":"Project Manager","dev":"Developer","admin":"Ops / Admin"}
    persona_colors = {"pm":"#a78bfa","dev":"#6fa8f0","admin":"#22c55e"}
    col1, col2 = st.columns([1, 0.2])
    with col1:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:4px;">
          <div style="width:32px;height:32px;border-radius:10px;background:#c1ff72;
                      display:inline-flex;align-items:center;justify-content:center;">
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
              <circle cx="9" cy="9" r="6" stroke="#0e0e10" stroke-width="2.2"/>
              <circle cx="9" cy="9" r="2.5" fill="#0e0e10"/>
            </svg>
          </div>
          <div>
            <div style="font-size:15px;font-weight:500;color:#f0f2f8;">{tab.title()}</div>
            <div style="font-size:11px;color:#888;">{persona_labels[persona]} · Mastercard AgentOps</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align:right;padding-top:4px;">
          <span class="badge-live">● Live</span>&nbsp;
          <span style="font-size:11px;padding:3px 8px;border-radius:20px;
                background:transparent;color:{persona_colors[persona]};
                border:0.5px solid {persona_colors[persona]}44;">{persona.upper()}</span>
        </div>
        """, unsafe_allow_html=True)

def sl(text):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)

def metric_card(label, value, sub="", sub_color="#888"):
    st.markdown(f"""
    <div class="metric-card">
      <div class="label">{label}</div>
      <div class="value">{value}</div>
      {'<div class="sub" style="color:'+sub_color+';">'+sub+'</div>' if sub else ''}
    </div>
    """, unsafe_allow_html=True)

def stat_cols(items):
    """items: list of (label, value, color)"""
    cols = st.columns(len(items))
    for col, (lbl, val, clr) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div style="background:#121214;border-radius:10px;padding:10px 12px;
                        border:0.5px solid #252530;text-align:center;">
              <div style="font-size:10px;color:#555;margin-bottom:3px;">{lbl}</div>
              <div style="font-size:16px;font-weight:500;color:{clr};">{val}</div>
            </div>
            """, unsafe_allow_html=True)

def render_alert_card(a, show_rca=False):
    cls = f"alert-{a['sev']}"
    rca_html = ""
    if show_rca:
        rca_html = f"""
        <details style="margin-top:8px;">
          <summary style="font-size:11px;color:#6fa8f0;cursor:pointer;">▼ show RCA hint</summary>
          <div style="margin-top:6px;padding:8px 10px;background:#0e0e10;border-radius:8px;
                      font-size:12px;color:#888;line-height:1.6;">{a['rca']}</div>
        </details>"""
    resolved_badge = badge("resolved","info") if a["resolved"] else ""
    st.markdown(f"""
    <div class="{cls}">
      <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;flex-wrap:wrap;">
        {badge(a['sev'], a['sev'])}
        <span style="font-size:11px;color:#888;">{a['agent']}</span>
        <span style="font-size:10px;color:#555;">· {a['component']}</span>
        {badge(a['env'], a['env'])}
        {resolved_badge}
      </div>
      <div style="font-size:12px;color:#ccc;line-height:1.5;">{a['msg']}</div>
      <div style="font-size:11px;color:#555;margin-top:3px;">{a['time']}</div>
      {rca_html}
    </div>
    """, unsafe_allow_html=True)

def render_build_card(b):
    stages_html = " › ".join(
        f'<span class="stage-{ss}">{s}</span>'
        for s, ss in zip(b["stages"], b["stage_status"])
    )
    color = {"success":STATUS_COLOR["healthy"],"unstable":STATUS_COLOR["degraded"],"failed":STATUS_COLOR["down"]}.get(b["status"],"#888")
    bg    = {"success":"#0d2218","unstable":"#2a1e0a","failed":"#2a1212"}.get(b["status"],"#16161a")
    bd    = {"success":"#1a4a30","unstable":"#4a3000","failed":"#4a1515"}.get(b["status"],"#252530")
    st.markdown(f"""
    <div style="background:{bg};border-radius:14px;border:0.5px solid {bd};padding:14px 16px;margin-bottom:10px;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;">
        <span style="width:8px;height:8px;border-radius:50%;background:{color};
                     margin-top:4px;flex-shrink:0;display:inline-block;"></span>
        <div style="flex:1;">
          <div style="font-size:13px;font-weight:500;color:#f0f2f8;">{b['agent']}</div>
          <div style="font-size:11px;color:#888;margin-top:1px;">
            {b['job']} {b['build']} · {badge(b['env'],b['env'])} · {b['time']}
          </div>
          <div style="font-size:11px;color:#555;margin-top:1px;">
            triggered by {b['triggered']} · {b['duration']}
          </div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:11px;color:{color};">{b['status']}</div>
          <a href="{b['url']}" target="_blank" style="font-size:11px;color:#6fa8f0;">Jenkins ↗</a>
        </div>
      </div>
      <div style="display:flex;gap:4px;flex-wrap:wrap;align-items:center;">{stages_html}</div>
    </div>
    """, unsafe_allow_html=True)


# ── OVERVIEW views ────────────────────────────────────────────────────────────
def render_overview(persona):
    render_topbar(persona, "Overview")
    sl("Fleet health score")
    rc1, rc2, rc3 = st.columns(3)
    rings = [
        (rc1, 85, "#c1ff72", "#1e2e1e", "Uptime",   "↑ 2% vs yesterday"),
        (rc2, 70, "#f0a500", "#2a1e0a", "Success",  "↓ 3% vs yesterday"),
        (rc3, 90, "#6fa8f0", "#1a1e2a", "Latency",  "↑ 5% vs yesterday"),
    ]
    for col, val, clr, trk, lbl, sub in rings:
        with col:
            st.plotly_chart(ring_chart(val, clr, trk, lbl), use_container_width=True, config={"displayModeBar":False})
            st.markdown(f'<div style="text-align:center;font-size:13px;font-weight:500;color:#f0f2f8;margin-top:-12px;">{lbl}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:center;font-size:11px;color:#555;margin-bottom:8px;">{sub}</div>', unsafe_allow_html=True)

    if persona == "pm":
        sl("Goal progress")
        goals = [
            ("Prod pipelines healthy", 1, 2, "#f0a500"),
            ("Avg success rate (prod)", 96.7, 99, "#22c55e"),
            ("Build success rate", 75, 100, "#f0a500"),
        ]
        for lbl, cur, tgt, clr in goals:
            pct = int((cur/tgt)*100)
            st.markdown(f"""
            <div style="background:#16161a;border-radius:12px;padding:12px 16px;
                        border:0.5px solid #252530;margin-bottom:8px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                <span style="font-size:12px;color:#ccc;">{lbl}</span>
                <span style="font-size:12px;font-weight:500;color:{clr};">{cur}/{tgt}</span>
              </div>
              <div style="background:#1e1e2a;border-radius:4px;height:5px;">
                <div style="width:{pct}%;height:100%;background:{clr};border-radius:4px;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        sl("Active incidents")
        for inc in [
            ("Credit Risk Agent","dev","Fully down — MCP + vector search offline. 6 missing env vars.","Assign to Tom W. — review deploy #14."),
            ("KYC Verification Agent","prod","doc-parser down, MCP degraded — affecting 5.8% of KYC flows.","Escalate to Priya S. — EU region review."),
        ]:
            st.markdown(f"""
            <div style="background:#16161a;border-radius:12px;border:0.5px solid #4a1515;
                        padding:12px 14px;margin-bottom:8px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">
                <span style="width:7px;height:7px;border-radius:50%;background:#ff6b6b;display:inline-block;"></span>
                <span style="font-size:13px;font-weight:500;color:#f0f2f8;">{inc[0]}</span>
                {badge(inc[1],inc[1])}
              </div>
              <div style="font-size:12px;color:#888;margin-bottom:4px;line-height:1.5;">{inc[2]}</div>
              <div style="font-size:11px;color:#f0a500;">→ {inc[3]}</div>
            </div>
            """, unsafe_allow_html=True)

    elif persona == "dev":
        sl("MLflow fleet metrics")
        c1, c2, c3, c4 = st.columns(4)
        with c1: metric_card("Fleet avg p50", "195ms", "across healthy agents", "#22c55e")
        with c2: metric_card("Fleet avg p95", "621ms", "KYC pulling avg up", "#f0a500")
        with c3: metric_card("Total calls", "74,920", "across all pipelines")
        with c4: metric_card("Error rate", "1.7%", "2 critical incidents", "#ff6b6b")
        sl("Per-agent latency snapshot")
        for a in AGENTS:
            c = sc(a["status"])
            p50 = f"{a['p50']}ms" if a["p50"] else "—"
            st.markdown(f"""
            <div style="background:#16161a;border-radius:12px;border:0.5px solid {c}44;
                        padding:10px 14px;margin-bottom:8px;display:flex;align-items:center;gap:10px;">
              {dot(a['status'])}
              <div style="flex:1;">
                <div style="font-size:12px;font-weight:500;color:#f0f2f8;">{a['name']}</div>
                <a href="{a['mlflow_url']}" target="_blank" style="font-size:10px;color:#6fa8f0;">MLflow ↗</a>
              </div>
              <div style="text-align:right;">
                <div style="font-size:12px;color:{c};">{p50}</div>
                <div style="font-size:10px;color:#555;">p50</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    elif persona == "admin":
        sl("Workspace registry")
        for ws in [
            ("adb-prod-mastercard-us","prod",2,"US East","healthy","https://adb-prod-mc.azuredatabricks.net"),
            ("adb-prod-mastercard-eu","prod",1,"EU West","degraded","https://adb-prod-mc-eu.azuredatabricks.net"),
            ("adb-staging-mastercard-us","staging",1,"US East","healthy","https://adb-staging-mc.azuredatabricks.net"),
            ("adb-dev-mastercard-us","dev",1,"US East","down","https://adb-dev-mc.azuredatabricks.net"),
        ]:
            c = sc(ws[4])
            st.markdown(f"""
            <div style="background:{c}11;border-radius:12px;border:0.5px solid {c}44;
                        padding:12px 14px;margin-bottom:8px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">
                {dot(ws[4])}
                <span style="font-size:13px;font-weight:500;color:#f0f2f8;">{ws[0]}</span>
                {badge(ws[1],ws[1])}
              </div>
              <div style="display:flex;justify-content:space-between;">
                <span style="font-size:11px;color:#888;">{ws[3]} · {ws[2]} agent{'s' if ws[2]>1 else ''}</span>
                <a href="{ws[5]}" target="_blank" style="font-size:11px;color:#6fa8f0;">Open workspace ↗</a>
              </div>
            </div>
            """, unsafe_allow_html=True)
        sl("DBU consumption")
        st.markdown("""
        <div style="background:#16161a;border-radius:12px;border:0.5px solid #252530;padding:14px 16px;">
          <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px;">
            <span style="font-size:12px;color:#888;">Month-to-date</span>
            <span style="font-size:18px;font-weight:500;color:#c1ff72;">478 <span style="font-size:12px;color:#555;">/ 1,000 DBU</span></span>
          </div>
          <div style="background:#1e1e2a;border-radius:5px;height:7px;">
            <div style="width:47.8%;height:100%;background:#c1ff72;border-radius:5px;"></div>
          </div>
          <div style="font-size:11px;color:#555;margin-top:5px;">47.8% of monthly budget · 522 DBU remaining</div>
        </div>
        """, unsafe_allow_html=True)


# ── AGENTS views ──────────────────────────────────────────────────────────────
def render_agents(persona):
    render_topbar(persona, "Agents")
    if persona == "pm":
        sl("Agent scorecard")
        df = pd.DataFrame([{
            "Agent": a["name"], "Version": a["version"],
            "Success": f"{a['success']}%", "Calls": f"{a['calls']:,}",
            "Status": a["status"], "Env": a["env"],
        } for a in AGENTS])
        st.dataframe(df, use_container_width=True, hide_index=True)
        sl("Deployment summary")
        for a in AGENTS:
            c = sc(a["status"])
            st.markdown(f"""
            <div style="background:{c}11;border-radius:12px;border:0.5px solid {c}44;
                        padding:12px 14px;margin-bottom:8px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                {dot(a['status'])}<span style="font-size:13px;font-weight:500;color:#f0f2f8;">{a['name']}</span>
                {badge(a['env'],a['env'])}
              </div>
              <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;font-size:11px;">
                <div style="color:#888;"><span style="color:#555;display:block;">Version</span>{a['version']}</div>
                <div style="color:#888;"><span style="color:#555;display:block;">Build</span>{a['jenkins_build']}</div>
                <div style="color:#888;"><span style="color:#555;display:block;">Deployed</span>{a['deployed'].split(' ')[0]}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    elif persona == "dev":
        names = [a["name"].split()[0] for a in AGENTS]
        sel_name = st.selectbox("Select agent", names, key="dev_agent_select")
        a = AGENTS[names.index(sel_name)]
        c = sc(a["status"])
        st.markdown(f"""
        <div style="background:{c}11;border-radius:14px;border:0.5px solid {c}44;padding:14px;margin-bottom:12px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
            {dot(a['status'])}
            <div style="flex:1;">
              <div style="font-size:14px;font-weight:500;color:#f0f2f8;">{a['name']}</div>
              <div style="font-size:11px;color:#888;">{a['version']} · {a['workspace']}</div>
            </div>
            {badge(a['env'],a['env'])}
          </div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <a href="{a['workspace_url']}" target="_blank" style="font-size:11px;color:#6fa8f0;">Workspace ↗</a>
            <a href="{a['mlflow_url']}" target="_blank" style="font-size:11px;color:#6fa8f0;">MLflow ↗</a>
            <a href="{a['jenkins_url']}" target="_blank" style="font-size:11px;color:#6fa8f0;">Jenkins {a['jenkins_build']} ↗</a>
            <a href="{a['mcp_url']}" target="_blank" style="font-size:11px;color:#6fa8f0;">MCP ↗</a>
            <a href="{a['vs_url']}" target="_blank" style="font-size:11px;color:#6fa8f0;">VectorSearch ↗</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

        sub1, sub2, sub3, sub4 = st.tabs(["Health","Metrics","Tools","Config"])
        with sub1:
            for comp_name, status, detail, url in [
                ("MCP Server", a["mcp_status"], f"v{a['mcp_version']} · {a['mcp_latency']}ms" if a["mcp_latency"] else f"v{a['mcp_version']} · no response", a["mcp_url"]),
                ("Vector Search", a["vs_status"], f"{a['vs_index']} · {a['vs_docs']/1e6:.1f}M docs" if a["vs_docs"] else f"{a['vs_index']} · 0 docs", a["vs_url"]),
                ("Guardrails", a["gr_status"], f"{a['gr_rules']} rules · {a['gr_blocked']} blocked", a["gr_url"]),
                ("Env vars", "degraded" if a["env_set"]<a["env_total"] else "healthy", f"{a['env_set']}/{a['env_total']} set", None),
            ]:
                cc = sc(status)
                link = f'<a href="{url}" target="_blank" style="font-size:11px;color:#6fa8f0;">view ↗</a>' if url else ""
                st.markdown(f"""
                <div style="background:{cc}11;border-radius:12px;border:0.5px solid {cc}44;
                            padding:11px 14px;margin-bottom:7px;display:flex;align-items:center;gap:10px;">
                  {dot(status)}
                  <div style="flex:1;">
                    <div style="font-size:12px;font-weight:500;color:#f0f2f8;">{comp_name}</div>
                    <div style="font-size:11px;color:#888;">{detail}</div>
                  </div>{link}
                </div>
                """, unsafe_allow_html=True)
        with sub2:
            p50c = "#22c55e" if a["p50"] and a["p50"]<500 else "#f0a500" if a["p50"] else "#ff6b6b"
            p95c = "#22c55e" if a["p95"] and a["p95"]<1000 else "#f0a500" if a["p95"] else "#ff6b6b"
            sc_c = "#22c55e" if a["success"]>97 else "#f0a500" if a["success"]>90 else "#ff6b6b"
            stat_cols([
                ("p50", f"{a['p50']}ms" if a["p50"] else "—", p50c),
                ("p95", f"{a['p95']}ms" if a["p95"] else "—", p95c),
                ("p99", f"{a['p99']}ms" if a["p99"] else "—", "#888"),
                ("Success", f"{a['success']}%", sc_c),
                ("Calls", f"{a['calls']:,}", "#f0f2f8"),
                ("Errors", str(a["errors"]), "#ff6b6b" if a["errors"]>500 else "#f0a500" if a["errors"]>100 else "#22c55e"),
            ])
            st.plotly_chart(spark_chart(a["traces"], sc(a["status"]), 80), use_container_width=True, config={"displayModeBar":False})
        with sub3:
            for t in a["tools"]:
                tc = sc(t["status"])
                lat = f"{t['latency']}ms avg" if t["latency"] else "no response"
                st.markdown(f"""
                <div style="background:{tc}11;border-radius:12px;border:0.5px solid {tc}44;
                            padding:11px 14px;margin-bottom:7px;display:flex;align-items:center;gap:10px;">
                  {dot(t['status'])}
                  <div style="flex:1;">
                    <div style="font-size:12px;font-family:monospace;color:#f0f2f8;">{t['name']}</div>
                    <div style="font-size:11px;color:#888;">{t['calls']:,} calls · {lat}</div>
                  </div>
                  <span style="font-size:11px;color:{tc};">{t['status']}</span>
                </div>
                """, unsafe_allow_html=True)
        with sub4:
            c1, c2 = st.columns(2)
            for col, items in [(c1,[("Version",a["version"]),("Env",a["env"])]),
                               (c2,[("Jenkins",a["jenkins_build"]),("Owner",a["owner"])])]:
                for k, v in items:
                    with col:
                        st.markdown(f"""
                        <div style="background:#16161a;border-radius:8px;padding:9px 11px;
                                    border:0.5px solid #252530;margin-bottom:6px;">
                          <div style="font-size:10px;color:#555;">{k}</div>
                          <div style="font-size:12px;color:#f0f2f8;">{v}</div>
                        </div>
                        """, unsafe_allow_html=True)

    elif persona == "admin":
        for a in AGENTS:
            c = sc(a["status"])
            enabled = st.toggle(a["name"], value=(a["status"]!="down"), key=f"tog_{a['id']}")
            st.markdown(f"""
            <div style="background:{c}11;border-radius:14px;border:0.5px solid {c}44;
                        padding:14px 16px;margin-bottom:10px;">
              <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:10px;">
                <div style="background:#1a1a20;border-radius:7px;padding:7px 9px;">
                  <div style="font-size:10px;color:#555;">Version</div>
                  <div style="font-size:11px;color:#f0f2f8;">{a['version']}</div>
                </div>
                <div style="background:#1a1a20;border-radius:7px;padding:7px 9px;">
                  <div style="font-size:10px;color:#555;">Owner</div>
                  <div style="font-size:11px;color:#f0f2f8;">{a['owner']}</div>
                </div>
                <div style="background:#1a1a20;border-radius:7px;padding:7px 9px;">
                  <div style="font-size:10px;color:#555;">Env vars</div>
                  <div style="font-size:11px;color:{'#ff6b6b' if a['env_set']<a['env_total'] else '#f0f2f8'};">{a['env_set']}/{a['env_total']}</div>
                </div>
              </div>
              <div style="display:flex;gap:10px;flex-wrap:wrap;">
                <a href="{a['workspace_url']}" target="_blank" style="font-size:11px;color:#6fa8f0;">Workspace ↗</a>
                <a href="{a['mlflow_url']}" target="_blank" style="font-size:11px;color:#6fa8f0;">MLflow ↗</a>
                <a href="{a['jenkins_url']}" target="_blank" style="font-size:11px;color:#6fa8f0;">Jenkins ↗</a>
              </div>
            </div>
            """, unsafe_allow_html=True)


# ── PIPELINE views ────────────────────────────────────────────────────────────
def render_pipeline(persona):
    render_topbar(persona, "Pipeline")
    passed   = sum(1 for b in BUILDS if b["status"]=="success")
    unstable = sum(1 for b in BUILDS if b["status"]=="unstable")
    failed   = sum(1 for b in BUILDS if b["status"]=="failed")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div style="background:#0d2218;border-radius:12px;padding:14px;border:0.5px solid #1a4a30;text-align:center;"><div style="font-size:26px;font-weight:500;color:#22c55e;">{passed}</div><div style="font-size:11px;color:#22c55e;opacity:.7;">Passed</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div style="background:#2a1e0a;border-radius:12px;padding:14px;border:0.5px solid #4a3000;text-align:center;"><div style="font-size:26px;font-weight:500;color:#f0a500;">{unstable}</div><div style="font-size:11px;color:#f0a500;opacity:.7;">Unstable</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div style="background:#2a1212;border-radius:12px;padding:14px;border:0.5px solid #4a1515;text-align:center;"><div style="font-size:26px;font-weight:500;color:#ff6b6b;">{failed}</div><div style="font-size:11px;color:#ff6b6b;opacity:.7;">Failed</div></div>', unsafe_allow_html=True)

    sl("Recent builds")
    for b in BUILDS:
        render_build_card(b)
        if persona == "dev" and b["job"] in ("kyc-agent-deploy","credit-agent-deploy"):
            logs = {
                "kyc-agent-deploy":["[Health Check] MCP server ping: TIMEOUT","[Health Check] Build marked UNSTABLE"],
                "credit-agent-deploy":["[Deploy] ERROR: DATABRICKS_TOKEN not set","[Deploy] FATAL: Build FAILED"],
            }
            with st.expander("▼ show logs"):
                for line in logs[b["job"]]:
                    color = "#ff6b6b" if "ERROR" in line or "FATAL" in line else "#f0a500" if "TIMEOUT" in line or "UNSTABLE" in line else "#888"
                    st.markdown(f'<div style="font-size:11px;font-family:monospace;color:{color};padding:2px 0;">{line}</div>', unsafe_allow_html=True)

    if persona == "admin":
        sl("Pipeline rules")
        for rule, default in [("Auto-approve prod deploys",False),("Enforce health check gate",True),("Auto-rollback on failure",True),("Slack notifications",True)]:
            st.toggle(rule, value=default, key=f"rule_{rule}")


# ── COSTS views ───────────────────────────────────────────────────────────────
def render_costs(persona):
    render_topbar(persona, "Costs")
    total_usd = sum(a["usd"] for a in AGENT_COSTS)
    total_dbu = sum(a["dbu"] for a in AGENT_COSTS)

    if persona == "pm":
        sl("Cost summary")
        c1, c2, c3, c4 = st.columns(4)
        with c1: metric_card("Total spend today", f"${total_usd:.2f}", "across all agents")
        with c2: metric_card("DBU consumed", str(total_dbu), "of 1,000 monthly budget")
        with c3: metric_card("Projected monthly", "~$4,680", "↑ 8% vs last month", "#f0a500")
        with c4: metric_card("Budget utilisation", "47.8%", "522 DBU remaining", "#22c55e")
        sl("Spend by agent")
        for a in AGENT_COSTS:
            st.markdown(f"""
            <div style="background:#16161a;border-radius:12px;padding:12px 16px;
                        border:0.5px solid #252530;margin-bottom:8px;">
              <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;">
                <div><span style="font-size:13px;font-weight:500;color:#f0f2f8;">{a['name']}</span>&nbsp;{badge(a['env'],a['env'])}</div>
                <span style="font-size:13px;font-weight:500;color:#f0f2f8;">${a['usd']:.2f}</span>
              </div>
              <div style="background:#1e1e2a;border-radius:4px;height:5px;margin-bottom:4px;">
                <div style="width:{a['pct']}%;height:100%;background:#a78bfa;border-radius:4px;"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:11px;color:#555;">
                <span>{a['dbu']} DBU · {a['tokens']} tokens</span><span>{a['pct']}% of total</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
        sl("Weekly DBU trend")
        colors = ["#2a1e40"]*6 + ["#a78bfa"]
        st.plotly_chart(bar_chart(WEEK_DAYS, WEEKLY_DBU, colors, 160), use_container_width=True, config={"displayModeBar":False})

    elif persona == "dev":
        sl("Token usage by agent")
        for a in AGENT_COSTS:
            st.markdown(f"""
            <div style="background:#16161a;border-radius:12px;padding:12px 14px;
                        border:0.5px solid #252530;margin-bottom:8px;">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                <div style="flex:1;"><span style="font-size:12px;font-weight:500;color:#f0f2f8;">{a['name']}</span>&nbsp;{badge(a['env'],a['env'])}</div>
                <span style="font-size:12px;color:#6fa8f0;">{a['tokens']} tokens</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(spark_chart(a["trend"], "#6fa8f0", 60), use_container_width=True, config={"displayModeBar":False})
        sl("Cost efficiency")
        rows = [("Fraud Detection","99.1% success","$0.00018/call","#22c55e"),
                ("KYC Verification","94.2% success","$0.00064/call","#f0a500"),
                ("Customer Assist","98.8% success","$0.00052/call","#22c55e"),
                ("Credit Risk","0% success","—","#ff6b6b")]
        for n, s, cc, col in rows:
            st.markdown(f'<div style="display:flex;gap:8px;padding:7px 0;border-bottom:0.5px solid #252530;font-size:11px;"><span style="flex:1;color:#f0f2f8;">{n}</span><span style="color:{col};">{s}</span><span style="color:#555;min-width:88px;text-align:right;">{cc}</span></div>', unsafe_allow_html=True)

    elif persona == "admin":
        sl("DBU budget control")
        budget = st.slider("Monthly DBU limit", 200, 3000, 1000, 50, key="dbu_budget")
        pct = (478/budget)*100
        bar_color = "#ff6b6b" if pct>85 else "#f0a500" if pct>60 else "#c1ff72"
        st.markdown(f"""
        <div style="background:#16161a;border-radius:14px;padding:16px;border:0.5px solid #252530;">
          <div style="background:#1e1e2a;border-radius:5px;height:7px;margin-bottom:6px;">
            <div style="width:{min(pct,100):.1f}%;height:100%;background:{bar_color};border-radius:5px;"></div>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:11px;color:#555;">
            <span>478 DBU used ({pct:.1f}%)</span>
            <span>${budget*0.06:.0f} est. monthly cost</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        sl("Per-agent DBU")
        for a in AGENT_COSTS:
            st.markdown(f"""
            <div style="background:#16161a;border-radius:12px;padding:12px 16px;
                        border:0.5px solid #252530;margin-bottom:8px;">
              <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px;">
                <span style="font-size:12px;font-weight:500;color:#f0f2f8;">{a['name']}</span>
                <span style="font-size:12px;color:#c1ff72;font-weight:500;">{a['dbu']} DBU</span>
              </div>
              <div style="background:#1e1e2a;border-radius:3px;height:4px;margin-bottom:4px;">
                <div style="width:{a['pct']}%;height:100%;background:#c1ff72;border-radius:3px;"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px;color:#555;">
                {badge(a['env'],a['env'])}<span>{a['pct']}% of fleet</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
        sl("Weekly DBU trend")
        colors = ["#1a3020"]*6 + ["#c1ff72"]
        st.plotly_chart(bar_chart(WEEK_DAYS, WEEKLY_DBU, colors, 160), use_container_width=True, config={"displayModeBar":False})


# ── ALERTS views ──────────────────────────────────────────────────────────────
def render_alerts(persona):
    render_topbar(persona, "Alerts")
    active   = [a for a in ALERTS if not a["resolved"]]
    resolved = [a for a in ALERTS if a["resolved"]]
    c1, c2, c3 = st.columns(3)
    with c1:
        crit = sum(1 for a in active if a["sev"]=="critical")
        st.markdown(f'<div style="background:#2a1212;border-radius:12px;padding:12px;border:0.5px solid #4a1515;text-align:center;"><div style="font-size:24px;font-weight:500;color:#ff6b6b;">{crit}</div><div style="font-size:11px;color:#ff6b6b;opacity:.7;">Critical</div></div>', unsafe_allow_html=True)
    with c2:
        warn = sum(1 for a in active if a["sev"]=="warning")
        st.markdown(f'<div style="background:#2a1e0a;border-radius:12px;padding:12px;border:0.5px solid #4a3000;text-align:center;"><div style="font-size:24px;font-weight:500;color:#f0a500;">{warn}</div><div style="font-size:11px;color:#f0a500;opacity:.7;">Warning</div></div>', unsafe_allow_html=True)
    with c3:
        info = sum(1 for a in active if a["sev"]=="info")
        st.markdown(f'<div style="background:#1a1e2a;border-radius:12px;padding:12px;border:0.5px solid #1a3050;text-align:center;"><div style="font-size:24px;font-weight:500;color:#6fa8f0;">{info}</div><div style="font-size:11px;color:#6fa8f0;opacity:.7;">Info</div></div>', unsafe_allow_html=True)

    show_rca = persona in ("dev", "admin")
    sl("Active alerts")
    for a in active:
        render_alert_card(a, show_rca=show_rca)

    sl("Resolved")
    for a in resolved:
        render_alert_card(a, show_rca=show_rca)

    if persona == "admin":
        sl("Alert rules")
        for rule, default in [("Agent down — 2 missed heartbeats",True),("p95 latency > 2s",True),("Error rate > 3%",True),("Missing env vars on deploy",True),("Build failure to prod",False),("Budget threshold 80%",True)]:
            st.toggle(rule, value=default, key=f"alert_rule_{rule}")


# ── Main app ──────────────────────────────────────────────────────────────────
def main():
    # Persona switcher
    if "persona" not in st.session_state:
        st.session_state.persona = "pm"
    if "tab" not in st.session_state:
        st.session_state.tab = "Overview"

    st.markdown('<div style="display:flex;gap:6px;margin-bottom:16px;">', unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns(3)
    persona_defs = [("pm","PM","#a78bfa","#14102a","#3a2a6a"), ("dev","Dev","#6fa8f0","#0a1525","#1a3050"), ("admin","Admin","#22c55e","#0d2218","#1a4a30")]
    for col, (k, label, color, bg, bd) in zip([pc1, pc2, pc3], persona_defs):
        with col:
            active = st.session_state.persona == k
            border = bd if active else "#252530"
            bgc    = bg if active else "#16161a"
            clr    = color if active else "#555"
            if st.button(label, key=f"persona_{k}"):
                st.session_state.persona = k
                st.session_state.tab = "Overview"
                st.rerun()
            # style the active persona button via JS trick
            if active:
                st.markdown(f"""
                <script>
                  const btns = window.parent.document.querySelectorAll('button');
                  btns.forEach(b => {{ if(b.innerText==='{label}') {{
                    b.style.background='{bg}';
                    b.style.color='{color}';
                    b.style.borderColor='{bd}';
                  }} }});
                </script>""", unsafe_allow_html=True)

    persona = st.session_state.persona
    tab = st.session_state.tab

    # Main tabs
    t1, t2, t3, t4, t5 = st.tabs(["Overview","Agents","Pipeline","Costs","Alerts"])

    with t1: render_overview(persona)
    with t2: render_agents(persona)
    with t3: render_pipeline(persona)
    with t4: render_costs(persona)
    with t5: render_alerts(persona)


if __name__ == "__main__":
    main()
