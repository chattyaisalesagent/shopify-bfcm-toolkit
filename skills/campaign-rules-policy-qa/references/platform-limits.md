# What the platform does and does not do on its own

Verified against Shopify's help centre on 24 September 2026. Each entry names its source page so it can be re-checked. Each entry says what the merchant should be told, because several of these are things a merchant reasonably assumes work differently.

Re-verify before relying on any of it in a new season. Platform behaviour moves.

The framing matters: almost everything a merchant promises can be honoured. The question is which part Shopify does automatically and which part a person does by hand. Never tell a merchant that orders are unprotected or that a promise cannot be kept when staff can create the return or refund manually. Say what the manual step is and who does it.

---

## Returns

Sources: help.shopify.com/en/manual/fulfillment/managing-orders/returns/return-rules, .../returns/self-serve-returns/setup, .../returns/self-serve-returns/management, .../returns/creating-returns, help.shopify.com/en/manual/customers/customer-accounts, help.shopify.com/en/manual/customers.

### What a return rule can express

- A **return window** of 14, 30, 90 days, unlimited, or a custom number of days, starting from each item's delivery or from delivery of the last item in the order. There is an option to extend a window that ends on a weekend or holiday to the next business day.
- **Return window overrides**: a different number of days for specific collections, products or variants. An override can be longer or shorter than the default. If an item is in more than one override, the shortest window applies.
- **Final sale items**: specific products or specific collections (not both at once) that cannot be returned. Final sale wins over any override. Bundles cannot be set as final sale.
- **Return shipping cost**: free, a flat fee per return, or the customer buys their own label. An optional **restocking fee** as a percentage.

### Rules are fixed when the order is placed

Return rules are applied to an order when the customer places it, and "changes to your return rules apply only to future orders". A merchant who lengthens the window in December has not changed anything for orders already placed in November.

Scheduling consequence: a holiday rule meant to cover orders from 1 November has to be saved before 1 November. Orders placed inside the promised range before the change keep the old window in the system and are honoured by hand (see below).

### A holiday window with calendar dates: approximate it, do not call it impossible

There is no rule based on purchase dates and no fixed calendar end date. A promise such as "anything bought 1 November to 24 December can be returned until 31 January" is approximated like this:

1. **Before the first covered order**, set the default window (or an override on the collections the promise covers) to a custom number of days long enough that the earliest covered order still reaches the deadline. Example: an order placed 1 November and delivered around 4 November needs about 88 days to reach 31 January, so a 90-day custom window covers it. Use the store's own delivery times.
2. **After the last covered purchase date**, set the window back to the normal length. Orders placed from then on get the normal window.
3. **Later orders in the range get more time in the system than the policy promises** (a 20 December order with 90 days runs into March). Self-serve requests are reviewed before approval, so staff decline requests that arrive after the published deadline, or the merchant decides to allow them. Say which.
4. **Edge cases are handled by hand**: orders placed in the range before the rule was changed, and any order delivered so early that the custom window ends before the deadline. Staff can create a return from the admin for any fulfilled item that has not been refunded, so these orders can always be honoured.

Tell the merchant which of these steps are automatic, which are manual, and roughly which orders fall into the manual group.

### Self-serve returns: who can use them

- Self-serve returns work through the **new customer accounts**. They do not work with legacy customer accounts. A store that keeps legacy accounts can still add the new customer accounts URL to its refund policy, footer or returns page, which gives customers access to request a return.
- Customers sign in with the **email address on the order and a 6-digit verification code** sent to that email. No password is needed. Every order adds the buyer to the store's customer list, and a customer with a customer profile already has an account. So a buyer who checked out as a guest can sign in with the order email and request a return themselves. Do not tell a merchant that guest buyers need a person.
- **Exchanges cannot be requested through self-serve returns**, and there are no exchange-specific return rules. Staff add exchange items when they approve or create the return.
- The sign-in code goes to the buyer's email, so a **gift recipient** cannot request a return on the buyer's order themselves. They need the buyer to do it, or they contact the store and a person creates the return.
- If customers can check out with only a phone number, the SMS link is their only route to self-serve, and they must enter an email address with the request.
- The merchant reviews every request and approves or declines it.

So the groups that need a person are gift recipients and anyone who wants an exchange, plus every shopper if the store has not turned self-serve returns on. If the policy mentions gifts or exchanges, say who handles them and how the shopper makes contact.

### Return fees are not deducted automatically

Return shipping fees and restocking fees are shown when a return is created, but "return fees aren't automatically deducted from refunds". Staff deduct them by hand when issuing the refund. A policy that says "$6.95 deducted from your refund" is honoured only if the person refunding does that step.

### Final sale is set by product or collection

Final-sale status lives in the return rules. It is not a property of a discount. Marking a collection final sale and then running a sitewide code produces the classic contradiction: the discount applies everywhere, the returns promise does not.

---

## Discounts

Sources: help.shopify.com/en/manual/discounts/discount-combinations, .../discounts/discount-types/free-shipping, .../discounts/discount-types/percentage-fixed-amount, help.shopify.com/en/manual/fulfillment/setup/shipping-rates/troubleshooting.

### The free shipping threshold and discounts: it depends on how free shipping is set up

There are two ways a store gives free shipping above an amount, and they behave differently.

- **A free shipping discount with a minimum purchase amount.** "Products are counted towards a minimum purchase amount at their discounted price." But "this happens only with discounts that can be combined. A discount that can't be combined with your free shipping discount never applies at the same time, so it never changes the minimum purchase amount." So if the sale code combines with the free shipping discount, the threshold is measured after the sale discount. If it does not combine, the shopper gets one or the other, never both.
- **A price-based shipping rate** (for example, $0 shipping for orders over $75 in a shipping zone). "The checkout determines shipping rates based on the total value of the cart after applying discounts, but before applying taxes." This is always after discounts.

Either way, a shopper who gets both the discount and free shipping has the threshold measured on the discounted cart. A $90 cart with 25% off becomes $67.50 and does not clear a $75 threshold. Shoppers read the pre-discount number and expect the opposite.

Ask the merchant which setup they use. The levers: lower the threshold for the sale period, or state the rule explicitly in the terms. Leaving the sentence as "free shipping on orders over $75" is not an option, because it does not say which $75.

### Active dates resolve in the store's admin timezone

"The time when the amount off discount starts and ends depends on the time zone that you select in your Shopify admin." A start date of 26 November in a store set to Eastern time starts at 12:00 am Eastern. Shoppers cannot see this timezone and most assume their own.

A bare end date is ambiguous twice over: start or end of that day, and whose day. Terms carry a time and a named timezone.

### Codes have a combination limit

At most **five product or order discount codes and one shipping discount code** can be entered on a single order. Combination is set per discount class (product, order, shipping) in each discount's combination settings.

### The checkout message explains nothing

When a shopper enters a code that cannot be combined with the discounts already applied, checkout shows exactly:

**Discount couldn't be used with your existing discounts**

It does not say which pair conflicted, why, or what would have worked. Quote it exactly whenever it goes into an FAQ or a saved reply, so staff and shoppers recognise it. This is the practical reason the stacking rule has to be written where a shopper can read it before checkout.

---

## Where the text lives

Source: help.shopify.com/en/manual/checkout-settings/refund-privacy-tos.

Shopify's written policies are six types: return, privacy, terms of service, shipping, legal notice, subscription. **There is no sale-terms or discount-terms page type.** The merchant chooses a home: a page linked from the banner, a section on the offer page, or an addition to an existing policy. Ask which, because text nobody can find fails the same way as text nobody wrote.

---

## International: US de minimis

Source: help.shopify.com/en/manual/international/duties-and-import-taxes/understanding-tariffs.

As of 29 August 2025, de minimis does not apply to shipments to the United States, so duties and import taxes apply to US imports regardless of value. Raise this only when the store ships into the US from another country (a US store shipping domestically is not affected), and only as a reason to state clearly who pays and when. It is not customs advice.

---

## Honest limits of this file

Some entries combine two documented facts (for example, guests can self-serve because every order creates a customer profile and a profile can sign in with its email). Where documentation is silent, this file does not assert that the platform forbids something.

Anything here that would change a merchant's plan materially should be confirmed in their own admin before the season.
