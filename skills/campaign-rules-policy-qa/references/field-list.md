# The fields

Four packs, plus the cross-check term list. Read the packs the request needs. Every field is a merchant decision (or, in Pack D, a product fact only the merchant can confirm), so the outcome of checking a field is one of three states, never an answer you supply:

- **Stated and unambiguous.** Reproduce it.
- **Stated but ambiguous.** A defect. Say what is ambiguous and what the two readings are.
- **Absent.** Mark `[DECISION NEEDED: ...]`.

Not every field applies to every store. A store with no free shipping has no threshold question; a store that ships only domestically has no Pack C. Skip what does not apply; do not pad the output with fields that were never relevant.

---

## Pack A. Discount and campaign rules

**1. Combination with other discounts.** Does the code combine with an automatic discount? With another code? With a shipping discount? These are three separate answers, and a merchant who says "no stacking" has usually only thought about the second.

**2. Eligibility of already-reduced items.** Does the code apply to items already marked down? This is the most asked question of a sale week and the one most often missing from the page.

**3. Returnability of discounted items.** Can items bought with the code be returned? Under the normal window, a shorter one, or not at all? Cross-check against the final-sale settings; see `platform-limits.md`.

**4. Free-shipping threshold.** Is there one, does it change for the sale, and is it measured **before or after** the discount? The platform answer is in `platform-limits.md` and the merchant still has to decide what to publish and whether to move the threshold.

**5. Start and end.** Date, time and named timezone, for both ends. A bare date is a defect.

**6. Exclusions.** Which products, collections or regions are excluded. "Some exclusions apply" names none and is unusable; treat it as absent, not as present.

**7. Gift purchases.** Can a recipient exchange an item bought with the code, and what do they need in order to do it? Cross-check with the self-serve limitation in `platform-limits.md`.

**8. When a code fails.** What the shopper should do, and who they contact. The checkout message explains nothing, so if the terms do not cover this the shopper's only route is to leave.

---

## Pack B. Holiday and post-holiday returns

**1. Which orders the holiday window covers.** Start and end, stated as purchase or delivery dates. Then check the timing consequence: on Shopify a return rule change applies only to future orders, so a rule meant to cover orders from 1 November has to exist before 1 November.

**2. The return deadline.** How many days, measured from what event (delivery, purchase), or a seasonal promise with a fixed calendar end date. If it is a fixed end date, the enforceability limit in `platform-limits.md` applies and must be raised.

**3. Gift returns and gift receipts.** Does the store issue gift receipts or gift notes? What can a recipient without a receipt do, what must they provide (order number, buyer's name or email), and what do they get back (store credit, exchange, refund to the buyer)? Is the buyer told? Most policies are silent here and it is the single most common post-holiday question.

**4. Exchanges versus refunds.** Which is offered, whether the customer chooses, how a customer starts an exchange given that self-serve returns do not cover exchanges, and what happens when the exchange item is out of stock or costs a different amount.

**5. Who pays return shipping.** Free, a flat fee deducted, or the customer buys the label. Whether this differs for exchanges, faulty items, and gift recipients.

**6. Condition rules.** Tags attached, unworn or unused, original packaging, opened items, hygiene or personalised items that cannot come back. Stated in words a shopper can check against the item in their hand.

**7. Items bought with a discount.** The refund is the price actually paid, not the list price: does the policy say so? What happens on a partial return from a bundle, a buy-one-get-one, or an order that received a gift with purchase? If a partial return drops the order below the free-shipping threshold, is the shipping charged back? Are sale or final-sale items covered by the holiday window or excluded from it?

**8. Restocking fee.** Whether one applies, and how much.

**9. Refund destination.** Original payment method, store credit, or the customer's choice.

**10. Publication deadline.** When this has to be live. Shoppers read it on 26 December, when nobody is on shift, so it is live before the holiday or it is not doing its job.

---

## Pack C. International orders, duties and taxes

Only for stores that ship across borders. Every answer here is a merchant decision; none of it is customs or legal advice.

**1. Who pays duties and import taxes.** The store (prices include them, often called delivered duty paid) or the shopper (paid to the carrier or customs on delivery). Per destination if it differs.

**2. Whether they are charged at checkout.** Are duties and taxes calculated and collected at checkout, or left to be collected on delivery? If collected at checkout, is that on for every destination the store sells to?

**3. What the shopper is told, and where.** The exact sentence on the product page, cart, checkout, shipping policy and order confirmation. A shopper who first learns about duties from a carrier's payment request is the most common source of a refused parcel.

**4. Refused or unclaimed parcels.** If the shopper refuses to pay duties on delivery: is the order refunded, minus what (original shipping, return shipping, duties the store already paid)? Who tells the shopper this before they refuse?

**5. International returns.** Who pays return shipping across the border, and are duties or taxes refunded on a return? The store often cannot recover them; the policy must say what the shopper gets back.

**6. International order-by dates.** If the store publishes holiday cutoffs, are international zones listed separately? Cross-border transit is longer and customs adds time. The dates themselves come from `delivery-cutoff-planner`; this field only checks the policy mentions them.

**Why this matters more than it used to, for US shoppers.** Since 29 August 2025 the US no longer applies the de minimis exemption that let low-value parcels enter duty-free, so a parcel of any value shipped to a US shopper can now carry duties or fees. Treat this as a reason to state clearly who pays and when, not as a statement of what any parcel will be charged. It is not legal or customs advice; the merchant should confirm current rules with their carrier or a customs broker.

---

## Pack D. Product claims consistency

For when the merchant pastes product text from more than one place: product page, collection page, marketplace listing, email, ads copy, FAQ, packaging text, saved replies, AI assistant knowledge.

A product claim is a fact about the product. The skill cannot see the product, so it never decides which version is true. It lines the versions up and asks the merchant to confirm from supplier documentation.

**1. Materials and ingredients.** Fabric composition, metals, "contains latex" versus "latex-free", "100% cotton" versus "cotton blend".

**2. Allergens.** Nuts, gluten, dairy, latex, fragrance, nickel. A missing allergen statement in one place when another place states one is a mismatch, not a gap to ignore.

**3. Safety and age.** Age grading, choking warnings, "BPA-free", "non-toxic", flammability, electrical safety.

**4. Certifications and standards.** Organic, vegan, cruelty-free, CE, FDA, any named certification. The certification name and scope must match.

**5. Size, fit and dimensions.** Measurements and size charts that differ between sources.

**6. Origin and care.** "Made in", care and washing instructions, warranty length.

Any mismatch on 1 to 4 is ranked above every commercial mismatch in the findings, because a wrong allergen or safety claim can harm someone.

---

## Cross-check term list

In cross-check mode, extract every statement about each of these terms from every pasted source and line them up:

- Free shipping threshold: amount, currency, before or after discount, regions it covers
- Returns window: length, the event it counts from, holiday extension dates
- Return of sale and final-sale items
- Code stacking: with automatic discounts, with other codes, with shipping discounts
- Already-reduced items: whether the code applies
- Sale start and end: date, time, timezone
- Exclusions: products, collections, regions
- Who pays return shipping
- Refund method: original payment, store credit, choice
- Gift returns and gift receipts
- Exchanges
- Order-by dates per region
- Duties and taxes: who pays, when, what the shopper is told
- Every product claim from Pack D

Typical places to collect from: returns policy, shipping policy, terms of service, FAQ, sale banner or announcement bar, promotional emails and SMS, product pages, cart or checkout notes, saved replies and macros, AI assistant knowledge base, social posts.

---

## Logical cross-checks within the text

Run these after the individual fields. Each is a pair that reads fine separately and cannot both be true.

- A sitewide sale plus "all sale items are final" plus any general returns promise. During a sitewide sale, every item is a sale item.
- A free-shipping threshold plus a percentage discount, where the terms never say which price the threshold measures.
- An extended holiday window plus final-sale collections, where neither says which wins.
- A gift exchange promise plus a self-serve returns flow that cannot process exchanges or serve someone without an account.
- A stated end date plus a stated timezone that differs from the store's admin timezone.
- "Free returns" plus international shipping, where the policy never says whether cross-border returns are included.
- "No hidden fees" or "the price you see is the price you pay" plus shopper-paid duties on delivery.
