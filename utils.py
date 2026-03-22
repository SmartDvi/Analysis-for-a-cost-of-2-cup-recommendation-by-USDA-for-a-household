import pandas as pd
import numpy as np

# ── DATA SOURCE ──────────────────────────────────────────────────────────────
CSV_PATH = 'https://raw.githubusercontent.com/SmartDvi/Analysis-for-a-cost-of-2-cup-recommendation-by-USDA-for-a-household/refs/heads/main/data/fruits.csv'

# ── CONSTANTS ────────────────────────────────────────────────────────────────
DAILY_CUPS_ADULT = 1.5          # USDA recommended midpoint for adults
DAYS_PER_YEAR    = 365

HOUSEHOLD_SIZES = {
    "Single Adult": 1,
    "Couple":       2,
    "Family of 3":  3,
    "Family of 4":  4,
    "Family of 5":  5,
}

FORM_COLORS = {
    "Fresh":  "#2d8b6e",
    "Canned": "#e07b39",
    "Frozen": "#4a90d9",
    "Dried":  "#9b59b6",
    "Juice":  "#f1c40f",
}

# Expected columns coming from the CSV
_REQUIRED_COLS = {
    "Fruit", "Form", "RetailPrice", "RetailPriceUnit",
    "Yield", "CupEquivalentSize", "CupEquivalentUnit",
}


# ── LOAD & CLEAN DATA ────────────────────────────────────────────────────────
def load_data(path: str = CSV_PATH) -> pd.DataFrame:
    """Load the fruit CSV, clean types, and compute derived columns."""
    df = pd.read_csv(path)

    missing = _REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing expected columns: {missing}")

    # Clean types
    df["RetailPrice"]       = pd.to_numeric(df["RetailPrice"],       errors="coerce")
    df["Yield"]             = pd.to_numeric(df["Yield"],             errors="coerce")
    df["CupEquivalentSize"] = pd.to_numeric(df["CupEquivalentSize"], errors="coerce")

    df = df.dropna(subset=["RetailPrice", "Yield", "CupEquivalentSize"]).copy()
    df = df[df["Yield"] > 0].copy()   # guard against zero-division

    # Compute CupEquivalentPrice from first principles
    df["CupEquivalentPrice"] = df.apply(_cup_price, axis=1).round(4)

    # Derived columns
    df["BaseFruit"] = (
        df["Fruit"]
        .str.split(",").str[0]
        .str.split("(").str[0]
        .str.strip()
    )
    df["Daily_Cost"]   = (df["CupEquivalentPrice"] * DAILY_CUPS_ADULT).round(4)
    df["Weekly_Cost"]  = (df["Daily_Cost"] * 7).round(2)
    df["Monthly_Cost"] = (df["Daily_Cost"] * 30.44).round(2)
    df["Annual_Cost"]  = (df["Daily_Cost"] * DAYS_PER_YEAR).round(2)

    return df.reset_index(drop=True)


def _cup_price(row) -> float:
    """Compute the cost per cup-equivalent for a single row."""
    if str(row["CupEquivalentUnit"]).strip().lower() == "fluid ounces":
        # RetailPrice is per pint (16 fl oz); cup-equiv is 8 fl oz
        return row["RetailPrice"] * (row["CupEquivalentSize"] / 16.0) / row["Yield"]
    else:
        # RetailPrice is per pound
        return (row["RetailPrice"] * row["CupEquivalentSize"]) / row["Yield"]


# ── ANALYSIS FUNCTIONS ───────────────────────────────────────────────────────

def cost_summary_by_form(df: pd.DataFrame) -> pd.DataFrame:
    """Average, min, and max annual per-person cost grouped by preparation form."""
    grp = (
        df.groupby("Form")["CupEquivalentPrice"]
        .agg(AvgCupPrice="mean", MinCupPrice="min", MaxCupPrice="max", Count="count")
        .reset_index()
    )
    grp["Annual_Avg"] = (grp["AvgCupPrice"] * DAILY_CUPS_ADULT * DAYS_PER_YEAR).round(2)
    grp["Annual_Min"] = (grp["MinCupPrice"] * DAILY_CUPS_ADULT * DAYS_PER_YEAR).round(2)
    grp["Annual_Max"] = (grp["MaxCupPrice"] * DAILY_CUPS_ADULT * DAYS_PER_YEAR).round(2)
    return grp.sort_values("AvgCupPrice").reset_index(drop=True)


def cheapest_items(df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    """Return the n lowest cup-equivalent-cost items."""
    return (
        df[["Fruit", "Form", "CupEquivalentPrice", "RetailPrice", "RetailPriceUnit", "Yield"]]
        .sort_values("CupEquivalentPrice")
        .head(n)
        .reset_index(drop=True)
    )


def most_expensive_items(df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    """Return the n highest cup-equivalent-cost items."""
    return (
        df[["Fruit", "Form", "CupEquivalentPrice", "RetailPrice", "RetailPriceUnit", "Yield"]]
        .sort_values("CupEquivalentPrice", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


def best_value_per_base_fruit(df: pd.DataFrame) -> pd.DataFrame:
    """For each base fruit, return the cheapest cup-equivalent form available."""
    idx = df.groupby("BaseFruit")["CupEquivalentPrice"].idxmin()
    return (
        df.loc[idx, ["BaseFruit", "Fruit", "Form", "CupEquivalentPrice"]]
        .reset_index(drop=True)
    )


def household_annual_budget(df: pd.DataFrame, strategy: str = "average") -> pd.DataFrame:
    """
    Project annual, monthly, weekly, and daily fruit cost for each household size.

    strategy
    --------
    'budget'  — median of the cheapest 25% of items
    'average' — overall median price
    'premium' — median of the most expensive 25% of items
    """
    prices = df["CupEquivalentPrice"].sort_values().values
    n = len(prices)

    if strategy == "budget":
        ref = float(np.median(prices[: max(1, n // 4)]))
    elif strategy == "premium":
        ref = float(np.median(prices[3 * n // 4 :]))
    else:
        ref = float(np.median(prices))

    rows = []
    for label, members in HOUSEHOLD_SIZES.items():
        annual = round(DAILY_CUPS_ADULT * ref * DAYS_PER_YEAR * members, 2)
        rows.append({
            "Household":    label,
            "Members":      members,
            "PricePerCup":  round(ref, 4),
            "Annual_Cost":  annual,
            "Monthly_Cost": round(annual / 12, 2),
            "Weekly_Cost":  round(annual / 52, 2),
            "Daily_Cost":   round(annual / DAYS_PER_YEAR, 2),
        })
    return pd.DataFrame(rows)


def price_range_stats(df: pd.DataFrame) -> dict:
    """Descriptive statistics for CupEquivalentPrice."""
    p = df["CupEquivalentPrice"]
    return {
        "min":    round(float(p.min()),          4),
        "max":    round(float(p.max()),          4),
        "mean":   round(float(p.mean()),         4),
        "median": round(float(p.median()),       4),
        "std":    round(float(p.std()),          4),
        "q25":    round(float(p.quantile(0.25)), 4),
        "q75":    round(float(p.quantile(0.75)), 4),
    }


def form_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Count and percentage of items by preparation form."""
    counts = df["Form"].value_counts().reset_index()
    counts.columns = ["Form", "Count"]
    counts["Percentage"] = (counts["Count"] / len(df) * 100).round(1)
    return counts