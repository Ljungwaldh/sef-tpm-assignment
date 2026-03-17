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

## AI Tools Used (for whole case assignment)

- **Notebook LM** Using source material of the case, the job description, and Svensk Elitfotboll website, creating an AI generated podcast to introduce and give initial guidance on how to solve the case and respective questions
- **Perpelxity** Overall structure and layering of the case assignment, used for deep research into tools such as Symplify and topics such as Mata Data Management (MDM). 
- **Claude** Used the browser version to help construct the Symplify User Guide and the PRD documents with carefully designed prompts created by Perplexity. Used Claude Code in generating the analysis and code in Github
- **Cursor** Used this IDE for interacting with Claude Code, and also using the Cursor AI Agent to consult with concerning the implementation plan suggested by Claude Code to ensure a conscious review and second opinion.

## AI Reflections
- When used in combination with one another and applying their respective strengths in respective phases of the case assignemnt, these tools can be very powerful in efficiently created content, code, and deeper understanding of technical platofrms and concepts - work that would take a considerably larger amount of time if AI wouldn't be utilised. At the very least, these tools help to generate extensive and high quality foundations, first drafts, and MVP's.
- A limitation is the level of trust in the output from AI tools - that these can efficiently generate content, however, that one must take caution and add the human element in validating what has been produced. For example, during the data analysis, I would find myself questioning some of the logic and conclusions AI has generated about the data, where it may not capture fully an understanding of how football business and the football world works (eg. AI's insights on Klarna and on geographical concentration).
