---
name: peak-load-cover-planner
description: Forecast customer-service message volume per day from the week before Black Friday to mid-January, build a named staff roster that includes weekends and the returns weeks after the holiday, show which days the team is short of hours and which hours of the day nobody covers, and estimate the helpdesk bill when volume goes over the plan cap. Use when a Shopify merchant asks how many support messages to expect over BFCM or the holidays, whether their team can keep up, who should work which days, whether to hire seasonal help, or what their helpdesk will cost if they exceed their ticket or conversation limit.
license: MIT
compatibility: Runs the bundled Python script with the standard library only, no network access and no dependencies. Falls back to guided manual arithmetic if scripts cannot run in the environment.
metadata:
  version: "0.1"
---

# Peak load and cover planner

Most support teams plan for Black Friday weekend and then stop. The season does not stop there. December brings "where is my order" questions right up to the holiday, and the returns wave comes after it: in the US it peaks around 26 December (Loop Returns data across Shopify merchants). Weekends stay busy throughout. This skill turns the merchant's own numbers into a day-by-day forecast, a roster with names on it, and a bill estimate, so the gaps show up on paper in October instead of in the inbox in December.

## The rule that governs everything here

**Every number in the plan is either something the merchant told you or an estimate the merchant chose. Never a number you picked.**

The forecast is only as honest as its weakest input, and the weakest input is usually the tickets-per-order ratio or the phase shape. If the merchant does not know a figure, show them the range of what it could be, where that range comes from, and make them choose. A silently chosen industry figure looks exactly like a fact once it is inside a table, and a plan built on it staffs the wrong days.

Label every assumption in the output as **merchant-stated** (they know it from their own data) or **merchant-chosen estimate** (they picked it because they did not know). The script refuses any other label. If an input is still open, mark it `[DECISION NEEDED: <the question>]` and do not run the forecast around it.

## Ask one question at a time

Ask in this order and wait for each answer. Merchants answer a list of ten questions with three answers.

1. **Last year's BFCM-week volume.** Conversations or tickets per day across Black Friday to the Thursday after Cyber Monday. Their helpdesk reports have it.
2. **If they do not have that:** orders per day in the same week, plus their own tickets-per-order ratio from any normal month (tickets divided by orders). If they have no ratio either, show them this and make them pick a number:

   > Published figures from one helpdesk vendor range from roughly 19 to 46 tickets per 100 orders depending on industry (source: Gorgias, https://www.gorgias.com/blog/ticket-volume). A helpdesk vendor has a reason to publish higher numbers, and your store may sit outside the range. Which number do you want to plan with?

   Record their answer as a merchant-chosen estimate. Do not pick the midpoint for them.
3. **Expected growth this year**, in percent. Planned ad spend, email list size and last year's sale depth are all reasonable ways for them to reason about it. Their number, not yours.
4. **Phase shape.** Compared with a BFCM-week day, how busy is a day in the week before the sale, a December day, and a day in the returns weeks after the holiday? Read `references/phase-calendar.md` and walk them through it. If they have last year's daily export, derive the factors from it and label them merchant-stated.
5. **Weekend level.** A Saturday or Sunday as a fraction of a weekday. See the data point in `references/phase-calendar.md`; again, their choice.
6. **Any single days they expect to spike**, such as 26 December or the day a second promotion launches. Optional.
7. **Time per conversation**, in minutes, from their helpdesk (average handle time) or their own estimate. Remind them BFCM conversations are often shorter than returns conversations; if they think the difference matters, run the plan twice.
8. **The team, one person at a time:** name, weekday shift, weekend shift (or none), days off in the window, and start and end dates for seasonal hires.
9. **Share of a shift spent actually answering customers**, as a percent. Breaks, meetings, packing and admin come out of it. Their number.
10. **Helpdesk plan:** price per month, how many tickets or conversations are included, the overage price and the block it is charged in (per ticket, per 100), what the unit is (ticket, conversation, resolution), and, for months the window only partly covers, the volume they expect on the days outside it.

Check the input before running. If a person has no shifts at all, or the helpdesk billing unit does not match what the forecast counts (tickets versus conversations), stop and ask.

## Run the plan

Assemble the JSON described in `references/input-schema.md` and run:

```
python3 scripts/plan.py <input.json> --markdown
```

Use the JSON output (without `--markdown`) if you need to process the result further.

The script returns: the assumption table with each label, one row per day (forecast, hours needed, hours available, gap, who is on shift, which hours of the day nobody covers), a summary per phase, the list of gap days, and the bill per calendar month.

### Manual fallback

If scripts cannot run in this environment, do the same arithmetic by hand and show every step so the merchant can check it:

1. **Level** = last year's per-day volume (or orders per day x tickets per 100 orders / 100) x (1 + growth / 100).
2. **Forecast for a day** = level x phase factor (BFCM week is 1.0) x weekend factor on Saturdays and Sundays x any single-day multiplier. Round half up to a whole conversation.
3. **Hours needed** = forecast x minutes per conversation / 60, to one decimal.
4. **Hours available** = sum of shift lengths of everyone working that day x share answering / 100, to one decimal. Skip people on a day off or outside their start and end dates.
5. **Gap** = hours needed minus hours available, when positive.
6. **Bill for a month** = plan price + (blocks over the cap, rounded up) x price per block. If the window covers only part of a month and the merchant gave no volume for the rest, say the bill is a lower bound.

Phases: the week before Black Friday is pre-sale; Black Friday to the Thursday after Cyber Monday is BFCM week; the day after that to the day before the holiday is December; the holiday to the end date is returns. Write the full daily table; do not summarise a phase as "similar every day", because weekends and days off change it.

## Report

In this order:

1. **Assumptions table**, every row labelled. Put merchant-chosen estimates first; they are the ones to revisit.
2. **Gap days**, sorted by gap hours, largest first. This is the list of work to do.
3. **Roster** in the layout in `references/roster-template.md`: one row per day, names on shift, hours, gap. Weekends are shown, not folded in.
4. **Uncovered hours of the day.** List them as the script prints them (for example "00:00 to 09:00, 20:00 to 24:00"). Say that these hours are not covered by anyone on the roster and stop there. Deciding who or what answers after hours is not part of this skill; the kit's Peak Season Readiness Audit covers it.
5. **Helpdesk bill per month**, with the lower-bound note where it applies.
6. **The three ways to close a gap**, stated plainly so the merchant chooses: move or extend shifts, add a person (with the dates they are needed), or reduce volume through clearer policy and delivery pages before the sale. Do not choose for them.

End with the open `[DECISION NEEDED]` items, if any.

## What this does not do

It does not compare helpdesk vendors or plans, and it does not recommend switching. If the merchant asks which helpdesk is cheaper, say that is outside this plan and use only the prices they gave you. It does not decide who covers after hours. It does not predict sales. It does not read the merchant's helpdesk; every number comes from them.
