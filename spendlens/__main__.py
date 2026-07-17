"""CLI entry point: python -m spendlens <statement.csv>

Prints a spending summary by category.
"""

import argparse
from collections import defaultdict

from .categorize import categorize_transactions
from .parser import load_transactions


def main():
    ap = argparse.ArgumentParser(prog="spendlens")
    ap.add_argument("statement", help="path to a bank statement csv")
    args = ap.parse_args()

    txns = categorize_transactions(load_transactions(args.statement))

    totals = defaultdict(float)
    for t in txns:
        if t.amount < 0:
            totals[t.category] += -t.amount
    total_spend = sum(totals.values())

    print(f"\nspending by category ({len(txns)} transactions)\n")
    for category, amount in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
        pct = amount / total_spend * 100 if total_spend else 0
        print(f"  {category:<15} {amount:>12,.2f}   {pct:4.1f}%")
    print(f"  {'-' * 35}")
    print(f"  {'total':<15} {total_spend:>12,.2f}")


if __name__ == "__main__":
    main()
