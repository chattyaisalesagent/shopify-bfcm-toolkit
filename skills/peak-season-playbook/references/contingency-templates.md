# Contingency plan templates

Four scenarios. Each plan must be decided before it is needed: the day a carrier is two days behind is not the day to decide what a late order earns. Every offer to shoppers must already be allowed by the authority table. Every trigger and offer comes from the merchant; if they have no answer, offer 2 or 3 labelled examples to pick from, and if they still do not decide, mark it.

Use the same headings for each: trigger, owner, first 3 actions, what shoppers are told, when to stop, log. Assign each action to a role the team actually has; for a solo founder most actions are the owner's.

---

## 1. Carrier delay

**Trigger.** [e.g. carrier announces delays in a region, or more than [n] orders show no tracking update for [n] days. Examples to pick from: 5 orders / 10 orders; 2 days / 3 days.]

**Owner.** [role]

**First 3 actions.**
1. List affected orders and regions.
2. Send the "running late" message (from delivery-cutoff-planner) to those orders before shoppers write in.
3. Update the shipping banner and cutoff dates if the carrier's new times move them. Decide whether to switch affected regions to another service.

**What shoppers are told.** The merchant's saved "running late" and "will not arrive in time" messages. Offer only: [compensation from the authority table, or DECISION NEEDED].

**Stop when.** The carrier confirms normal service and no affected order is still undelivered.

**Log.** Orders contacted, offers made, total cost.

---

## 2. Stock-out mid-sale

**Trigger.** [e.g. a promoted product sells out, or oversold orders appear because stock was wrong.]

**Before the sale.** Check which products have "Continue selling when out of stock" turned on, and if the store uses Shopify POS, remember it can sell below zero (it warns staff). Either can create orders you cannot fill.

**Owner.** [role]

**First 3 actions.**
1. Mark the product sold out and pull it from scheduled emails and banners.
2. List orders that cannot ship on time.
3. Contact those shoppers with the options below, before they notice.

**What shoppers are told.** Options the merchant allows, in their order of preference. A full refund is always one of them. [e.g. wait for restock by a confirmed date / swap to a similar item at the sale price / full refund.] Whether the sale price is honoured on a later restock: [DECISION NEEDED if not given]. Never give a restock date the merchant has not confirmed.

For US orders, the FTC Mail Order Rule requires that when you cannot ship in the time you promised (or within 30 days if you promised none), you tell the shopper and offer to cancel with a prompt refund.

**Stop when.** Every affected order has a chosen option and the product page is correct.

**Log.** Orders affected, option each shopper chose, total cost.

---

## 3. Volume above forecast

**Trigger.** [e.g. open conversations above [n], or first reply time above [n] hours, for more than [n] hours. Use the forecast from peak-load-cover-planner as the baseline if the merchant has one.]

**Owner.** [role]

**First 3 actions.**
1. Call in [named backup people], in this order: [list].
2. Sort the queue so these come first: [merchant's priority, e.g. orders not yet shipped, payment problems, anything on the always-owner list].
3. Post a realistic reply time in the auto-reply and on the contact page. Pause [e.g. a scheduled promotional email] if the merchant agreed that is an option.

**What shoppers are told.** A holding reply with a real reply time: "[merchant wording]". Do not promise a time the team cannot meet.

**Stop when.** The queue is back under [n] for [n] hours.

**Log.** Peak queue size, hours over trigger, who was called in.

---

## 4. Parcel held at customs (only if the store ships abroad)

**Trigger.** Tracking shows a parcel held by customs, or a shopper reports a duties or customs request.

**Owner.** [role]

**First 3 actions.**
1. Check tracking or the carrier for the reason: missing documents, duties or taxes unpaid, or inspection.
2. Tell the shopper what the carrier needs, using the store's duties wording from the brief (collected at checkout, or paid by the shopper on delivery).
3. If the store has to pay duties or send documents, send it to the owner the same day.

**What shoppers are told.** Why the parcel is held and what happens next. Offer only: [what the authority table allows, e.g. refund or reship if it is returned to sender, or DECISION NEEDED].

**Stop when.** The parcel is released, or it is returned to sender and handled under the authority table.

**Log.** Orders held, reason, days held, cost to the store.

---

## Checks

- Every role named in a plan exists in the team list.
- Every offer appears in the authority table for the role making it.
- Every trigger has a number the merchant chose, or is marked.
- The stock-out plan always includes a full refund option.

Sources, checked September 2026:
- Inventory tracking and POS: https://help.shopify.com/en/manual/products/inventory/getting-started-with-inventory/set-up-inventory-tracking
- FTC Mail Order Rule: https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule
- EU right of withdrawal: https://help.shopify.com/en/manual/compliance/legal/eu-right-of-withdrawal
- UK online returns: https://www.gov.uk/accepting-returns-and-giving-refunds
