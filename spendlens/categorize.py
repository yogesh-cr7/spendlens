"""Assign categories to transactions by matching keywords in the description.

Dumb but effective first pass. Anything the rules don't recognise gets
'uncategorised' - the plan is to send those to an LLM later instead of
growing this keyword list forever.
"""

CATEGORY_RULES = {
    "income": ("salary",),
    "rent": ("rent",),
    "food delivery": ("swiggy", "zomato"),
    "groceries": ("bigbasket", "blinkit", "grofers", "dmart", "groceries"),
    "transport": ("uber", "ola", "petrol", "fuel", "metro"),
    "shopping": ("amazon", "flipkart", "myntra"),
    "entertainment": ("netflix", "spotify", "prime video", "pvr", "movie", "bookmyshow"),
    "utilities": ("electricity", "bescom", "water bill", "broadband", "recharge", "jio", "airtel"),
    "health": ("pharmacy", "apollo", "hospital", "clinic"),
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
