# Phase calendar

The season has four phases. Each needs a different amount of cover and asks different questions.

| Phase | Dates | What shoppers ask about | In the forecast |
|---|---|---|---|
| 1. Four weeks before the sale | Roughly late October to the week before Black Friday | Early deals, "will this be on sale", sizing, stock | Only the last week is forecast (`pre_sale`). The weeks before that are for building this plan, hiring and training |
| 2. BFCM week | Black Friday to the Thursday after Cyber Monday | Discount codes, stacking, stock-outs, order changes, "where is my order" starts | `bfcm_week` |
| 3. Early December to the holiday | The Friday after BFCM week to the day before the holiday | Delivery: "will it arrive in time", late shipments, cutoff dates, gift options | `december` |
| 4. After the holiday to mid-January | The holiday to the end date | Returns, exchanges, gift returns without a receipt, refunds not yet received | `returns` |

## 2026 dates

Black Friday is Friday 27 November 2026 (it was Friday 28 November 2025). Cyber Monday is 30 November. Christmas Day 2026 is a Friday, and 1 January 2027 is a Friday. Every date seven days apart falls on the same weekday.

## If the merchant has last year's daily counts, use them

Do not turn a daily export into phase factors. Averages flatten every spike inside a phase: in a worked example, last year's Black Friday was 180 tickets, the BFCM-week average 143, and a phase-mode forecast gave Black Friday 2026 about 166 against the 198 the daily data implies at 10 percent growth. The pre-Christmas rush on the last Monday and Tuesday and the 29 to 31 December returns days vanished the same way. Use `baseline.method: "daily_series"` instead. The script matches each 2026 day to last year's day (same weekday and distance from Black Friday before Christmas Eve, same calendar date from Christmas Eve on).

## Phase mode: when the merchant has only a BFCM-week figure

Phase factors are ratios of **average days, all days included**:

- factor for a phase = average day in that phase / average day in BFCM week (week total / 7).
- weekend factor = average weekend day / average weekday, **each averaged separately** across the season.

The script then splits each phase average into a weekday level and a weekend level that add back up to the phase total, so a weekend is lowered once, not twice. Do not multiply a phase average by the weekend factor yourself.

If the merchant is recalling rather than measuring, ask: "Was December about half as busy as sale week? A quarter? About the same?" Label the answer merchant-chosen estimate. Never supply a factor yourself. If they cannot say, mark `[DECISION NEEDED: how busy was <phase> compared with BFCM week last year?]` and offer to run a low and a high value they name.

## New store: no last year

Ask for the last four normal weeks: messages per week, or orders per week and messages per 100 orders (messages divided by orders, times 100). Then ask how much busier they expect each phase to be than a normal day now: the uplift. It comes from their own plan (discount depth, ad budget, email list), not from you. Do not quote an industry uplift. If they have no number, ask for their expected BFCM-week order lift in plain words ("about double a normal week? triple?") and add scenarios with every day's forecast times 1.5 and 2, labelled as scenarios, so they see what happens if the sale beats their guess. The returns phase for a new store depends on how much they sell in BFCM week and December, so ask them to reason from that.

## Things merchants underestimate

**The returns wave comes after the holiday, not during the sale.** Loop Returns data for 26 December 2024 to 12 January 2025 puts the top US return day on 26 December, the UK on 2 January and Australia and New Zealand on 6 January (https://www.loopreturns.com/blog/post-holiday-returns-sales-trends-data-loop/). A roster that ends a week after Cyber Monday misses it. Keep cover for two to three weeks after the holiday.

**Weekends do not go quiet the same way for every message.** Chatty's own platform data (1,530,306 shopper messages to stores' AI chat, 1 June to 14 September 2026, outside peak season, days in UTC) shows weekend volume against weekdays at 100: shopping questions 89, order questions (post-purchase) 61. So a weekend day can be anywhere from about 0.6 to 0.9 of a weekday depending on the mix. It is one data point for the merchant to weigh, not their weekend factor. Many small teams roster nobody at weekends, and the plan will show those days as gaps and the Monday backlog.

**December is long.** BFCM is four days of spike; December is three weeks of steady delivery questions. A lower level over more days can add up to more total hours than BFCM week. The phase summary shows this.
