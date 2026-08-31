"""Charts for the TCP simulator."""

import matplotlib.pyplot as plt


def congestion_chart(series: dict[str, list[dict]]):
    fig, ax = plt.subplots(figsize=(10, 4.8))
    palette = ["#2463eb", "#e55c30"]
    for (name, records), color in zip(series.items(), palette):
        rounds = [row["round"] for row in records]
        cwnds = [row["cwnd"] for row in records]
        ax.plot(rounds, cwnds, marker="o", linewidth=2.25, markersize=4, label=name, color=color)
        for row in records:
            if "duplicate ACKs" in row["event"] or "Timeout" in row["event"]:
                ax.axvline(row["round"], color=color, linestyle=":", alpha=0.45)
                ax.annotate("loss", (row["round"], row["cwnd"]), xytext=(4, 8), textcoords="offset points", color=color, fontsize=8)
    ax.set_title("TCP Congestion Window over Time", fontweight="bold")
    ax.set_xlabel("Round / RTT")
    ax.set_ylabel("Congestion window (MSS)")
    ax.grid(alpha=0.22)
    ax.set_xlim(left=1)
    ax.legend()
    fig.tight_layout()
    return fig
