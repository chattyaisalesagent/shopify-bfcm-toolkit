# Output

The work is delivered in two replies, with a decision round between them. The promise to the merchant is one clean version of their terms, ready to publish, so the final reply must not carry a placeholder on anything that blocks publication.

**First reply:** the cross-check table (when two or more places were pasted), the findings, and the blocking decisions as a numbered batch.

**Decision round:** the merchant answers the batch, in one reply or one question at a time. Ask again for any answer that is unclear or opens a new blocking gap. If nothing blocks, skip straight to the final reply.

**Final reply:** shopper-facing terms, FAQ answers, staff decision table, replacement text for every place that changes, what Shopify does automatically versus by hand, and any non-blocking decisions left.

If the merchant asked only for a check and does not want to decide yet, stop after the first reply and say which answers would unlock the final text.

Write files when the environment allows it and the merchant wants them; otherwise put the same content in the reply. The shape matters more than the delivery.

---

## 0. Cross-check table, when cross-checking

Lead with this. One block per term, product-claim terms first, then the terms with a mismatch, then incomplete and stale ones. Consistent terms are listed in one line at the end ("Consistent across all sources: code stacking, refund method"), not tabled.

**Term: Free shipping threshold** (Mismatch)

| Source | Exact wording |
|---|---|
| Shipping policy | "Free shipping on orders over $75" |
| Sale banner | "Free shipping over $50 this weekend" |
| FAQ | "Free shipping on orders of $75 or more after discounts" |
| Sale email | "Free shipping on everything this weekend" |

- **Versions:** A, $75, threshold measure not stated (shipping policy). B, $50 during the sale (banner). C, $75 measured after discounts (FAQ). D, no threshold during the sale (sale email).
- **Platform behaviour:** when the shopper gets both the discount and free shipping, the threshold is measured on the discounted cart (from `platform-limits.md`, when relevant).
- **The merchant must pick one version**, then update: shipping policy, sale banner, FAQ, sale email.
- `[DECISION NEEDED: pick one version of the free shipping threshold: A, B, C or D]`

Rules for this table:

- Quote exactly. Never paraphrase a source, never tidy its wording.
- Mark any source the merchant described rather than pasted as "(described, not pasted)".
- Label each term Consistent, Mismatch, Incomplete or Stale. Mismatch means a shopper would get a different answer depending on where they read ("30 days of delivery" against "until January 31" is a Mismatch, not Incomplete). Incomplete means one place leaves out a condition but what it says is not wrong.
- Never choose the version. Name the choice and the places that change.
- For a product-claim mismatch, the line is "The merchant must confirm the true fact from supplier documentation", not "pick one", because a claim is a fact, not a preference.

---

## 1. Findings, when auditing

Right after the cross-check table, or first if there is none. Ordered by damage, not by where they appear in the text.

**Product-claim mismatches**, if any, before everything else. A wrong allergen, material or safety claim can harm someone.

**Contradictions.** Quote both statements, say why they cannot both hold, and say which one the merchant has to change. Do not choose for them.

**Missing fields.** Name the field and what a shopper cannot work out without it. A bare list of field names does not tell the merchant why it matters.

**Ambiguities.** Quote the sentence, give the two readings, and say which decision resolves it.

Keep it to what is actually wrong. A finding list padded with observations buries the contradiction at the top.

---

## 2. Shopper-facing terms

Plain sentences, ordered the way a shopper hits the questions: what the offer is, what it applies to, what it does not, when it starts and ends with a timezone, what happens to returns, what happens if the code fails. For a post-holiday returns policy: which orders it covers, the deadline, condition rules, gifts, exchanges, who pays return shipping, how discounted items are refunded, where the money goes. For international orders: who pays duties and taxes, when they are charged, and what happens if a parcel is refused.

Written in the final reply, from the merchant's answers. In cross-check mode, write one version of each term for every source to use.

No blocking item may remain as `[DECISION NEEDED: ...]` here; if one is still open, go back to the decision round instead of printing. A non-blocking gap is left out of the text and listed in part 7, never filled with a plausible placeholder, because a plausible placeholder gets published.

No marketing language. This text exists to be quoted back at the store, so it should read like something the store is prepared to be held to.

---

## 3. FAQ answers

Each of these is a real question, short answer, two or three sentences, phrased for a shopper. They go into a help page, an agent's macro, and any assistant's knowledge base without further editing.

Write one for each field that was actually decided. Typical set:

- Does this code work on items already on sale?
- Can I use two codes together?
- Is free shipping calculated before or after the discount?
- Can I return something I bought on sale?
- When exactly does the sale end?
- I received this as a gift, can I exchange it?
- I have no gift receipt, what can I do?
- Can I exchange for a different size instead of a refund?
- Who pays for return shipping?
- I bought this with a discount, how much do I get back?
- My code did not work, what now? (Quote the checkout message exactly: Discount couldn't be used with your existing discounts)
- I checked out as a guest, can I still start a return myself?
- Will I have to pay import duties or taxes?
- What happens if I refuse to pay duties on delivery?

Do not write an answer for a field still undecided. An invented answer is worse than a missing one.

Check each answer against a guest buyer, a gift recipient, a shopper who wants an exchange and a shopper in each country the store ships to. A saved reply that says "just log in" is wrong for a gift recipient; "free returns on all orders" is wrong if cross-border returns are not free.

---

## 4. Staff decision table

One row per rule: the rule, the answer, and the exception if any. This exists so two agents on the same day give the same answer, and so a merchant can hand it to a seasonal hire.

| Rule | Answer | Exception |
|---|---|---|

Keep it terse. It gets read under pressure.

---

## 5. Replacement text per place

For each place that has to change (banner, FAQ, email template, saved reply, product page), the exact new text. The merchant pastes these in; nothing is left saying the old thing.

---

## 6. What Shopify does automatically and what staff do by hand

Only when `platform-limits.md` applies. For each: what the merchant promises, what Shopify does on its own, the manual step that honours the rest, who does it, and the settings to change with the date to change them (for example: set a 90-day custom return window before 1 November, set it back on 25 December, decline self-serve requests after 31 January).

Never say an order is unprotected when staff can honour the page by hand. Say what the hand step is.

---

## 7. Decisions

**In the first reply, blocking decisions only**, as a numbered batch the merchant can answer in one message, each with the known options (A, B) and the places that change once picked.

A decision **blocks publication** if its answer changes whether a shopper qualifies, what they pay, a date or time, eligibility, or the refund amount, method or window. The free shipping threshold measured before or after discount, and the sale start and end time with timezone, always block. So does every product-claim mismatch. Wording, tone and layout never block.

**In the final reply, non-blocking decisions left**, if any, each with who decides.
