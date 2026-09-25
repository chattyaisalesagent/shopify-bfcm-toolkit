---
name: peak-load-cover-planner
description: Forecast customer-service message volume per day from the week before Black Friday to mid-January, from last year's daily counts, last year's BFCM-week average, or a new store's normal weeks and expected sales lift. Carry unanswered work over to the next day, draft a named roster that fills short days from the people who say they can take extra days, flag anyone working too many days in a row, list the days that still need extra help and the hours of the day nobody covers, and estimate the helpdesk bill including a separate AI resolution meter. Use when a Shopify merchant asks how many support messages to expect over BFCM or the holidays, whether their team (even a solo owner) can keep up, who should work which days, whether to hire seasonal help, or what their helpdesk will cost over the plan cap.
license: MIT
compatibility: Runs the bundled Python script with the standard library only, no network access and no dependencies. Falls back to guided manual arithmetic if scripts cannot run in the environment.
metadata:
  version: "0.2"
---

# Peak load and cover planner

Most support teams plan for Black Friday weekend and then stop. The season does not stop there. December brings "where is my order" questions right up to the holiday, and the returns wave comes after it: in the US the top return day is 26 December (Loop Returns data, see `references/phase-calendar.md`). Weekends stay busy, and work not done on Sunday is still there on Monday. This skill turns the merchant's own numbers into a day-by-day forecast, a draft roster with names on it, and a bill estimate, so the gaps show up on paper in October instead of in the inbox in December.

## The rule that governs everything here

**Every number in the plan is either something the merchant told you or an estimate the merchant chose. Never a number you picked.**

That includes sales uplift, tickets per order, weekend level, hourly pattern and helpdesk prices. If the merchant does not know a figure, show them what it could be and where that comes from, and make them choose. A silently chosen industry figure looks exactly like a fact once it is inside a table.

Label every assumption as **merchant-stated** (from their own data) or **merchant-chosen estimate** (picked because they did not know). The script refuses any other label. If an input is still open, mark it `[DECISION NEEDED: <the question>]` and do not run the forecast around it.

## Ask one question at a time

Ask in this order and wait for each answer. The no-code prompt version of this tool asks the same questions in the same order.

1. **Dates.** Black Friday, Cyber Monday, the main holiday they plan around, and the end date (usually mid-January). For 2026: Black Friday Friday 27 November, Cyber Monday 30 November, Christmas Friday 25 December.
2. **What history they have.** Pick the first route that fits:
   - **A. Last year's daily counts** (conversations or tickets per day, from the helpdesk export) from a week before last Black Friday to mid-January. Best. Ask for the file or the list, and last year's Black Friday (28 November 2025 in the US).
   - **B. Only last year's BFCM-week total or average.** Or orders per day that week plus their own tickets per 100 orders from a normal month. If they have no ratio, show them this and make them pick:
     > Gorgias platform data from March 2026 ranges from 19 tickets per 100 orders (toys and games) to 46 (electronics, vehicles and parts) (https://www.gorgias.com/blog/ticket-volume). A helpdesk vendor has a reason to publish higher numbers, and your store may sit outside the range. Which number do you want to plan with?
   - **C. New store, no last year.** Their last four normal weeks: messages per week, or orders per week and messages per 100 orders.
3. **Growth** (routes A and B). Expected change on last year, in percent.
4. **Shape** (routes B and C).
   - Route B: how busy an average day in the week before the sale, December up to the holiday, and the returns weeks is, compared with an average BFCM-week day. See `references/phase-calendar.md`.
   - Route C: how many times a normal day they expect in each phase (pre-sale, BFCM week, December, returns). This is their sales plan, not yours. If they have no number, ask for their expected BFCM-week order lift in plain words, then offer scenarios with every day's forecast times 1.5 and 2, labelled as scenarios.
5. **Weekend level** (routes B and C). An average weekend day divided by an average weekday, averaged separately. Offer the one data point in `references/phase-calendar.md` (Chatty data: shopping questions 89, order questions 61, per 100 on weekdays). Their choice.
6. **Single days they expect to spike** that are not already in their data, such as a second launch. Optional.
7. **Minutes per conversation**, from their helpdesk (average handle time) or their own estimate.
8. **The team, one person at a time:** name, weekday shift, weekend shift (or none), days off, start and end dates for seasonal hires, and for the draft roster: which weekdays they could take an extra shift, the shift times for an added day, and their weekly hour limit.
9. **Longest run of working days** they allow. If they have no rule, the plan uses six and says so.
10. **Share of a shift spent actually answering customers**, as a percent.
11. **Hourly pattern** (optional). The share of a day's messages that arrives in each hour, from their helpdesk's busiest-hours report. Without it, the plan lists uncovered hours but cannot count the messages in them. Do not make one up.
12. **Helpdesk plan:** price per month, what it counts (tickets, conversations), how many are included, the overage price and block, and volume they expect outside the window for part-months. Then: does the plan bill AI-resolved conversations on a separate meter? If yes, the AI price, included resolutions, overage price per resolution, the share they expect AI to resolve, and whether a resolved conversation is also charged as a ticket. (On Gorgias it is: "You are charged both a ticket fee + automation fee if AI Agent responds to a ticket and does not hand over the conversation to a human agent", https://docs.gorgias.com/en-US/how-youre-billed-for-using-gorgias-199385.) Prices come from their plan page or invoice, never from you.

Before running, show every input in one table with its label and ask them to confirm. If a person has no shifts and no extra days, or the helpdesk unit does not match what the forecast counts, stop and ask.

## Run the plan

Assemble the JSON described in `references/input-schema.md` and run:

```
python3 scripts/plan.py <input.json> --markdown
```

Use the JSON output (without `--markdown`) to process the result further. The script returns the assumptions, one row per day (forecast, hours needed, who is on shift and whether the draft added them, hours available, gap, work carried in and left at the end of the day, uncovered hours, and messages in hours nobody covers), a phase summary, the draft roster before and after, a per person view with run flags, the days that still need extra help, the bill per month, and the scenario table.

### Manual fallback

If scripts cannot run, do the same arithmetic by hand and show every step. Write one row per day; fill the Day column by stepping one day at a time from a known anchor (27 November 2026 is a Friday; 25 December 2026 is a Friday) and check it against that anchor.

1. **Forecast.**
   - Route A: for days before the day before the holiday, last year's day at the same distance from Black Friday (same weekday; 27 Nov 2026 takes 28 Nov 2025, that is 364 days earlier); from the day before the holiday on, the same date last year. Multiply by (1 + growth / 100).
   - Routes B and C: phase average = BFCM level x phase factor (route B, level = last year's average day x (1 + growth / 100)), or normal day x phase uplift (route C). Weekday level = phase average x days in phase / (weekdays + weekend factor x weekend days); weekend level = weekday level x weekend factor.
   - Times any single-day multiplier. Round half up.
2. **Hours needed** = forecast x minutes / 60, one decimal.
3. **Hours available** = shift hours of everyone working x share answering / 100, one decimal.
4. **Carried in** = yesterday's "left at end of day" (0 on the first day). **Left at end of day** = hours needed + carried in - hours available, if positive.
5. **Draft roster:** follow the fill rule in `references/roster-template.md`.
6. **Runs:** count each person's consecutive working days; flag runs over the limit.
7. **Bill for a month** = plan price + (units over the cap / block size, rounded up) x block price + AI meter (AI price + resolutions over its cap x price per resolution, where resolutions = volume x AI share / 100, rounded half up). If AI resolutions are not also tickets, take them out of the ticket volume first. If the window covers only part of a month and the merchant gave no volume for the rest, say the bill is a lower bound.

## Report

In this order:

1. **Assumptions table**, merchant-chosen estimates first.
2. **Days that need extra help**, most hours first, after the draft. This is the list of work to do.
3. **Roster** in the layout in `references/roster-template.md`: one row per day, names on shift with added shifts marked, hours, gap, backlog. Weekends shown.
4. **Before and after the draft**, and the per person view with every `[DECISION NEEDED]` run flag.
5. **Uncovered hours of the day**, and with an hourly share the messages that arrive in them. List them and stop. Who or what answers after hours is not part of this skill; the kit's Peak Season Readiness Audit covers it.
6. **Helpdesk bill per month**, with the lower-bound note where it applies.
7. **Scenarios**, when the volume level is a merchant-chosen estimate, labelled as what-ifs.
8. **The three ways to close what is left**, stated plainly so the merchant chooses: move or extend shifts, add a person (with the dates they are needed), or reduce volume through clearer policy and delivery pages before the sale. Do not choose for them.

End with the open `[DECISION NEEDED]` items, if any.

## What this does not do

It does not compare helpdesk vendors or plans, and it does not recommend switching. It does not decide who covers after hours. It does not predict sales; the uplift is the merchant's. It does not read the merchant's helpdesk; every number comes from them. It does not move a regular shift, cancel a day off or add a person the merchant did not name; the draft only uses extra days people offered. Hours needed assume a person handles every forecast message; if the merchant expects an AI to resolve a share, they can lower the forecast themselves and say so in the assumptions.
