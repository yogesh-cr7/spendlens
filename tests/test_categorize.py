from spendlens.categorize import UNCATEGORISED, categorize, categorize_transactions
from spendlens.parser import load_transactions

from pathlib import Path

SAMPLES = Path(__file__).parent.parent / "data" / "samples"


def test_basic_matches():
    assert categorize("UPI-SWIGGY-ORDER") == "food delivery"
    assert categorize("RENT TRANSFER") == "rent"
    assert categorize("SALARY CREDIT ACME CORP") == "income"
    assert categorize("NETFLIX SUBSCRIPTION") == "entertainment"


def test_matching_is_case_insensitive():
    assert categorize("netflix") == categorize("NETFLIX")


def test_unknown_descriptions_fall_through():
    assert categorize("SOME RANDOM SHOP 4821") == UNCATEGORISED


def test_categorize_transactions_fills_field():
    txns = load_transactions(SAMPLES / "sample_statement.csv")
    assert all(t.category is None for t in txns)
    categorize_transactions(txns)
    assert all(t.category is not None for t in txns)
    # sample data is deliberately all recognisable
    assert not any(t.category == UNCATEGORISED for t in txns)
