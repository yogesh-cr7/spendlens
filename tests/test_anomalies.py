from datetime import date

from spendlens.anomalies import find_anomalies, find_duplicate_charges, find_price_increases
from spendlens.parser import Transaction


def txn(month, day, desc, amount):
    return Transaction(date=date(2026, month, day), description=desc, amount=amount)


def test_finds_duplicate_charge():
    txns = [
        txn(4, 8, "DOORDASH ORDER", -32.50),
        txn(4, 8, "DOORDASH ORDER", -32.50),
    ]
    dups = find_duplicate_charges(txns)
    assert len(dups) == 1
    assert dups[0].kind == "duplicate"


def test_no_duplicate_if_too_far_apart():
    txns = [
        txn(4, 1, "DOORDASH ORDER", -32.50),
        txn(4, 10, "DOORDASH ORDER", -32.50),
    ]
    assert find_duplicate_charges(txns, window_days=3) == []


def test_different_amounts_not_a_duplicate():
    txns = [
        txn(4, 8, "AMAZON MKTPLACE", -32.50),
        txn(4, 8, "AMAZON MKTPLACE", -19.99),
    ]
    assert find_duplicate_charges(txns) == []


def test_finds_price_increase():
    txns = [
        txn(4, 4, "NETFLIX.COM", -15.49),
        txn(5, 4, "NETFLIX.COM", -18.99),
    ]
    increases = find_price_increases(txns)
    assert len(increases) == 1
    assert increases[0].kind == "price_increase"


def test_small_price_changes_not_flagged():
    txns = [
        txn(4, 4, "NETFLIX.COM", -15.49),
        txn(5, 4, "NETFLIX.COM", -15.99),  # ~3% bump, under the 10% threshold
    ]
    assert find_price_increases(txns) == []


def test_find_anomalies_combines_both_checks():
    txns = [
        txn(4, 4, "NETFLIX.COM", -15.49),
        txn(4, 8, "DOORDASH ORDER", -32.50),
        txn(4, 8, "DOORDASH ORDER", -32.50),
        txn(5, 4, "NETFLIX.COM", -18.99),
    ]
    kinds = {a.kind for a in find_anomalies(txns)}
    assert kinds == {"duplicate", "price_increase"}
