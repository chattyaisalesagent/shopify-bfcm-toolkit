# Phase calendar

The season has four phases. Each needs a different amount of cover and asks different questions, and the forecast treats each separately so the roster can too.

| Phase | Dates | What shoppers ask about | In the forecast |
|---|---|---|---|
| 1. Four weeks before the sale | Roughly late October to the week before Black Friday | Early deals, "will this be on sale", sizing, stock | Only the last week is forecast (`pre_sale`). The weeks before that are for building this plan, hiring and training |
| 2. BFCM week | Black Friday to the Thursday after Cyber Monday | Discount codes, stacking, stock-outs, order changes, "where is my order" starts | `bfcm_week`, factor fixed at 1.0. Everything else is measured against it |
| 3. Early December to the holiday | The Friday after BFCM week to the day before the holiday | Delivery: "will it arrive in time", late shipments, cutoff dates, gift options | `december` |
| 4. After the holiday to mid-January | The holiday to the end date | Returns, exchanges, gift returns without a receipt, refunds not yet received | `returns` |

## Things merchants underestimate

**The returns wave comes after the holiday, not during the sale.** Loop Returns data across Shopify merchants puts the US returns peak on 26 December; the same data shows the UK peaking around 2 January and Australia and New Zealand around 6 January. A roster that ends on Cyber Monday plus one week misses it. Keep cover for two to three weeks after the holiday, and consider a `day_overrides` entry for the peak day in the merchant's main market.

**Weekends do not go quiet.** One retailer platform's data shows weekend shopping messages staying at 89 for every 100 on weekdays. Treat that as one data point for the merchant to weigh, not as their weekend factor. Many small teams roster nobody at weekends, and the plan will show those days as gaps.

**December is long.** BFCM is four days of spike; December is three weeks of steady delivery questions. A lower factor over more days can add up to more total hours than BFCM week. The phase summary shows this.

## Helping the merchant choose phase factors

Best: derive them from last year's daily export. Average daily volume in each phase divided by average daily volume in BFCM week. Label merchant-stated.

Next best: ask them to recall. "Was December about half as busy as sale week? A quarter? About the same?" Label merchant-chosen estimate.

Never supply a factor yourself. If they cannot say, mark `[DECISION NEEDED: how busy was <phase> compared with BFCM week last year?]` and offer to run two versions (a low and a high factor they name) so they can see how much it changes the roster.
