"""Flag transactions worth a second look.

Two checks for now:
- duplicate charges: same description + amount within a few days (usually a
  double-swipe or a billing glitch)
- price increases: a recurring charge (same description) that jumped
  compared to last time (subscriptions creeping up)

Both are naive string-matching - if a merchant changes their description
slightly month to month (adds a date, a reference number, whatever) this
won't catch it. Good enough as a first pass; fuzzy matching is a TODO.
"""

from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Anomaly:
    kind: str  # "duplicate" or "price_increase"
    message: str
    transactions: list


def find_duplicate_charges(transactions, window_days=3):
    """Flag charges with identical description+amount within window_days."""
    anomalies = []
    spends = sorted((t for t in transactions if t.amount < 0), key=lambda t: t.date)
    seen = []
    for t in spends:
        for prior in seen:
            same_charge = prior.description == t.description and prior.amount == t.amount
            close_enough = (t.date - prior.date).days <= window_days
            if same_charge and close_enough:
                anomalies.append(
                    Anomaly(
                        kind="duplicate",
                        message=(
                            f"possible duplicate: {t.description} (${-t.amount:.2f}) "
                            f"on {prior.date} and {t.date}"
                        ),
                        transactions=[prior, t],
                    )
                )
        seen.append(t)
    return anomalies


def find_price_increases(transactions, threshold=0.10):
    """Flag recurring charges that rose by more than `threshold` (10% default)
    from their previous occurrence."""
    by_description = defaultdict(list)
    for t in transactions:
        if t.amount < 0:
            by_description[t.description].append(t)

    anomalies = []
    for description, txns in by_description.items():
        txns.sort(key=lambda t: t.date)
        for prev, curr in zip(txns, txns[1:]):
            prev_amt, curr_amt = -prev.amount, -curr.amount
            if prev_amt <= 0:
                continue
            increase = (curr_amt - prev_amt) / prev_amt
            if increase > threshold:
                anomalies.append(
                    Anomaly(
                        kind="price_increase",
                        message=(
                            f"{description} went up {increase * 100:.0f}%: "
                            f"${prev_amt:.2f} -> ${curr_amt:.2f}"
                        ),
                        transactions=[prev, curr],
                    )
                )
    return anomalies


def find_anomalies(transactions):
    return find_duplicate_charges(transactions) + find_price_increases(transactions)
