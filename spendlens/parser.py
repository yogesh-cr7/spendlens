"""Load transactions from bank statement CSVs.

Every bank exports slightly different CSVs - different column names,
different date formats - so this normalises them into one Transaction shape.
"""

import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y")

# different banks name their columns differently
COLUMN_ALIASES = {
    "date": {"date", "txn date", "transaction date", "value date"},
    "description": {"description", "narration", "details", "particulars"},
    "amount": {"amount", "txn amount"},
}

# TODO: some banks split amount into separate debit/credit columns,
# need to handle that once I get a sample statement in that format


class ParseError(Exception):
    pass


@dataclass
class Transaction:
    date: date
    description: str
    amount: float  # negative = money out, positive = money in


def _parse_date(raw):
    raw = raw.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    raise ParseError(f"unrecognised date: {raw!r}")


def _match_columns(header):
    """Map our field names to whatever the bank called them."""
    mapping = {}
    lowered = {col.lower().strip(): col for col in header}
    for field, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in lowered:
                mapping[field] = lowered[alias]
                break
        else:
            raise ParseError(f"couldn't find a column for {field!r} in {header}")
    return mapping


def load_transactions(path):
    """Read a statement CSV and return a list of Transactions."""
    path = Path(path)
    transactions = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ParseError(f"{path} is empty")
        cols = _match_columns(reader.fieldnames)
        for row in reader:
            amount = float(row[cols["amount"]].replace(",", ""))
            transactions.append(
                Transaction(
                    date=_parse_date(row[cols["date"]]),
                    description=row[cols["description"]].strip(),
                    amount=amount,
                )
            )
    return transactions
