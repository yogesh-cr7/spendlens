# spendlens

Analyze bank statement CSVs — categorize spending, flag unusual transactions,
and (eventually) ask questions about where your money went in plain English.

Started this because my bank's app is useless for actually understanding
spending patterns across months.

Work in progress. 


Rough plan:

- [x] parse bank statement CSVs (different banks = different formats, fun)
- [x] rule-based categorization to start
- [ ] LLM categorization for the messy stuff rules can't handle
- [x] anomaly detection (subscriptions creeping up, duplicate charges)
- [ ] agent that answers questions like "why was March so expensive?"

## Setup

```
python -m venv venv
venv\Scripts\activate      # windows
pip install -r requirements.txt
```

## Usage

```
python -m spendlens data/samples/sample_statement.csv
```

Prints a spending summary by category:

```
spending by category (15 transactions)

  rent                1,800.00   74.3%
  utilities             164.30    6.8%
  shopping              129.99    5.4%
  ...
```

If it finds a duplicate charge or a recurring bill that jumped in price, it says so:

```
worth a look (2):

  [duplicate] possible duplicate: DOORDASH ORDER ($32.50) on 2026-04-08 and 2026-04-08
  [price_increase] NETFLIX.COM went up 23%: $15.49 -> $18.99
```

(try it: `python -m spendlens data/samples/statement_with_anomalies.csv`)
