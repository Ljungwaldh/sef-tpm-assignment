import os
import time
import numpy as np
import pandas as pd

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── 1. Load ──────────────────────────────────────────────────────────────────
print("\n=== LOADING DATA ===\n")
t0 = time.time()

dtype_map = {
    "club":             "category",
    "country":          "category",
    "city":             "category",
    "payment_method":   "category",
    "order_status":     "category",
    "product_category": "category",
    "product_name":     "category",
    "quantity":         "int16",
    "unit_price":       "float32",
    "total_amount":     "float32",
}

df = pd.read_csv(
    "ecommerce_orders_1.5M.csv",
    dtype=dtype_map,
    parse_dates=["order_date"],
    engine="c",
)

load_time = time.time() - t0
mem_mb = df.memory_usage(deep=True).sum() / 1024**2
print(f"Loaded {len(df):,} rows in {load_time:.1f}s  |  Memory: {mem_mb:.1f} MB")

# ── 2. Revenue & Orders per Club — Monthly ───────────────────────────────────
print("\n=== CLUB MONTHLY REVENUE & GROWTH ===\n")

df["year_month"] = df["order_date"].dt.to_period("M")

club_monthly = (
    df.groupby(["club", "year_month"], observed=True)
    .agg(revenue=("total_amount", "sum"), orders=("order_id", "count"))
    .reset_index()
)

# Growth: compare revenue in first half of timeline vs second half
periods = sorted(df["year_month"].unique())
mid = periods[len(periods) // 2]

early = club_monthly[club_monthly["year_month"] < mid].groupby("club", observed=True)["revenue"].sum()
recent = club_monthly[club_monthly["year_month"] >= mid].groupby("club", observed=True)["revenue"].sum()

growth = ((recent - early) / early.replace(0, np.nan)).dropna().sort_values()

print("Top 5 fastest-growing clubs (revenue growth rate):")
print(growth.tail(5).apply(lambda x: f"{x:+.1%}").to_string())
print("\nTop 5 most stagnating clubs (revenue growth rate):")
print(growth.head(5).apply(lambda x: f"{x:+.1%}").to_string())

club_monthly.to_csv(f"{OUTPUT_DIR}/club_monthly_revenue.csv", index=False)

# ── 3. Return Rates by Payment Method ────────────────────────────────────────
print("\n=== RETURN RATES BY PAYMENT METHOD ===\n")

total_by_pm = df.groupby("payment_method", observed=True)["order_id"].count().rename("total_orders")
returned_by_pm = (
    df[df["order_status"] == "Returned"]
    .groupby("payment_method", observed=True)["order_id"]
    .count()
    .rename("returned_count")
)

return_rates = pd.concat([total_by_pm, returned_by_pm], axis=1).fillna(0)
return_rates["returned_count"] = return_rates["returned_count"].astype(int)
return_rates["return_rate_%"] = (return_rates["returned_count"] / return_rates["total_orders"] * 100).round(2)
print(return_rates.sort_values("return_rate_%", ascending=False).to_string())

return_rates.to_csv(f"{OUTPUT_DIR}/return_rates_by_payment.csv")

# ── 4. Geographic Distribution of Club Merchandise ───────────────────────────
print("\n=== GEOGRAPHIC DISTRIBUTION OF CLUB MERCHANDISE ===\n")

geo = (
    df.groupby(["club", "country", "city"], observed=True)["order_id"]
    .count()
    .reset_index(name="city_orders")
)

club_totals = geo.groupby("club", observed=True)["city_orders"].sum().rename("club_total")
geo = geo.join(club_totals, on="club")
geo["share"] = geo["city_orders"] / geo["club_total"]

hhi = geo.groupby("club", observed=True)["share"].apply(lambda s: (s**2).sum()).rename("HHI")

print("Top 3 most geographically concentrated clubs (high HHI):")
print(hhi.sort_values(ascending=False).head(3).to_string())
print("\nTop 3 most geographically distributed clubs (low HHI):")
print(hhi.sort_values(ascending=True).head(3).to_string())

top10_clubs = club_totals.nlargest(10).index
print("\nTop 3 cities per club (10 largest clubs):")
for club in top10_clubs:
    top_cities = (
        geo[geo["club"] == club]
        .nlargest(3, "city_orders")[["city", "country", "city_orders", "share"]]
    )
    top_cities["share"] = top_cities["share"].apply(lambda x: f"{x:.1%}")
    print(f"\n  {club}")
    print(top_cities.to_string(index=False))

geo.to_csv(f"{OUTPUT_DIR}/club_geo_distribution.csv", index=False)

# ── 5. Price Inconsistency Check ─────────────────────────────────────────────
print("\n=== PRICE INCONSISTENCY CHECK ===\n")

mask = ~np.isclose(
    df["total_amount"].astype("float64"),
    df["quantity"].astype("float64") * df["unit_price"].astype("float64"),
    rtol=1e-3,
)
mismatches = df[mask]
mismatch_count = mask.sum()
mismatch_pct = mismatch_count / len(df) * 100

print(f"Price mismatches: {mismatch_count:,} rows ({mismatch_pct:.2f}% of dataset)")
if mismatch_count > 0:
    sample = mismatches[["order_id", "quantity", "unit_price", "total_amount"]].head(5)
    sample = sample.copy()
    sample["expected"] = (sample["quantity"] * sample["unit_price"]).round(2)
    print("\nSample mismatched rows:")
    print(sample.to_string(index=False))
    mismatches.to_csv(f"{OUTPUT_DIR}/price_mismatches.csv", index=False)
else:
    pd.DataFrame().to_csv(f"{OUTPUT_DIR}/price_mismatches.csv", index=False)

# ── 6. Email Shared by Multiple Customer IDs ─────────────────────────────────
print("\n=== EMAILS USED BY MULTIPLE CUSTOMER IDs ===\n")

email_cust_count = df.groupby("email")["customer_id"].nunique()
shared = email_cust_count[email_cust_count > 1]

print(f"Emails shared by >1 customer_id: {len(shared):,}")
if len(shared) > 0:
    print("\nTop 10 examples:")
    for email in shared.nlargest(10).index:
        cids = df[df["email"] == email]["customer_id"].unique().tolist()
        print(f"  {email}: {cids}")

    shared_df = (
        df[df["email"].isin(shared.index)]
        .groupby("email")["customer_id"]
        .unique()
        .reset_index()
    )
    shared_df["customer_ids"] = shared_df["customer_id"].apply(lambda x: ", ".join(x))
    shared_df[["email", "customer_ids"]].to_csv(f"{OUTPUT_DIR}/shared_emails.csv", index=False)
else:
    pd.DataFrame().to_csv(f"{OUTPUT_DIR}/shared_emails.csv", index=False)

# ── 7. Heuristic Test/Placeholder Detection ───────────────────────────────────
print("\n=== SUSPECTED TEST / PLACEHOLDER RECORDS ===\n")

test_keywords = r"test|placeholder|dummy|example|noreply|fake"
suspicious_domains = r"@test\.|@example\.|@mailinator\.|@yopmail\."
dummy_zip_pattern = r"^0+$|^1{4,}|^9{4,}|^12345|^00000"
dummy_names = {"test", "dummy", "fake", "admin", "user", "n/a", "na", "unknown"}

email_col = df["email"].fillna("").astype(str)
first_lower = df["first_name"].fillna("").astype(str).str.lower()
last_lower  = df["last_name"].fillna("").astype(str).str.lower()
zip_col     = df["zipcode"].fillna("").astype(str)

mask_email_kw   = email_col.str.contains(test_keywords, case=False, regex=True, na=False)
mask_email_dom  = email_col.str.contains(suspicious_domains, case=False, regex=True, na=False)
mask_name       = first_lower.isin(dummy_names) | last_lower.isin(dummy_names)
mask_zip        = zip_col.str.match(dummy_zip_pattern, na=False)

combined_mask = mask_email_kw | mask_email_dom | mask_name | mask_zip

test_rows = df[combined_mask].copy()
total_test = combined_mask.sum()

print(f"Total suspected test/placeholder rows: {total_test:,} ({total_test/len(df)*100:.2f}% of dataset)")
print("\nBreakdown by detection reason:")
print(f"  Email contains test keywords : {mask_email_kw.sum():,}")
print(f"  Suspicious email domain      : {mask_email_dom.sum():,}")
print(f"  Dummy first/last name        : {mask_name.sum():,}")
print(f"  Dummy zipcode pattern        : {mask_zip.sum():,}")
print(f"  (rows may match multiple criteria)")

test_rows.to_csv(f"{OUTPUT_DIR}/suspected_test_records.csv", index=False)

# ── Final Summary ─────────────────────────────────────────────────────────────
print("\n=== SUMMARY ===\n")
print(f"Total rows analysed      : {len(df):,}")
print(f"Suspected test rows      : {total_test:,}")
print(f"Price mismatches         : {mismatch_count:,}")
print(f"Output CSVs saved to     : {OUTPUT_DIR}/")
print(f"Total elapsed time       : {time.time() - t0:.1f}s")
