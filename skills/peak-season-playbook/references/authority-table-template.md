# "Who may decide what" template

This table exists so that two agents on the same day give the same answer, and so a seasonal hire knows where their authority ends. Every amount comes from the merchant, in the merchant's currency. A blank is marked, not filled.

## Columns: only the roles the team has

One column per role the merchant named, owner last. Examples:

- Solo founder with one seasonal helper: `Decision | Seasonal helper | Owner`
- Small team: `Decision | Agent | Owner`
- Larger team: `Decision | Seasonal hire | Agent | Team lead | Owner`

Never add a column for a role the team does not have.

## Decision table

| Decision | [Role 1] | [Role 2] | Owner |
|---|---|---|---|
| Full refund within policy, after the item is back and checked | | | |
| Refund outside the returns window | | | |
| Partial refund for a problem (late, damaged, wrong item) | | | |
| Exchange for same item, different size or colour | | | |
| Exchange for a different item | | | |
| Compensation: discount code for next order | | | |
| Compensation: gift card | | | |
| Compensation: free shipping or free upgrade | | | |
| Honour an expired promotion code | | | |
| Cancel an unshipped order (nothing fulfilled yet) | | | |
| Refund and return a shipped order | | | |

"After the item is back and checked" means the parcel has arrived at the store and someone has looked at it. A shopper creating a return label is not enough.

Cell wording, always one of:
- "Yes, up to [amount]"
- "No, escalate to [role]"
- `[DECISION NEEDED: may a <role> <decision>, and up to how much?]`

Add a row for any other decision the merchant names. Delete a row only if the merchant says it never happens.

### Offering examples when the merchant has no limits

This happens in turn 2 of the conversation (see SKILL.md). Every blank cell for a role other than the owner is blocking, so each missing decision gets one numbered line under the heading "Examples, pick one or write your own", with options a), b), c), most cautious first and one value per role in each option. For instance:

- 1. Partial refund for a problem, VA: a) $0, escalate to owner b) up to $25 c) up to $50
- 2. Refund outside the window, VA: a) no, escalate to owner b) yes, up to $25
- 3. Discount code for next order, Agent / Lead: a) no / up to 10% b) up to 10% / up to 15%

The merchant answers all lines in one reply ("1b, 2a, 3: 15% / 20%", or "all a"). Use the merchant's currency. Only values the merchant picks or types go into the final table; the owner's column is "Yes".

## Limits per shopper

- Maximum total compensation to one shopper for one order, any role: [amount or DECISION NEEDED]
- Compensation types that may not be combined: [merchant's list or DECISION NEEDED]

## Always goes to the owner, whatever the amount

Fixed, always on the list:
- Any chargeback or payment dispute. Nobody refunds, or gives a gift card or discount, on that order. Shopify does not allow a refund while a chargeback is open.

Ask the merchant for the rest. You may name these as examples, clearly as examples; the final list is theirs:
- a shopper mentioning a lawyer, the press or a regulator
- a safety or allergy issue with a product
- the same shopper asking for compensation a second time

## How to escalate

- Channel: [helpdesk note, chat group, phone]
- What to include: order number, what the shopper asked for, what you already offered.
- What to tell the shopper while waiting: "[merchant wording]"
- Response time the owner commits to: [DECISION NEEDED if not given]

## Shopify facts for the team

Put these under the table in plain words.

- **Cancelling.** Only an order with nothing fulfilled yet can be cancelled. Once anything is fulfilled, refund and return instead. If an order was already refunded, cancel it on its own (not in bulk) and choose to refund Later, so it is not refunded twice.
- **Refund limits are a written rule.** Shopify's refund permissions ("Refund to original payment method", "Refund to store credit") are on or off, with no amount cap. If a role may not refund at all, turn those permissions off for that person.
- **Daily refund check.** The lead (or the owner, if there is no lead) opens Orders, filters Payment status is Refunded or Partially refunded, saves it as a view, and compares each refund with this table.
- **Chargebacks.** Refunds can't be issued while a chargeback is open. Send it to the owner.

Sources, checked September 2026:
- Cancelling: https://help.shopify.com/en/manual/fulfillment/managing-orders/canceling-orders
- Staff refund permissions: https://help.shopify.com/en/manual/your-account/users/roles/permissions/store-permissions
- Order filters: https://help.shopify.com/en/manual/fulfillment/managing-orders/viewing-orders/filtering-orders
- Refunds during a chargeback: https://help.shopify.com/en/manual/payments/chargebacks/resolve-chargeback
