# SEF E-Commerce Orders Analysis

Exploratory data analysis of 1.5 million e-commerce orders for Swedish football club merchandise, conducted as a case assignment for Svensk Elitfotboll (SEF).

## Questions Answered

1. **Revenue & growth by club** — Monthly revenue and order counts per club, with fastest-growing and most stagnating clubs identified.
2. **Return rates by payment method** — Which payment methods correlate with higher return rates.
3. **Geographic distribution** — Where each club's merchandise is bought, with concentration metrics (HHI) per club.
4. **Price inconsistencies** — Orders where `total_amount ≠ quantity × unit_price`.
5. **Shared emails** — Email addresses linked to multiple distinct customer IDs.
6. **Test/placeholder records** — Heuristic detection of synthetic or dummy rows in the dataset.

## Usage

```bash
pip install pandas numpy
python3 analysis.py
```

Output CSVs are written to the `output/` directory.

> **Dataset note:** Raw dataset `ecommerce_orders_1.5M.csv` is not included in this repository due to size.
> It was provided via Dropbox by Svensk Elitfotboll for this case assignment.
> Place the CSV in the project root before running `analysis.py`.

## Business Findings

- **Hammarby IF** is the standout growth club (+127% revenue, second half vs first half of the period), well ahead of the next fastest-growing clubs (~47–50%).
- All clubs show positive revenue growth; the "stagnating" group is simply growing more slowly (~40%).
- **Klarna** has a return rate of ~15%, three times higher than all other payment methods (~5%). This is consistent with Klarna's "buy now, decide later" model and represents a meaningful operational cost.
- Club merchandise is heavily concentrated in home cities: AIK (47% Stockholm), Djurgårdens IF (50% Stockholm), Häcken (61% Göteborg), Sirius (54% Uppsala). **Mjällby AIF** has the most nationally distributed customer base.

## Data Quality Findings

- **998 rows (0.07%)** have a `total_amount` that does not match `quantity × unit_price`. These likely reflect discounts applied at checkout that are not captured in a dedicated discount column.
- **509 emails** are associated with more than one `customer_id`, suggesting duplicate account creation or data entry errors.
- **104 rows (0.01%)** were flagged as likely test or placeholder records based on email patterns (e.g. `@test.com`), dummy names, or suspicious zipcodes.
