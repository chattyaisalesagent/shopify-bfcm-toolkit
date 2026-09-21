# The fields

Two packs. Read the one the request needs. Every field is a merchant decision, so the outcome of checking a field is one of three states, never an answer you supply:

- **Stated and unambiguous.** Reproduce it.
- **Stated but ambiguous.** A defect. Say what is ambiguous and what the two readings are.
- **Absent.** Mark `[DECISION NEEDED: ...]`.

Not every field applies to every sale. A store with no free shipping has no threshold question. Skip what does not apply; do not pad the output with fields that were never relevant.

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

## Pack B. Holiday returns and exchanges

**1. The window.** How many days, measured from what event, or a seasonal promise with a fixed end date. If it is a seasonal promise, the enforceability limit in `platform-limits.md` applies and must be raised.

**2. Which orders it covers.** Stated as dates. Then check the timing consequence: a rule has to exist before the orders it covers are placed.

**3. Who pays return shipping.** Free, a flat fee, or the customer buys the label.

**4. Restocking fee.** Whether one applies, and how much.

**5. Final sale.** Which products or collections, and whether that survives the holiday extension or is suspended for it.

**6. Exchanges.** Whether they are offered, how a customer starts one, and who handles it given that self-serve does not cover exchanges.

**7. A gift without a receipt.** What the recipient can do, what they need to prove, and what they get back. Most policies are silent here and it is the single most common post-holiday question.

**8. Refund destination.** Original payment method, store credit, or the customer's choice.

**9. Publication deadline.** When this has to be live. Shoppers read it on 26 December, when nobody is on shift, so it is live before the holiday or it is not doing its job.

---

## Cross-checks

Run these after the individual fields. Each is a pair that reads fine separately and cannot both be true.

- A sitewide sale plus "all sale items are final" plus any general returns promise. During a sitewide sale, every item is a sale item.
- A free-shipping threshold plus a percentage discount, where the terms never say which price the threshold measures.
- An extended holiday window plus final-sale collections, where neither says which wins.
- A gift exchange promise plus a self-serve returns flow that cannot process exchanges or serve someone without an account.
- A stated end date plus a stated timezone that differs from the store's admin timezone.
