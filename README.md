# 🍎 FruitBudget Analytics
### How Much Does It Cost U.S. Households to Eat Enough Fruit?

> **A data-driven dashboard answering one of the most practical questions in American household economics — built on official USDA pricing data and the federal dietary guidelines.**

### Dasboard Previews:


<img width="1856" height="973" alt="Screenshot from 2026-03-22 15-59-29" src="https://github.com/user-attachments/assets/6a47b43c-c831-44ea-8f04-561fa8390aad" />




<img width="1856" height="973" alt="Screenshot from 2026-03-22 15-59-58" src="https://github.com/user-attachments/assets/b135fd32-649b-400d-8998-057d03a2fbc0" />

### Explore App : https://py.cafe/SmartDvi/Fruit%20Budget%20Analytics%20for%20U.S%20Household 

---

## 📌 Table of Contents

1. [The Question This Project Answers](#the-question-this-project-answers)
2. [The Short Answer](#the-short-answer)
3. [Understanding the Data](#understanding-the-data)
4. [Key Findings — Explained for Everyone](#key-findings--explained-for-everyone)
   - [What Is a Cup-Equivalent?](#what-is-a-cup-equivalent)
   - [Annual Cost by Preparation Form](#annual-cost-by-preparation-form)
   - [What Best-Case, Typical, and Worst-Case Mean](#what-best-case-typical-and-worst-case-mean)
   - [Full Form-by-Form Breakdown](#full-form-by-form-breakdown)
   - [The Cheapest Fruits Available](#the-cheapest-fruits-available)
   - [The Most Expensive Fruits Available](#the-most-expensive-fruits-available)
   - [What This Costs Different Households](#what-this-costs-different-households)
5. [Project Structure](#project-structure)
6. [How to Run the Dashboard](#how-to-run-the-dashboard)
7. [Data Source & Methodology](#data-source--methodology)
8. [Limitations & Disclaimers](#limitations--disclaimers)
9. [Related Publications](#related-publications)

---

## The Question This Project Answers

**"How much money does it cost U.S. households to eat a sufficient quantity and variety of fruits?"**

The U.S. Department of Agriculture (USDA) recommends that adults eat **1.5 to 2 cups of fruit per day** as part of a healthy diet. This project calculates exactly what that commitment costs — broken down by fruit type, preparation method (fresh, canned, frozen, dried, juice), household size, and shopping strategy.

This is not a theoretical exercise. Families, policymakers, nutrition educators, and SNAP program administrators all need to understand whether meeting federal dietary guidelines is financially realistic for the average American household.

---

## The Short Answer

| Scenario | Daily Cost | Monthly Cost | Annual Cost |
|---|---|---|---|
| **Single adult — average mix** | $1.51 | $46.00 | **$552.02** |
| **Couple — average mix** | $3.02 | $92.00 | **$1,104.03** |
| **Family of 3 — average mix** | $4.54 | $138.00 | **$1,656.05** |
| **Family of 4 — average mix** | $6.05 | $184.01 | **$2,208.07** |
| **Family of 5 — average mix** | $7.56 | $230.01 | **$2,760.08** |

> *Based on the median cup-equivalent price of $1.0082 across all 62 fruit items, at 1.5 cups per person per day.*

**The most important single number:** A family of four can meet the USDA fruit recommendation for roughly **$6.05 per day** — less than the cost of a fast-food meal.

---

## Understanding the Data

### Dataset at a Glance

| Metric | Value |
|---|---|
| Data source | USDA ERS Fruit & Vegetable Prices (Updated Dec 9, 2025) |
| Total fruit items analyzed | **62** |
| Preparation forms covered | **5** (Fresh, Canned, Frozen, Dried, Juice) |
| Unique base fruits | **29** |
| Lowest cost per cup-equivalent | **$0.2429** — Watermelon (fresh) |
| Highest cost per cup-equivalent | **$3.5556** — Canned cherries in syrup |
| Median cost per cup-equivalent | **$1.0082** |
| Mean cost per cup-equivalent | **$1.0651** |

### Dataset Composition

Of the 62 items analyzed:

| Form | Items | Share |
|---|---|---|
| Fresh | 24 | 38.7% |
| Canned | 12 | 19.4% |
| Juice | 11 | 17.7% |
| Dried | 9 | 14.5% |
| Frozen | 6 | 9.7% |

Fresh fruits make up the largest share of the market — nearly 4 in 10 items tracked are fresh.

---

## Key Findings — Explained for Everyone

### What Is a Cup-Equivalent?

The USDA measures fruit consumption in **cup-equivalents** — a standardized unit that lets you compare apples to orange juice fairly. One cup-equivalent equals:

- 1 cup of fresh or frozen fruit (roughly a large handful)
- 1 cup of 100% fruit juice
- ½ cup of dried fruit

This matters because a pound of watermelon and a pound of raisins are very different amounts of food. Cup-equivalents level the playing field.

**The cup-equivalent price** is the cost to get one serving of that fruit — the single most useful number for comparing value across forms.

---

### Annual Cost by Preparation Form

This is the headline analysis. We looked at every fruit in the dataset and asked: *if you ate only this form of fruit at 1.5 cups per day, what would it cost you per year?*

The chart groups results into three scenarios per form:

- **Best-case** — the cheapest option available in that form category
- **Typical** — the average price across all items in that form
- **Worst-case** — the most expensive option available in that form category

---

### What Best-Case, Typical, and Worst-Case Mean

**Why three scenarios?**

Because the word "fresh" or "canned" covers an enormous price range. A can of peaches and a can of cherries in syrup are both "canned," but they cost very differently. Similarly, buying the cheapest fresh fruit (watermelon at $0.24/cup) is a completely different financial reality than buying the most expensive (raspberries at $2.58/cup).

These three scenarios tell a household: *here is the floor, the typical expectation, and the ceiling if you shop without checking prices.*

---

### Full Form-by-Form Breakdown

#### 🍹 Juice — The Most Affordable Form on Average

| Scenario | Annual Cost per Person | What That Means Daily |
|---|---|---|
| **Best-case** | **$166.60/yr** | $0.46/day |
| **Typical** | **$328.35/yr** | $0.90/day |
| **Worst-case** | **$897.57/yr** | $2.46/day |

**What this means in plain language:**

Juice is the most budget-friendly category overall. The best-case of **$166.60/year** is achievable with frozen concentrate — apple, grape, orange, or pineapple juice concentrate consistently delivers the lowest cost per cup in the entire dataset, often under $0.40/cup. At the typical price of **$328.35/year** ($27.36/month), juice represents a reasonable fruit budget for a single adult. The worst-case of **$897.57/year** reflects premium bottled juices like pomegranate, which cost $1.64/cup.

**What it means for U.S. households:** Frozen concentrate juice is the most cost-effective single strategy for meeting daily fruit recommendations. A family of four relying on an average juice mix would spend approximately **$1,313/year** — compared to $8,826/year if they chose the most expensive juice options.

> ⚠️ **Important:** The USDA counts only 100% fruit juice toward daily intake, and recommends no more than one cup per day from juice. Juice alone should not be the only fruit source in a balanced diet.

---

#### 🍇 Dried — Predictable, Moderate Cost

| Scenario | Annual Cost per Person | What That Means Daily |
|---|---|---|
| **Best-case** | **$342.84/yr** | $0.94/day |
| **Typical** | **$566.35/yr** | $1.55/day |
| **Worst-case** | **$706.82/yr** | $1.94/day |

**What this means in plain language:**

Dried fruit is the most *consistent* form — the gap between cheapest and most expensive ($342 to $706) is the narrowest of all five forms. This means there are no budget surprises: no matter which dried fruit you buy, the price will fall within a predictable, moderate range. The typical shopper spends about **$566/year** ($47/month) on dried fruit.

**What it means for U.S. households:** Dried fruit is uniquely practical — it doesn't spoil, requires no refrigeration, and is portion-portable. Cranberries ($0.63/cup) and raisins ($0.66/cup) are the standout values. For families focused on reducing food waste or stocking emergency pantries, dried fruit provides excellent nutritional value per dollar of shelf space.

---

#### 🍓 Fresh — The Widest Price Range of Any Form

| Scenario | Annual Cost per Person | What That Means Daily |
|---|---|---|
| **Best-case** | **$132.99/yr** | $0.36/day |
| **Typical** | **$566.68/yr** | $1.55/day |
| **Worst-case** | **$1,410.09/yr** | $3.86/day |

**What this means in plain language:**

Fresh fruit has the most dramatic price spread in the entire analysis — a difference of over **$1,277 per year** between the best and worst options. This is because "fresh fruit" spans everything from watermelon ($0.24/cup) and bananas ($0.31/cup) all the way up to raspberries ($2.58/cup) and blackberries ($2.25/cup).

The best-case of **$132.99/year** ($11.08/month) is the single lowest annual cost in this entire analysis — achievable by routinely choosing watermelon, bananas, pineapple, cantaloupe, and apples. The worst-case of **$1,410/year** would mean exclusively buying premium fresh berries year-round.

**What it means for U.S. households:** Fresh fruit can be the cheapest *or* the most expensive form — the difference depends entirely on which fruits you choose. Strategic shoppers who follow seasonal availability and prioritize high-yield staples can eat very well on very little. The risk is that shopping habits and brand preferences quietly push families toward high-cost fresh items without realizing the magnitude of the difference.

**For a family of four at the typical fresh price:** $566.68 × 4 = **$2,266.72/year** ($188.89/month). Switching from a worst-case to a best-case fresh shopping strategy for that same family saves over **$5,085/year**.

---

#### 🥫 Canned — Most Expensive on Average, But Good Value Options Exist

| Scenario | Annual Cost per Person | What That Means Daily |
|---|---|---|
| **Best-case** | **$346.13/yr** | $0.95/day |
| **Typical** | **$761.01/yr** | $2.09/day |
| **Worst-case** | **$1,946.69/yr** | $5.33/day |

**What this means in plain language:**

Canned fruit is the most expensive category on average, and its worst-case ($1,946/year) is the highest of any form — driven by canned cherries packed in syrup at $3.56/cup, the single most expensive item in the entire dataset. However, well-chosen canned fruit — peaches or pears packed in *juice* — is affordable and nutritious.

The critical distinction is the **packing medium**:
- Fruit packed in **juice**: $0.63–$1.29/cup — reasonable value
- Fruit packed in **syrup or water**: $1.22–$3.56/cup — significantly more expensive

**What it means for U.S. households:** For food security, emergency preparedness, and consistent availability regardless of season, canned fruit is uniquely valuable. Its shelf life is measured in years, not days. However, canned purchases require label literacy — choosing juice-packed over syrup-packed cuts annual cost nearly in half while also reducing added sugar intake.

**For a family of four at the typical canned price:** $761.01 × 4 = **$3,044.04/year** ($253.67/month) — more than double the best-case scenario for the same nutritional outcome.

---

#### ❄️ Frozen — High Floor, Narrow Range, Excellent Nutritional Value

| Scenario | Annual Cost per Person | What That Means Daily |
|---|---|---|
| **Best-case** | **$605.10/yr** | $1.66/day |
| **Typical** | **$785.27/yr** | $2.15/day |
| **Worst-case** | **$1,115.15/yr** | $3.06/day |

**What this means in plain language:**

Frozen fruit has the highest best-case floor of all five forms — even the cheapest frozen option costs $605/year per person. This is because the frozen category is concentrated in higher-value items: berries, peaches, and mixed fruit blends. There are no budget "anchors" in frozen the way watermelon and bananas anchor the fresh category.

However, frozen's price range is relatively narrow ($605 to $1,115), which means predictability. Frozen strawberries ($1.11/cup) offer reasonable value; frozen raspberries ($2.04/cup) are the costliest frozen option.

**What it means for U.S. households:** Frozen fruit is nutritionally comparable — and often superior — to fresh, as it is typically harvested and frozen at peak ripeness with no transport degradation. For families who want berries regularly (among the most antioxidant-rich foods available), frozen is typically 40–60% cheaper than fresh equivalents. The tradeoff is that the frozen category costs more overall than strategic fresh or juice shopping.

---

### The Cheapest Fruits Available

These 15 items deliver the most affordable cup-equivalent price in the entire dataset:

| Rank | Fruit | Form | Cost per Cup | Annual Cost (1 Person) |
|---|---|---|---|---|
| 1 | Watermelon | Fresh | $0.2429 | $133.01 |
| 2 | Apples, frozen concentrate | Juice | $0.3043 | $166.60 |
| 3 | Bananas | Fresh | $0.3085 | $168.90 |
| 4 | Pineapple, frozen concentrate | Juice | $0.3628 | $198.63 |
| 5 | Oranges, frozen concentrate | Juice | $0.3669 | $200.88 |
| 6 | Grapes, frozen concentrate | Juice | $0.3762 | $205.98 |
| 7 | Apples, ready-to-drink | Juice | $0.4350 | $238.16 |
| 8 | Pineapple | Fresh | $0.4401 | $240.95 |
| 9 | Apples | Fresh | $0.4996 | $273.53 |
| 10 | Grapes, ready-to-drink | Juice | $0.5254 | $287.66 |
| 11 | Oranges, ready-to-drink | Juice | $0.5286 | $289.41 |
| 12 | Cantaloupe | Fresh | $0.5529 | $302.74 |
| 13 | Grapefruit, ready-to-drink | Juice | $0.5968 | $326.74 |
| 14 | Pineapple, ready-to-drink | Juice | $0.6122 | $335.28 |
| 15 | Cranberries | Dried | $0.6262 | $342.84 |

**Key insight for households:** A family that builds its fruit intake around this list — watermelon, bananas, pineapple, apples, cantaloupe, and frozen concentrate juices — can fully meet the USDA daily recommendation for as little as **$0.37–$0.94 per person per day**.

---

### The Most Expensive Fruits Available

| Rank | Fruit | Form | Cost per Cup | Annual Cost (1 Person) |
|---|---|---|---|---|
| 1 | Cherries, packed in syrup or water | Canned | $3.5556 | $1,946.69 |
| 2 | Raspberries | Fresh | $2.5755 | $1,410.09 |
| 3 | Blackberries | Fresh | $2.2473 | $1,230.39 |
| 4 | Raspberries | Frozen | $2.0368 | $1,115.15 |
| 5 | Cherries | Fresh | $1.7320 | $948.53 |
| 6 | Pomegranate, ready-to-drink | Juice | $1.6394 | $897.57 |
| 7 | Blackberries | Frozen | $1.5965 | $874.02 |
| 8 | Apricots, packed in syrup or water | Canned | $1.5168 | $830.70 |
| 9 | Pomegranate | Fresh | $1.5054 | $824.46 |
| 10 | Fruit cocktail, packed in syrup or water | Canned | $1.4242 | $779.84 |

**Key insight:** Canned cherries in syrup cost **14.6 times more per cup** than watermelon. A household that regularly buys fresh raspberries or blackberries is spending more than 10× what they would on a budget mix — for the same number of nutritional cup-equivalents.

---

### What This Costs Different Households

#### 🛒 Budget Strategy — Median of Cheapest 25% ($0.4401/cup)

*Achievable by choosing items like watermelon, bananas, pineapple, frozen concentrate juices, and cantaloupe.*

| Household | Daily | Weekly | Monthly | **Annual** |
|---|---|---|---|---|
| Single Adult | $0.66 | $4.63 | $20.08 | **$240.95** |
| Couple | $1.32 | $9.27 | $40.16 | **$481.91** |
| Family of 3 | $1.98 | $13.90 | $60.24 | **$722.86** |
| Family of 4 | $2.64 | $18.54 | $80.32 | **$963.82** |
| Family of 5 | $3.30 | $23.17 | $100.40 | **$1,204.77** |

#### ⚖️ Average Strategy — Median across all items ($1.0082/cup)

*Represents typical U.S. market purchasing behavior.*

| Household | Daily | Weekly | Monthly | **Annual** |
|---|---|---|---|---|
| Single Adult | $1.51 | $10.62 | $46.00 | **$552.02** |
| Couple | $3.02 | $21.23 | $92.00 | **$1,104.03** |
| Family of 3 | $4.54 | $31.85 | $138.00 | **$1,656.05** |
| Family of 4 | $6.05 | $42.46 | $184.01 | **$2,208.07** |
| Family of 5 | $7.56 | $53.08 | $230.01 | **$2,760.08** |

#### 🌟 Premium Strategy — Median of Most Expensive 25% ($1.5111/cup)

*Reflects consistent purchasing of berries, specialty fruits, and premium-packaged items.*

| Household | Daily | Weekly | Monthly | **Annual** |
|---|---|---|---|---|
| Single Adult | $2.27 | $15.91 | $68.94 | **$827.33** |
| Couple | $4.53 | $31.82 | $137.89 | **$1,654.65** |
| Family of 3 | $6.80 | $47.73 | $206.83 | **$2,481.98** |
| Family of 4 | $9.07 | $63.64 | $275.78 | **$3,309.31** |
| Family of 5 | $11.33 | $79.55 | $344.72 | **$4,136.64** |

**The strategic takeaway:** The difference between budget and premium shopping is **$1,245.49/year for a family of four**. A household that makes informed, value-conscious fruit choices — prioritizing frozen concentrate juice, fresh watermelon and bananas, and juice-packed canned fruit — can save over $1,200 annually while meeting the exact same USDA dietary recommendation. This is the central insight this project delivers.

---

## Project Structure

```
Analysis-for-a-cost-of-2-cup-recommendation-by-USDA-for-a-household/
│
├── run.py              # Dash dashboard application — run this to launch
├── utils.py            # All data loading, calculations, and analysis functions
├── EDA.ipynb           # Exploratory Data Analysis notebook
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project configuration
├── uv.lock             # Dependency lock file
│
└── data/
    ├── fruits.csv      # USDA ERS fruit pricing data (62 items, 5 forms)
    └── vegetables.csv  # USDA ERS vegetable pricing data
```

### File Responsibilities

**`utils.py`** — The analytical engine. Loads the CSV, computes cup-equivalent prices from first principles, and exposes clean functions for every analysis in the dashboard. All calculations are reproducible and documented inline.

**`run.py`** — The Dash web application. Imports from `utils.py` and renders six interactive tabs: Overview, By Form, Households, Explorer, Heatmap, and Data Source. Supports light and dark mode with a toggle in the header.

**`data/fruits.csv`** — The raw data. Contains retail prices, yield factors, and cup-equivalent sizes for 62 fruit items from USDA ERS Circana scanner data (2023).

**`data/vegetables.csv`** — Vegetable pricing data for a complete household diet cost analysis (not yet integrated into the dashboard).

---

## How to Run the Dashboard

### Prerequisites

- Python 3.9 or higher
- `uv` package manager (recommended) or `pip`

### Install dependencies

**Using uv (recommended):**
```bash
uv sync
```

**Using pip:**
```bash
pip install -r requirements.txt
```

### Launch the dashboard

```bash
python run.py
```

Open your browser to: **http://127.0.0.1:8050**

### Custom CSV path

```bash
# CLI argument
python run.py --csv /path/to/your/fruits.csv

# Environment variable
FRUITS_CSV=/path/to/fruits.csv python run.py
```

### Core Dependencies

| Package | Purpose |
|---|---|
| `dash` | Web application framework |
| `dash-mantine-components` | Professional UI component library |
| `dash-iconify` | Icon support |
| `plotly` | Interactive charts and visualizations |
| `pandas` | Data manipulation and analysis |
| `numpy` | Numerical calculations |

---

## Data Source & Methodology

### Primary Data Source

**USDA Economic Research Service (ERS) — Fruit and Vegetable Prices**
- 🔗 https://www.ers.usda.gov/data-products/fruit-and-vegetable-prices/
- Last updated: **December 9, 2025**
- Data year: **2023** retail scanner data from Circana

### Dietary Recommendation Basis

**USDA Dietary Guidelines for Americans 2020–2025**
- Recommended daily fruit intake: **1.5 to 2 cups per day for adults**
- This analysis baseline: **1.5 cups/day** (conservative midpoint)
- Children: 1–1.5 cups/day | Active adults: up to 2.5 cups/day

### Price Calculation Formulas

**Weight-based items (sold per pound):**
```
CupEquivalentPrice = (RetailPrice × CupEquivalentSize) / Yield
```

**Volume-based items / juices (sold per pint):**
```
CupEquivalentPrice = RetailPrice × (CupEquivalentSize / 16) / Yield
```
*1 pint = 16 fl oz · 1 cup-equivalent of juice = 8 fl oz*

**Yield** is the edible fraction of the purchased item. A whole pineapple has a yield of 0.51 — 49% is rind and core. Canned fruit in juice has a yield of 1.00 — everything purchased is consumed.

**Annual household cost:**
```
Annual = CupEquivalentPrice × cups_per_day × 365 × household_members
```

### Strategy Definitions

| Strategy | Reference Price | Method |
|---|---|---|
| Budget | $0.4401/cup | Median of cheapest 25% of items |
| Average | $1.0082/cup | Median across all 62 items |
| Premium | $1.5111/cup | Median of most expensive 25% of items |

---

## Limitations & Disclaimers

1. **Prices are point-in-time estimates.** 2023 Circana scanner data reflects average retail prices across a national store sample. Actual prices vary by region, season, store type, and promotions.

2. **Year-to-year comparisons are not valid.** Due to methodology changes across survey years (2013, 2016, 2020, 2022, 2023), prices from different periods should not be compared directly.

3. **This analysis covers fruits only.** The full USDA recommendation covers combined fruit and vegetable intake. The `vegetables.csv` file enables a complete household diet cost analysis.

4. **The "average" strategy is not a shopping recommendation.** It is a statistical midpoint representing the median market price. Real households mix budget and premium choices based on preference, availability, and season.

5. **SNAP context.** The average monthly SNAP benefit for a family of four is approximately $973 (FY2024). Fruit at the average mix represents about **18.9% of that benefit** ($184/month). Budget-conscious fruit choices are material for food-assistance households.

6. **Findings should not be attributed to Circana.** Retail scanner data was provided by Circana. All analysis and conclusions are those of this project.

---

## Related Publications

- [Satisfying Fruit & Vegetable Recommendations Possible for Under $3/Day — USDA ERS (2024)](https://www.ers.usda.gov/amber-waves/2024/september/satisfying-fruit-and-vegetable-recommendations-possible-for-under-3-a-day-data-analysis-shows/)
- [The Cost of Satisfying Fruit & Vegetable Recommendations in the Dietary Guidelines — USDA ERS](https://www.ers.usda.gov/publications/pub-details/?pubid=42904)
- [SNAP Households & Fruit/Vegetable Affordability — USDA ERS (2021)](https://www.ers.usda.gov/amber-waves/2021/july/for-supplemental-nutrition-assistance-program-snap-households-fruit-and-vegetable-affordability-is-partly-a-question-of-budgeting/)
- [Americans Can Meet F&V Guidelines for $2.10–$2.60/Day — USDA ERS (2019)](https://www.ers.usda.gov/amber-waves/2019/june/americans-still-can-meet-fruit-and-vegetable-dietary-guidelines-for-2-10-2-60-per-day/)
- [USDA Dietary Guidelines for Americans 2020–2025](https://www.dietaryguidelines.gov/resources/2020-2025-dietary-guidelines-online-materials)
- [Download: All Fruits Average Prices CSV — USDA ERS](https://www.ers.usda.gov/media/6210/all-fruits-average-prices-csv-format.csv)

---

## License

This project uses publicly available USDA government data. Analysis, code, and visualizations are available for educational and non-commercial use.

---

*Built with [Dash](https://dash.plotly.com/) · [Dash Mantine Components](https://www.dash-mantine-components.com/) · [Plotly](https://plotly.com/) · Data: [USDA ERS](https://www.ers.usda.gov/data-products/fruit-and-vegetable-prices/)*
