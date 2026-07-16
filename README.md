# spendlens

Analyze bank statement CSVs — categorize spending, flag unusual transactions,
and (eventually) ask questions about where your money went in plain English.

Started this because my bank's app is useless for actually understanding
spending patterns across months.

Work in progress. Rough plan:

- [ ] parse bank statement CSVs (different banks = different formats, fun)
- [ ] rule-based categorization to start
- [ ] LLM categorization for the messy stuff rules can't handle
- [ ] anomaly detection (subscriptions creeping up, duplicate charges)
- [ ] agent that answers questions like "why was March so expensive?"

## Setup

```
python -m venv venv
venv\Scripts\activate      # windows
pip install -r requirements.txt
```
