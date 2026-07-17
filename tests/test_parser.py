from datetime import date
from pathlib import Path

import pytest

from spendlens.parser import ParseError, Transaction, load_transactions

SAMPLES = Path(__file__).parent.parent / "data" / "samples"


def test_loads_sample_statement():
    txns = load_transactions(SAMPLES / "sample_statement.csv")
    assert len(txns) == 15
    assert txns[0] == Transaction(date(2026, 5, 1), "PAYROLL DEPOSIT ACME CORP", 4850.0)


def test_amounts_keep_their_sign():
    txns = load_transactions(SAMPLES / "sample_statement.csv")
    spends = [t for t in txns if t.amount < 0]
    credits = [t for t in txns if t.amount > 0]
    assert len(spends) == 13
    assert len(credits) == 2  # salary + a refund


def test_recognises_other_column_names(tmp_path):
    f = tmp_path / "hdfc_style.csv"
    f.write_text("Txn Date,Narration,Amount\n03/05/2026,COFFEE,-120\n")
    txns = load_transactions(f)
    assert txns[0].date == date(2026, 5, 3)  # dd/mm/yyyy, not mm/dd
    assert txns[0].amount == -120


def test_unknown_columns_raise(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text("foo,bar\n1,2\n")
    with pytest.raises(ParseError):
        load_transactions(f)


def test_amounts_with_commas(tmp_path):
    f = tmp_path / "commas.csv"
    f.write_text('date,description,amount\n2026-05-01,RENT,"-15,000.00"\n')
    txns = load_transactions(f)
    assert txns[0].amount == -15000.0
