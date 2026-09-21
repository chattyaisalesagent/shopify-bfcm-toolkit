# What the platform can and cannot enforce

Verified against Shopify's own documentation, checked 21 September 2026. Each entry says what the merchant should be told, because several of these are things a merchant reasonably assumes work and which do not.

Re-verify before relying on any of it in a new season. Platform behaviour moves.

---

## Returns

### A seasonal returns window is not expressible as a rule

Shopify return rules offer a **number of days from delivery**, or from the last item delivered: 14, 30, 90, unlimited, or a custom number of days. There is no purchase-date-range trigger and no fixed calendar end date.

So a promise of the shape *"anything bought between 1 November and 24 December can be returned until 31 January"* **cannot be configured**. It can be published as policy, and it can be honoured, but the store will not enforce it. Every return under that promise arrives as a manual exception for whoever handles returns.

Tell the merchant: the policy is publishable, the rule is not, and somebody has to carry the difference by hand. Ask who, and roughly how many orders that is.

### Return rule changes are not retroactive

A change to a return rule **applies only to future orders**. A merchant who extends the window in December has not extended anything for the orders already placed in November.

This has a scheduling consequence worth stating whenever a holiday extension comes up: if the extended window is meant to cover orders from 1 November, the rule has to be in place **before** 1 November. Deciding it in December is already too late for the orders it was meant to protect.

### Self-serve returns exclude exchanges, guests and gift recipients

Self-serve returns run from the online store and the Shop app, and they require the customer to be **signed in**. Exchanges **cannot be requested through self-serve** at all, and there are no exchange-specific return rules.

So the two groups most likely to need help after a holiday, a guest who checked out without an account and a person who received a gift, cannot start a return themselves. Whatever the policy promises them has to be delivered by a person. If the policy mentions gifts or exchanges, say who handles them and how the recipient makes contact.

### Final sale is set by product or collection

Final-sale status lives in the return rules, assigned by product or by collection. It is not a property of a discount. Marking a collection final sale and then running a sitewide code produces exactly the contradiction described in the skill: the discount applies everywhere, the returns promise does not.

---

## Discounts

### The free-shipping threshold is measured after the discount

When a free-shipping discount combines with an order or product discount, Shopify evaluates the threshold against the **discounted** cart value.

A $90 cart with 25% off becomes $67.50 and therefore does **not** clear a $75 threshold. Shoppers read the pre-discount number and expect the opposite, which is why this surfaces as a complaint in exactly the week nobody has time for it.

The merchant has two levers: lower the threshold for the sale period, or state the rule explicitly in the terms. Either is fine. Leaving the sentence as "free shipping on orders over $75" is not, because it does not say which $75.

### Active dates resolve in the store's admin timezone

A discount's start and end times are interpreted in the **store's admin timezone**, which no shopper can see and most will assume is their own.

An end date written as a bare date is therefore ambiguous twice over: it does not say whether the sale ends at the start or the end of that day, and it does not say whose day. Terms should carry a time and a named timezone.

### Codes have a combination limit

At most **five product or order discount codes plus one shipping discount code** can apply to a single order. Combination behaviour is set per discount class, product, order and shipping, through the combines-with settings.

### Checkout never explains a failure

When codes conflict, the shopper sees only **"Some discount codes couldn't be used together."** It does not say which pair conflicted, why, or which combination would have worked.

That message is the entire shopper-facing explanation the platform provides, which is the practical reason the stacking rule has to be written somewhere a shopper can read before they reach checkout.

---

## Where the text lives

Shopify's policy generator provides **six** templates: return, privacy, terms of service, shipping, legal notice, subscription. **There is no sale-terms or discount-terms page type.**

So the terms produced here have no native home. The merchant has to choose one: a dedicated page linked from the sale banner, a section on the offer page, or an addition to an existing policy page. Ask which, because text nobody can find fails the same way as text nobody wrote.

---

## Honest limits of this file

Several entries describe an absence, and an absence is harder to verify than a feature. Where documentation is silent rather than explicit, the entry above says what the documentation does and does not contain rather than asserting the platform forbids something.

Anything here that would change a merchant's plan materially should be confirmed in their own admin before the season, not taken on this file's word alone.
