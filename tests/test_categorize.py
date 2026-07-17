from spendlens.categorize import UNCATEGORISED, categorize, categorize_transactions
from spendlens.parser import load_transactions

from pathlib import Path

SAMPLES = Path(__file__).parent.parent / "data" / "samples"


def test_basic_matches():
    assert categorize("DOORDASH ORDER") == "food delivery"
    assert categorize("ZELLE RENT PAYMENT") == "rent"
    assert categorize("PAYROLL DEPOSIT ACME CORP") == "income"
    assert categorize("NETFLIX.COM") == "entertainment"

def test_travel_bookings():
    assert categorize("LYFT RIDE 05-07") == "transport"
    assert categorize("AMTRAK TICKETS") == "transport"

def test_uber_eats_is_food_not_transport():
    # "uber eats" contains "uber", so rule order decides this one
    assert categorize("UBER EATS") == "food delivery"
    assert categorize("UBER TRIP") == "transport"

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
