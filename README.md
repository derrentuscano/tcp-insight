# TCP Insight Lab

Interactive CN mini-project focused on TCP Tahoe and TCP Reno congestion control in RTT-sized rounds.

> This is an educational simulator. It models TCP behavior; it does not modify your computer's actual TCP stack.

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Run the activation command again whenever you open a new terminal before
launching the application.  `(.venv)` at the beginning of the prompt confirms
that the virtual environment is active.

## Features

- TCP Tahoe and TCP Reno, with a comparison view
- Configurable starting cwnd, ssthresh, receiver window, RTT, rounds, and loss scenario
- Slow Start, Congestion Avoidance (AIMD), and Reno fast recovery behavior
- No loss, specific loss, timeout, and reproducible random loss modes
- cwnd-over-time chart with loss annotations
- Full event table and calculated RTT, throughput, max/average cwnd, loss count, timeout count, and recovery time

## Project structure

```text
tcp-congestion-simulator/
├── app.py                 # Streamlit interface
├── simulation.py          # Tahoe and Reno simulation engine
├── visualization.py       # Congestion-window chart
├── ui_components.py       # Reusable interface components
├── requirements.txt       # Python dependencies
└── .streamlit/config.toml # Dark-mode application theme
```

## Upload to GitHub

To push this project to the `tcp-insight` repository, configure the remote once, then push from this project folder:

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/tcp-insight.git
git push -u origin main
```
