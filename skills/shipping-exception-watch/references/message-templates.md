# Proactive messages, one per group

The point of this skill is that the shopper hears about the problem from the store before they have to ask. These drafts follow the same wording and rules as the delivery templates in `delivery-cutoff-planner` (its "running late" and "will not arrive" messages), adapted for an order that has already shipped and is visibly off track. They are repeated here so this skill works on its own.

Rules for every draft:

- **Fill brackets only from the script output or from what the merchant confirmed.** Leave anything else as a marked bracket.
- **The carrier status is quoted from the file, never written from imagination.** If the file says `In transit` and a last update of 2 December, the message says exactly that. If the file has no status detail, say "the carrier's tracking has not updated since **[date]**" or leave the bracket.
- **No new delivery date the merchant cannot back up.** "We don't have a reliable new estimate yet" is an acceptable sentence when it is true.
- **Every offer is the merchant's decision.** Refunds, gift cards, discount codes, reshipping, paying duties: each one stays `[DECISION NEEDED: ...]` until the merchant confirms it, and an unconfirmed offer must not appear in a message that goes out under the store's name.
- **Drafts only.** The merchant reviews and sends them from their own email or helpdesk tool.

---

## 1. `past_promised_date`: late, not yet delivered

Use for every order in the group. If `days_late` is large or the order was a gift for a fixed date, the merchant may prefer the stronger version below.

> Hi **[first name]**, we're sorry: your order **[order number]** hasn't arrived by **[promised date]**, the date we gave you.
>
> It left us on **[ship date]** with **[carrier]**. The latest update we have from the carrier shows **[status as written in the file]** on **[last update date]**. Track it here: **[tracking link]**.
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

> Hi **[first name]**, a quick update on order **[order number]**. It's currently with customs in **[destination country]**. The carrier shows: **[status or note as written in the file]**.
>
> **[Only if the merchant confirms what is needed: "To release it, customs needs {document / duty payment}. {What the shopper should do, or what the store is doing}."]**
>
> **[DECISION NEEDED: who pays any duties or fees. Only include if the store's policy says so or the merchant decides now.]**
>
> Customs timing is outside our and the carrier's control, so we can't promise a date yet. We'll update you as soon as it's released. Track it here: **[tracking link]**.

Do not tell the shopper they owe duties, or that the store will pay them, unless the merchant has confirmed which. Check the matched keywords in the output first: a note that only mentions customs in passing is not a hold.

---

## 3. `tracking_stalled`: no update for a while

The order is not late yet. The goal is to reach the shopper before they notice the tracking page has not changed.

> Hi **[first name]**, we've noticed the tracking for your order **[order number]** hasn't updated since **[last update date]**. That can happen during busy weeks when parcels move between depots without a scan.
>
> It's still due by **[promised date]**, and we're keeping an eye on it. If there's no movement by **[date the merchant chooses]**, we'll **[DECISION NEEDED: what the store will do, e.g. open a trace with the carrier, reship]** and let you know.
>
> Track it here: **[tracking link]**. Questions? **[how to reach a person]**.

Only say "we've opened a trace with the carrier" if the merchant has actually done it.

---

## 4. `delivered_but_contacted`: marked delivered, shopper says it didn't arrive

The shopper has already written in, so this is a reply, sent in the same thread.

> Hi **[first name]**, thanks for letting us know, and sorry for the worry. **[Carrier]** marked order **[order number]** as delivered on **[last update date]**.
>
> Could you check a few places for us: with neighbours, around the door or a side entrance, a mailbox or parcel locker, and with anyone else at the address who may have taken it in?
>
> If it hasn't turned up by **[date, e.g. two days from now]**, reply here and we'll **[DECISION NEEDED: next step, e.g. open a claim with the carrier, reship, refund]**.

Do not suggest the shopper is mistaken, and do not promise a reship or refund in the first reply unless the merchant has decided to.

---

## `contacted_but_on_track`

The shopper asked, but the file shows nothing wrong. Reply with the facts the file holds: status as written, last update date, promised date, tracking link. No offer is needed.

## Sending order

Work down `urgency_rank`. Past-due orders first: those shoppers are the most likely to write in, dispute the charge, or leave a review about it next.
