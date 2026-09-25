# The three delivery templates

For carrier shipments, Shopify's built-in customer notifications are Shipping confirmation (sent when the order is fulfilled), Shipping update (when tracking information is updated), Out for delivery and Delivered, the last two triggered by carrier tracking events. **None of them tells the shopper a parcel is late or will miss the date.** Local delivery works differently: Out for delivery and Delivered do not apply, a delivery confirmation email goes out when the merchant marks the order delivered, and Shopify has listed a "Local order missed delivery" notification for a failed local drop-off. That still does not cover a carrier parcel running late. These three templates fill that gap. Checked against help.shopify.com/en/manual/fulfillment/setup/notifications/customer-notifications and help.shopify.com/en/manual/fulfillment/fulfilling-orders/local-delivery-fulfillment on 24 September 2026.

Fill every bracket from what the merchant has told you or from the script's output. Leave a bracket unfilled, marked, rather than guessing.

---

## 1. Dispatched, on track

Sent when the order ships within the normal window, ahead of or on the computed cutoff.

> Your order is on its way. We expect it to arrive by **[target arrival date]**. Track it here: **[tracking link]**.
> If anything changes, we'll email you.

Nothing unusual here; it exists mainly so the merchant has all three in one place and does not have to write this one from scratch under pressure while the other two are more urgent.

---

## 2. Running late, still expected before the target date range

Sent when a shipment has slipped past its normal transit estimate but the merchant's system still expects it before the promise breaks entirely. This is the hardest of the three to get the tone right on: honest about the delay, specific about what happens next, without promising a date nobody can back up.

> We're sorry, your order is running behind schedule. It left our warehouse on **[dispatch date]** and the carrier's latest update shows **[carrier status, e.g. "in transit, last scanned in {city} on {date}"]**.
>
> Based on this, we now expect it **[new estimated date, or "within the next X days" if no better estimate exists]**. This is later than the **[original target arrival date]** we originally promised, and we're sorry for that.
>
> **[If applicable: what the merchant is doing about it, e.g. a partial refund, a discount code, free return shipping if the order arrives too late to be useful.]**
>
> Questions? **[how to reach a person]**.

Do not fill the new estimated date with a guess. If the merchant has no better information than the carrier's last scan, say so honestly rather than inventing a number that sounds more confident than the situation supports.

---

## 3. Will not arrive before the target date

Sent once it is clear the order will miss the holiday or the promised date entirely. The most important of the three, and the one merchants are least likely to have written in advance, precisely because nobody wants to send it.

> We're very sorry. Your order will not arrive by **[original target date]**.
>
> Current status: **[carrier status]**. Our best estimate now is **[new date, or "we don't have a reliable new estimate yet" if true]**.
>
> Here are your options:
> - **[Keep the order, arriving when it can. State what, if anything, the merchant is offering: a partial refund, a gift card, free shipping on their next order.]**
> - **[Cancel for a full refund, if the merchant is offering this.]**
> - **[If this was a gift: any expedited alternative the merchant can offer, e.g. a digital gift card to send in the meantime.]**
>
> To choose, **[how to respond]**. We're sorry this order won't be there when you needed it.

This is the message that protects the relationship when the promise already failed. A merchant who has never written it in advance writes something worse on the day, under pressure, with no options prepared. Ask the merchant, while there is still time, which of the options above they are actually willing to offer, and do not put an option in the template the merchant has not confirmed.

---

## Using these with the cutoff table

Pair each zone's `feasible: false` result from the script with template 3 rather than template 2: if the cutoff itself has already passed for a zone, the merchant is not looking at a delay, they are looking at a promise they cannot keep for anyone ordering into that zone today, and the message to prepare is the one that offers options, not the one that asks for patience.
