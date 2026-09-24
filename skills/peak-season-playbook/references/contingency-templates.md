# Contingency plan templates

Three scenarios. Each plan must be decided before it is needed: the day a carrier is two days behind is not the day to decide what a late order earns. Every offer to shoppers must already be allowed by the authority table. Every trigger and offer comes from the merchant; if they have not decided, mark it.

Use the same five headings for each scenario.

---

## 1. Carrier delay

**Trigger to activate.** [e.g. carrier announces delays in a region, or more than [n] orders show no tracking update for [n] days. Merchant sets n.]

**Who does what.**
- [Role]: checks which orders and regions are affected and lists them.
- [Role]: sends the "running late" message (from delivery-cutoff-planner) to affected orders before shoppers write in.
- [Role]: updates the shipping banner and cutoff dates if the carrier's new times move them.
- [Role]: decides whether to switch affected regions to another carrier or service.

**What shoppers are told.** Use the merchant's saved "running late" and "will not arrive in time" messages. Offer only: [compensation from the authority table, or DECISION NEEDED].

**Stand down when.** [e.g. the carrier confirms normal service and no affected order is still undelivered.]

**Log.** Orders contacted, offers made, total cost, so the merchant can review after the season.

---

## 2. Stock-out mid-sale

**Trigger to activate.** [e.g. a promoted product sells out, or oversold orders appear because stock was wrong.]

**Who does what.**
- [Role]: hides or marks the product sold out, and removes it from banners and emails still scheduled.
- [Role]: lists orders that cannot be fulfilled.
- [Role]: contacts those shoppers with the options below, before they notice.
- [Role]: decides whether a restock date is real enough to offer a backorder.

**What shoppers are told.** Options the merchant allows, in their order of preference: [e.g. wait for restock by a confirmed date / swap to a similar item at the sale price / full refund]. Whether the sale price is honoured on a later restock: [DECISION NEEDED if not given]. Never give a restock date the merchant has not confirmed.

**Stand down when.** [e.g. every affected order has a chosen option and the product page is correct.]

**Log.** As above.

---

## 3. Volume above forecast

**Trigger to activate.** [e.g. open conversations above [n], or first response time above [n] hours, for more than [n] hours. Use the forecast from peak-load-cover-planner as the baseline if the merchant has one.]

**Who does what.**
- [Role]: calls in [named backup people], in this order: [list].
- [Role]: sorts the queue so these come first: [merchant's priority, e.g. orders not yet shipped, payment problems, anything on the always-escalate list].
- [Role]: posts a notice on the contact page and in the auto-reply with the realistic response time.
- [Role]: pauses [e.g. a scheduled promotional email] if the merchant has agreed that is an option.

**What shoppers are told.** A holding reply with a real response time: "[merchant wording]". Do not promise a time the team cannot meet.

**Stand down when.** [e.g. the queue is back under [n] for [n] hours.]

**Log.** Peak queue size, hours over trigger, who was called in.

---

## Checks

- Every role named in a plan exists in the team list.
- Every offer appears in the authority table for the role making it.
- Every trigger has a number the merchant chose, or is marked.
