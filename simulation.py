"""Deterministic round-based models of TCP Tahoe and TCP Reno."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import random


class State(str, Enum):
    SLOW_START = "Slow Start"
    CONGESTION_AVOIDANCE = "Congestion Avoidance"
    FAST_RECOVERY = "Fast Recovery"


@dataclass
class RoundRecord:
    round: int
    cwnd: float
    ssthresh: float
    state: str
    event: str
    rwnd: float
    effective_window: float
    segments_sent: int
    ack_number: int
    rtt_ms: float

    def to_dict(self):
        return asdict(self)


def _loss_event(round_no: int, mode: str, loss_round: int, probability: float, rng: random.Random) -> str | None:
    if mode == "No loss":
        return None
    if mode == "Loss at specific round" and round_no == loss_round:
        return "Triple duplicate ACK"
    if mode == "Timeout at specific round" and round_no == loss_round:
        return "Timeout"
    if mode == "Random loss" and rng.random() < probability:
        return "Triple duplicate ACK"
    return None


def simulate(
    algorithm: str,
    rounds: int = 30,
    initial_cwnd: float = 1.0,
    initial_ssthresh: float = 16.0,
    loss_mode: str = "No loss",
    loss_round: int = 12,
    loss_probability: float = 0.08,
    seed: int = 7,
    receiver_window: float = 32.0,
    base_rtt_ms: float = 80.0,
) -> list[dict]:
    """Run a simplified TCP congestion-control simulation, one RTT per round.

    A loss is detected either as a timeout or as three duplicate ACKs.  The model
    deliberately favors explainable, textbook behavior over wire-level fidelity.
    """
    if algorithm not in {"TCP Tahoe", "TCP Reno"}:
        raise ValueError("algorithm must be TCP Tahoe or TCP Reno")

    cwnd = max(float(initial_cwnd), 1.0)
    ssthresh = max(float(initial_ssthresh), 2.0)
    state = State.SLOW_START if cwnd < ssthresh else State.CONGESTION_AVOIDANCE
    rng = random.Random(seed)
    records: list[RoundRecord] = []
    next_sequence = 1

    for round_no in range(1, rounds + 1):
        loss = _loss_event(round_no, loss_mode, loss_round, loss_probability, rng)
        event = "ACK received"

        if loss == "Timeout":
            ssthresh = max(cwnd / 2, 2.0)
            cwnd = 1.0
            state = State.SLOW_START
            event = "Timeout → cwnd reset to 1"
        elif loss == "Triple duplicate ACK":
            ssthresh = max(cwnd / 2, 2.0)
            if algorithm == "TCP Tahoe":
                cwnd = 1.0
                state = State.SLOW_START
                event = "3 duplicate ACKs → Tahoe restarts Slow Start"
            else:
                cwnd = ssthresh
                state = State.CONGESTION_AVOIDANCE
                event = "3 duplicate ACKs → Reno fast retransmit/recovery"
        else:
            if state == State.SLOW_START:
                cwnd *= 2
                event = "ACK received → exponential growth"
                if cwnd >= ssthresh:
                    state = State.CONGESTION_AVOIDANCE
                    event += "; enter Congestion Avoidance"
            else:
                cwnd += 1
                state = State.CONGESTION_AVOIDANCE
                event = "ACK received → additive increase"

        effective_window = min(cwnd, receiver_window)
        segments_sent = max(1, int(effective_window))
        ack_number = next_sequence + segments_sent
        rtt_ms = base_rtt_ms + (effective_window * 1.6) + (35 if loss else 0)
        records.append(RoundRecord(
            round_no, round(cwnd, 2), round(ssthresh, 2), state.value, event,
            receiver_window, round(effective_window, 2), segments_sent, ack_number, round(rtt_ms, 1),
        ))
        next_sequence = ack_number

    return [record.to_dict() for record in records]


def metrics(records: list[dict]) -> dict[str, float | int | str]:
    cwnds = [row["cwnd"] for row in records]
    losses = [row for row in records if "duplicate ACKs" in row["event"] or "Timeout" in row["event"]]
    timeouts = [row for row in records if "Timeout" in row["event"]]
    recovery_lengths: list[int] = []
    for loss in losses:
        after = [row for row in records if row["round"] > loss["round"] and row["cwnd"] >= loss["ssthresh"]]
        if after:
            recovery_lengths.append(after[0]["round"] - loss["round"])
    return {
        "maximum_cwnd": max(cwnds) if cwnds else 0,
        "average_cwnd": round(sum(cwnds) / len(cwnds), 2) if cwnds else 0,
        "loss_events": len(losses),
        "timeouts": len(timeouts),
        "recovery_time": round(sum(recovery_lengths) / len(recovery_lengths), 1) if recovery_lengths else "N/A",
        "average_rtt_ms": round(sum(row["rtt_ms"] for row in records) / len(records), 1) if records else 0,
        "segments_delivered": sum(row["segments_sent"] for row in records) - len(losses),
        "throughput_estimate": round(sum(row["segments_sent"] for row in records) / sum(row["rtt_ms"] for row in records) * 1000, 2) if records else 0,
    }


def handshake_trace() -> list[dict]:
    """Return the fixed, illustrative three-way TCP connection setup."""
    return [
        {"Step": 1, "From": "Client", "To": "Server", "Flags": "SYN", "Sequence": 1000, "Acknowledgment": "—", "Meaning": "Request a connection"},
        {"Step": 2, "From": "Server", "To": "Client", "Flags": "SYN, ACK", "Sequence": 5000, "Acknowledgment": 1001, "Meaning": "Accept and acknowledge"},
        {"Step": 3, "From": "Client", "To": "Server", "Flags": "ACK", "Sequence": 1001, "Acknowledgment": 5001, "Meaning": "Connection established"},
    ]
