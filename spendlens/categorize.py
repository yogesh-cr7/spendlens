"""Assign categories to transactions by matching keywords in the description.

Dumb but effective first pass. Anything the rules don't recognise gets
'uncategorised' - the plan is to send those to an LLM later instead of
growing this keyword list forever.
"""

# order matters: "uber eats" must be checked before "uber" catches it
# as transport, so food delivery sits above transport
CATEGORY_RULES = {
    "income": ("payroll", "salary", "direct deposit"),
    "rent": ("rent",),
    "food delivery": ("doordash", "grubhub", "uber eats", "postmates"),
    "groceries": ("trader joe", "whole foods", "safeway", "kroger", "costco", "aldi"),
    "transport": ("uber", "lyft", "amtrak", "mta", "gas station", "shell", "chevron", "exxon"),
    "shopping": ("amazon", "target", "walmart", "best buy"),
    "entertainment": ("netflix", "spotify", "hulu", "amc", "regal", "movie"),
    "utilities": ("con edison", "coned", "electric", "t-mobile", "verizon", "comcast", "internet"),
    "health": ("cvs", "walgreens", "pharmacy", "clinic", "hospital"),
}

UNCATEGORISED = "uncategorised"


def categorize(description):
    """Return a category name for a transaction description."""
    desc = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(keyword in desc for keyword in keywords):
            return category
    return UNCATEGORISED


def categorize_transactions(transactions):
    """Fill in the category field on every transaction. Mutates in place."""
    for txn in transactions:
        txn.category = categorize(txn.description)
    return transactions
