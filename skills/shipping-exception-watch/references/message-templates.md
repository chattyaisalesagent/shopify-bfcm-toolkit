# Proactive messages, one per group

The point of this skill is that the shopper hears about the problem from the store before they have to ask. These drafts follow the same wording and rules as the delivery templates in `delivery-cutoff-planner` (its "running late" and "will not arrive" messages), adapted for an order that has already shipped and is visibly off track. They are repeated here so this skill works on its own.

Rules for every draft:

- **Fill brackets only from the script output or from what the merchant confirmed.** Leave anything else as a marked bracket.
- **The carrier status is quoted from the file, never written from imagination.** If the file says `In transit` and a last update of 2 December, the message says exactly that. If the file has no status detail, say "the carrier's tracking has not updated since **[date]**" or leave the bracket.
- **No new delivery date the merchant cannot back up.** "We don't have a reliable new estimate yet" is an acceptable sentence when it is true.
- **Every offer is the merchant's decision.** Refunds, gift cards, discount codes, reshipping, paying duties: each one stays `[DECISION NEEDED: ...]` until the merchant confirms it, and an unconfirmed offer must not appear in a message that goes out under the store's name.
- **No names from the file.** Every greeting uses `[first name]`, which the merchant's email or helpdesk tool fills in. The skill never reads names.
- **Nothing for on-track orders.** Shopify's customer notifications already cover shipping confirmation, shipping updates, out for delivery and delivered. These drafts are only for the cases Shopify has no notification for.
- **Drafts only.** The merchant reviews and sends them from their own email or helpdesk tool.

---

## 1. `past_promised_date`: late, not yet delivered

Use for every order in the group. If `days_late` is large or the order was a gift for a fixed date, the merchant may prefer the stronger version below.

> Hi **[first name]**, we're sorry: your order **[order number]** hasn't arrived by **[promised date]**, the date we gave you.
>
> It left us on **[ship date]**, **[with {carrier}, if the file has it]**. The latest update we have from the carrier shows **[status as written in the file]**, **[on last update date, if the file has one]**. Track it here: **[tracking link]**.
>
> **[New estimate if the merchant has one, or: "We don't have a reliable new estimate yet, and we're checking with the carrier now."]**
>
> **[DECISION NEEDED: what the store offers for the delay, e.g. a partial refund, a discount code, free return shipping if it arrives too late to be useful. Delete this line if nothing is offered.]**
>
> We'll write again as soon as it moves. Questions? **[how to reach a person]**.

**Stronger version, when it will clearly miss the date that mattered** (a holiday, an event):

> Hi **[first name]**, we're very sorry. Your order **[order number]** will not arrive by **[promised date]**.
>
> Current status from **[carrier]**: **[status as written in the file]**, last updated **[last update date]**.
>
> Here are your options:
> - **[DECISION NEEDED: keep the order, arriving when it can, and what if anything the store offers for that]**
> - **[DECISION NEEDED: cancel for a full refund, if offered]**
> - **[DECISION NEEDED: if it was a gift, any alternative in the meantime, e.g. a digital gift card]**
>
> To choose, **[how to respond]**.

If the order is also flagged `customs_hold`, add the customs paragraph from template 2.

---

## 2. `customs_hold`: held at customs

> Hi **[first name]**, a quick update on order **[order number]**. It's currently with customs in **[destination country]**. The carrier shows: **[status or tracking detail as written in the file]**.
>
> **[Only if the merchant confirms what is needed: "To release it, customs needs {document / duty payment}. {What the shopper should do, or what the store is doing}."]**
>
> **[DECISION NEEDED: who pays any duties or fees. Only include if the store's policy says so or the merchant decides now.]**
>
> Customs timing is outside our and the carrier's control, so we can't promise a date yet. We'll update you as soon as it's released. Track it here: **[tracking link]**.

Do not tell the shopper they owe duties, or that the store will pay them, unless the merchant has confirmed which. Check the matched keywords in the output first: a carrier event that only mentions customs in passing is not a hold.

---

## 3. `delivery_problem`: failed, attempted or delayed delivery

The order is not late yet, but the carrier reports a problem: a failed or attempted delivery, a delay, or an exception. Shopify sends no notification for these, so the shopper often sees the card through the door or the tracking page before hearing from the store.

> Hi **[first name]**, a quick heads-up on order **[order number]**. **[Carrier, if the file has it]** reports: **[status as written in the file]**.
>
> **[If the status is a failed or attempted delivery: "It looks like the carrier couldn't complete the delivery. Their notice or the tracking link below should say how to rearrange delivery or collect the parcel."]**
> **[If the status is delayed: "The carrier has marked it as delayed. It's still due by {promised date}, and we're watching it."]**
>
> Track it here: **[tracking link]**. If the parcel is sent back to us, we'll **[DECISION NEEDED: next step, e.g. reship at no cost, refund]**.
>
> Questions? **[how to reach a person]**.

Do not invent the carrier's pickup address, how long it holds the parcel, or how many attempts it makes; that differs by carrier and is not in the file. Only say "we've contacted the carrier" if the merchant has.

---

## 4. `tracking_stalled`: no update for a while

The order is not late yet. The goal is to reach the shopper before they notice the tracking page has not changed.

> Hi **[first name]**, we've noticed the tracking for your order **[order number]** hasn't updated since **[last update date]**. That can happen during busy weeks when parcels move between depots without a scan.
>
> It's still due by **[promised date]**, and we're keeping an eye on it. If there's no movement by **[date the merchant chooses]**, we'll **[DECISION NEEDED: what the store will do, e.g. open a trace with the carrier, reship]** and let you know.
>
> Track it here: **[tracking link]**. Questions? **[how to reach a person]**.

Only say "we've opened a trace with the carrier" if the merchant has actually done it.

---

## 5. `delivered_but_contacted`: marked delivered, shopper says it didn't arrive

The shopper has already written in, so this is a reply, sent in the same thread.

> Hi **[first name]**, thanks for letting us know, and sorry for the worry. **[Carrier]** marked order **[order number]** as delivered **[on {date}, if the file has one]**.
>
> Could you check a few places for us: with neighbours, around the door or a side entrance, a mailbox or parcel locker, and with anyone else at the address who may have taken it in?
>
> If it hasn't turned up by **[date, e.g. two days from now]**, reply here and we'll **[DECISION NEEDED: next step, e.g. open a claim with the carrier, reship, refund]**.

Do not suggest the shopper is mistaken, and do not promise a reship or refund in the first reply unless the merchant has decided to.

---

## `check_tracking`: no draft until the tracking page confirms it

These orders are candidates from Shopify-only data: possibly stalled, possibly never scanned, possibly held at customs. None is confirmed, so none gets a message yet. Show the merchant each order with its `check_reasons`, tell them to open the order in Shopify admin and click the tracking number, then:

- tracking says customs, clearance, duties or documents: use template 2, Held at customs;
- tracking has not moved for several days: use template 4, Tracking stalled, with the last scan date from the tracking page;
- tracking says failed, attempted or exception: use template 3, Delivery problem;
- tracking shows recent scans: no message.

For a `past_promised_date` or `delivery_problem` order flagged `possible_customs_hold`, the same check decides whether to add the customs paragraph or use template 2.

## `contacted_but_on_track`

The shopper asked, but the file shows nothing wrong. Reply with the facts the file holds: status as written, last update date, promised date, tracking link. No offer is needed.

## Sending order

Work down `urgency_rank`. Past-due orders first: those shoppers are the most likely to write in, dispute the charge, or leave a review about it next.
