"""TCP Insight Lab: a focused educational congestion-control simulator."""

import pandas as pd
import streamlit as st

from simulation import metrics, simulate
from visualization import congestion_chart


st.set_page_config(page_title="TCP Insight Lab | Congestion Control", page_icon="📡", layout="wide")
st.markdown("""
<style>
  .block-container { max-width: 1240px; padding-top: 2rem; padding-bottom: 3rem; }
  .hero { background: linear-gradient(115deg,#082552,#185bb7); padding: 28px 32px; border-radius: 18px; color: #fff; margin-bottom: 1.35rem; }
  .hero h1 { margin: 0; font-size: 2.1rem; } .hero p { margin: 8px 0 0; color: #d9e8ff; }
  [data-testid="stSidebar"] { background: #0d1726; border-right: 1px solid #263b55; }
  [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
  [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: #edf5ff !important; }
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #aebfd3 !important; }
  [data-testid="stSidebar"] input { color: #edf5ff !important; }
  [data-testid="stSidebar"] [data-baseweb="select"] *, [data-testid="stSidebar"] [data-baseweb="input"] * { color: #edf5ff !important; }
  [data-testid="stSidebar"] [data-testid="stThumbValue"], [data-testid="stSidebar"] [data-testid="stSlider"] p { color: #edf5ff !important; }
  [data-testid="stSidebar"] [data-testid="stSidebarContent"] hr { border-color: #263b55; }
  [data-testid="stSidebar"] button[kind="primary"] { background: #2e7df6; color: #ffffff !important; border-color: #2e7df6; }
  [data-testid="stMetric"] { background: #152235; border: 1px solid #2e4662; border-radius: 12px; padding: 13px; }
  [data-testid="stMetric"] label, [data-testid="stMetric"] [data-testid="stMetricValue"] { color: #f4f8ff !important; }
  [data-testid="stMetric"] [data-testid="stMetricLabel"] { color: #b7c9dd !important; }
  .intro { color: #9eb0c7; margin-bottom: 1rem; }.callout{background:#11233a;border:1px solid #294562;border-radius:12px;padding:15px 18px;color:#d7e7fa}
</style>
<div class="hero"><h1>📡 TCP Insight Lab</h1><p>Visualise how TCP Tahoe and TCP Reno adjust the congestion window when the network is healthy or congested.</p></div>
""", unsafe_allow_html=True)


def run_simulation(algorithm, rounds, cwnd, ssthresh, loss_mode, loss_round, probability, seed, rwnd, rtt):
    algorithms = [algorithm] if algorithm != "Compare Tahoe and Reno" else ["TCP Tahoe", "TCP Reno"]
    return {
        name: simulate(name, rounds, cwnd, ssthresh, loss_mode, loss_round, probability, seed, rwnd, rtt)
        for name in algorithms
    }


if "results" not in st.session_state:
    st.session_state.results = run_simulation("TCP Reno", 30, 1.0, 16.0, "No loss", 12, 0.08, 7, 32.0, 80.0)

with st.sidebar:
    st.header("Simulation settings")
    st.caption("Change these inputs, then run the model.")
    algorithm = st.selectbox("TCP algorithm", ["TCP Reno", "TCP Tahoe", "Compare Tahoe and Reno"])
    st.divider()
    st.subheader("Starting conditions")
    cwnd = st.number_input("Initial cwnd (MSS)", min_value=1.0, max_value=128.0, value=1.0, step=1.0)
    ssthresh = st.number_input("Initial ssthresh (MSS)", min_value=2.0, max_value=256.0, value=16.0, step=1.0)
    rwnd = st.number_input("Receiver window / rwnd (MSS)", min_value=1.0, max_value=256.0, value=32.0, step=1.0)
    rtt = st.number_input("Base RTT (ms)", min_value=1.0, max_value=2000.0, value=80.0, step=5.0)
    rounds = st.slider("Number of rounds / RTTs", min_value=5, max_value=100, value=30)
    st.divider()
    st.subheader("Loss scenario")
    loss_mode = st.selectbox("Packet-loss event", ["No loss", "Loss at specific round", "Timeout at specific round", "Random loss"])
    loss_round = st.slider("Loss round", 1, rounds, min(12, rounds), disabled=loss_mode not in {"Loss at specific round", "Timeout at specific round"})
    probability = st.slider("Random-loss probability", 0.01, 0.50, 0.08, 0.01, disabled=loss_mode != "Random loss")
    seed = st.number_input("Random seed", min_value=0, value=7, step=1, disabled=loss_mode != "Random loss")
    if st.button("Run simulation", type="primary", use_container_width=True):
        st.session_state.results = run_simulation(algorithm, rounds, cwnd, ssthresh, loss_mode, loss_round, probability, int(seed), rwnd, rtt)

results = st.session_state.results
st.header("Congestion-window behaviour")
st.markdown("<p class='intro'>The line shows <b>cwnd</b>, the amount of data TCP can send before waiting for acknowledgments. Dotted vertical lines mark detected loss.</p>", unsafe_allow_html=True)
st.pyplot(congestion_chart(results), use_container_width=True)

overview, rounds_tab, analysis, learn = st.tabs(["Current state", "Round-by-round log", "Performance metrics", "How it works"])
with overview:
    selected = st.selectbox("View algorithm", list(results), key="overview")
    final = results[selected][-1]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current cwnd", f'{final["cwnd"]} MSS')
    c2.metric("Current ssthresh", f'{final["ssthresh"]} MSS')
    c3.metric("TCP state", final["state"])
    c4.metric("Latest RTT", f'{final["rtt_ms"]} ms')
    st.markdown(f"<div class='callout'><b>Last event:</b> {final['event']}</div>", unsafe_allow_html=True)
with rounds_tab:
    st.markdown("<p class='intro'>Each row represents one RTT. Watch cwnd, ssthresh, state, and event change over time.</p>", unsafe_allow_html=True)
    selected = st.selectbox("View algorithm", list(results), key="log")
    st.dataframe(pd.DataFrame(results[selected])[["round", "cwnd", "ssthresh", "state", "event", "effective_window", "rtt_ms"]], use_container_width=True, hide_index=True)
with analysis:
    st.markdown("<p class='intro'>Metrics are calculated from the congestion-control run above. Throughput is an educational estimate, not a live network measurement.</p>", unsafe_allow_html=True)
    for name, records in results.items():
        st.subheader(name)
        data = metrics(records)
        row1 = st.columns(4)
        row1[0].metric("Maximum cwnd", f'{data["maximum_cwnd"]} MSS')
        row1[1].metric("Average cwnd", f'{data["average_cwnd"]} MSS')
        row1[2].metric("Average RTT", f'{data["average_rtt_ms"]} ms')
        row1[3].metric("Throughput estimate", f'{data["throughput_estimate"]} MSS/s')
        row2 = st.columns(3)
        row2[0].metric("Packet-loss events", data["loss_events"])
        row2[1].metric("Timeouts", data["timeouts"])
        row2[2].metric("Recovery time", f'{data["recovery_time"]} rounds')
with learn:
    st.markdown("""
### TCP congestion control in this simulator

- **Slow Start:** cwnd doubles on each successful RTT until it reaches `ssthresh`.
- **Congestion Avoidance:** cwnd then grows by one MSS per RTT—TCP's additive increase.
- **Timeout:** Tahoe and Reno reduce `ssthresh` and reset cwnd to one MSS.
- **Three duplicate ACKs:** Tahoe returns to Slow Start. Reno performs fast retransmit/recovery and continues with a reduced window.
- **AIMD:** TCP increases gradually during normal delivery and decreases sharply when it detects congestion.

Use the loss scenario in the sidebar to see these responses in the graph and the metrics.
""")
