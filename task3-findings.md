# Task 3: Data Analysis Findings

Analysis of 1,500,000 e-commerce orders for Swedish football club merchandise.

---

## Q1: Revenue & Growth by Club

**Finding:** Hammarby IF shows +127% revenue growth (second half vs first half of the dataset period), far ahead of the next fastest-growing clubs at ~47–50%. All clubs show positive growth; the slowest-growing clubs still achieve ~40%.

**Implication:** Hammarby IF's outsized growth may reflect a membership surge, a successful campaign, or expanding merchandise range. The gap between Hammarby and the rest of the league suggests uneven commercial development across clubs — a strategic concern for SEF if it aims to grow the collective commercial footprint.

**Recommended action:** Investigate the drivers behind Hammarby IF's growth (product mix, marketing activity, new customer acquisition) and identify transferable practices. Consider sharing learnings across clubs through SEF's commercial network.

---

## Q2: Return Rates by Payment Method

**Finding:** Klarna has a return rate of ~15%, roughly three times higher than Card, PayPal, Swish, and Invoice (~5% each).

**Implication:** Klarna's "buy now, pay later" model encourages speculative purchasing — customers order items they may not intend to keep. This inflates gross order volumes while creating real operational costs: reverse logistics, restocking, and delayed revenue recognition.

**Recommended action:** Evaluate whether Klarna's higher conversion rate justifies its return-rate cost. Consider introducing restocking fees for Klarna returns, adjusting return policy terms for deferred-payment methods, or surfacing size/fit guidance more prominently at checkout to reduce uncertainty-driven returns.

**Addtional Reflections** It is valid to investigate the cost vs. benefits of having Klarna, but part of the benefit analysis has to consider what the business case would look like if Klarna was not be available as a payment option - how much would this affect the average order value amounts and subsequent revenues? In marketing and ecommerce there tends to be the trend that, given the higher variety of payment methods available, the higher the revenue and customer LTV (life-time-value). Multiple studies in e‑commerce show that aligning checkout with customers’ preferred payment methods reduces cart abandonment and raises conversion and revenue, and that more flexible digital payment options (e.g. wallets, BNPL) can support higher order values and repeat purchasing, which are key drivers of customer lifetime value (see e.g. Monext, 2024; PayPal, 2024; Jadhav & Batish, 2024).

The investigation would need to include the analysis of if Klarna customers generally have higher average orde value and higher LTV than other customers using other payment methods.

---

## Q3: Geographic Distribution of Club Merchandise

**Finding:** Most clubs sell predominantly in their home city — AIK (47% Stockholm), Djurgårdens IF (50% Stockholm), Häcken (61% Göteborg), Sirius (54% Uppsala). Mjällby AIF has the most nationally distributed customer base, suggesting either a diaspora fanbase or broader brand appeal.

**Implication:** Heavy home-city concentration limits revenue ceiling and exposes clubs to local economic or demographic shifts. A geographically distributed fanbase is a commercial resilience indicator.

**Recommended action:** For concentrated clubs, explore targeted campaigns in secondary cities where they already have a footprint (e.g. Göteborg for Stockholm clubs). For Mjällby AIF, investigate what drives national reach and whether it can be scaled. SEF could support cross-club geographic analysis as part of a shared commercial intelligence offering.

**Addtional Reflections** While the analysis and suggestion is valid to explore and perhaps A/B test targeted campaigns in secondary cities they they have a footprint, the nature of Swedish football does naturally make it difficult for clubs to increase their geographical reach, with cultural aspects to consider. Primarily, it's crucial that the customer records and data is accurate towards a given individual - this being touched upon in Task 2 with the Contact Data Synchronisation Platform (ensuring a 'Golden Record') and the data quality task in Task 3 regarding multiple email addresses where each one has more than 1 'customer id' associated with it. This is so that retargeting efforts can be correctly targeted and relevant for the given customer/user. In reagrds to Mjällby AIF, one could assume a mix of the facts that it is a very small town in Sweden (where many have perhaps moved to other parts of h country), and their recent success in winning SM Guld in 2025 can be indicators of why their commercial fan following is more widespread across the country, the 'underdog' narrative that may have influenced football fans across the nation.

---

## Q4: Price Inconsistencies

**Finding:** 998 rows (0.07% of the dataset) have a `total_amount` that does not equal `quantity × unit_price`. The discrepancy pattern — totals both above and below the expected value — suggests applied discounts or manual price overrides not captured in a dedicated field.

**Implication:** The dataset contains a `discount_code` column that is almost entirely empty. If discounts are being applied at checkout but not recorded in the data, SEF and clubs lose visibility into promotional activity, making it difficult to measure campaign ROI or audit revenue accurately.

**Recommended action:** Audit the order management system to ensure discount amounts are written to the dataset at the time of transaction. Add a `discount_amount` column to the data model. Until then, treat `total_amount` as the authoritative revenue figure rather than the derived `quantity × unit_price`.

---

## Q5: Emails Linked to Multiple Customer IDs

**Finding:** 509 email addresses are each associated with more than one `customer_id`, representing duplicate customer records in the system.

**Implication:** Duplicate records distort customer lifetime value calculations, inflate unique customer counts, and can cause double-targeting in email marketing campaigns — undermining both analytics accuracy and customer experience.

**Recommended action:** Run a deduplication pass to merge records sharing the same email address. Introduce a uniqueness constraint on email at the account-creation layer to prevent future duplicates. Flag the 509 affected emails for CRM review to consolidate order history under a single canonical customer ID.

---

## Q6: Test / Placeholder Records

**Finding:** 104 rows (0.01%) were flagged as likely test or synthetic records based on heuristic signals: email addresses matching `@test.com` or similar domains, names such as "Test" or "Dummy", and zipcodes matching known placeholder patterns (e.g. `00000`, `12345`).

**Implication:** While the volume is small, the presence of test records in production data indicates that the system does not cleanly separate test and production environments, or that test accounts were never purged. This introduces noise into any analysis and could affect aggregated KPIs if not removed.

**Recommended action:** Purge confirmed test records from the production dataset. Implement environment tagging or a `is_test` flag at the data pipeline level. Add automated data quality checks to flag anomalous email domains and placeholder values before data reaches analytics systems.

---

## Reflection

**Tools used:** Python with `pandas` and `numpy`, run via the command line against a local CSV file.

**Why:** Pandas is well-suited to structured tabular data at this scale. Using categorical dtypes for low-cardinality string columns and `float32` for numeric fields reduced memory usage significantly and kept load time under 5 seconds for 1.5M rows. `numpy.isclose` allowed a fully vectorised price consistency check without any row-level iteration. All aggregations were expressed as `groupby` + `agg` operations, which are both readable and performant.

**What I learned from the data:** The data is largely clean — only 0.07% price mismatches and 0.01% test records — but the gaps that do exist (undocumented discounts, duplicate customer accounts, Klarna return behaviour) are commercially meaningful rather than just cosmetic data quality issues. One would need to assess the tradeoff of addressing these gaps in the data versus other competing priorities, and if the issues are systematic or relatively isolated. The most actionable finding is probably the Klarna return rate: it could be a large, measurable cost driver that can be acted on directly. The geographic concentration analysis was the most structurally interesting — it reframes what looks like strong home-city sales into a question about national growth potential.

**On the use of AI tools:** This analysis was completed using a combination of three AI tools, each serving a distinct role.

Perplexity AI was used as a starting point to structure how to approach the case — identifying what questions to ask of the data, how to frame the analysis, and what prompts to use when engaging other tools. It acted as a fast research and scaffolding layer, helping translate a broad brief into a concrete plan.

Claude (accessed via the terminal in Cursor IDE using Claude Code) was used to design and implement the analysis script. Claude's planning mode was particularly valuable: before writing any code, it produced a detailed implementation plan covering data loading strategy, each analytical question, performance considerations, and expected outputs. This made it possible to review and validate the approach before any code was committed.

Cursor AI Agent was used to provide a second opinion on Claude's proposed implementation plan. Having an independent model review the plan before execution added a useful layer of validation — surfacing any gaps in logic or alternative approaches worth considering.

The key learning from working across these tools is that the combination is powerful but requires conscious engagement. AI tools can generate plausible-sounding plans and code very quickly, which creates a risk of implementing suggestions without sufficiently scrutinising them. The most effective workflow was one where each tool's output was treated as a proposal to be evaluated rather than a decision to be accepted — using planning mode to make Claude's reasoning explicit, and using Cursor's agent to stress-test that reasoning before acting on it. Speed and quality are not in conflict when the human stays in the loop at the right moments.
