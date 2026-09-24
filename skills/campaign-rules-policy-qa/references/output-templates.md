# Output

Up to seven parts, produced in this order. The cross-check table comes first when that mode ran. If the merchant asked only for a check, the terms may be short or absent and the findings come first.

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
- **Platform behaviour:** the threshold is measured on the discounted cart (from `platform-limits.md`, when relevant).
- **The merchant must pick one version**, then update: shipping policy, sale banner, FAQ, sale email.
- `[DECISION NEEDED: pick one version of the free shipping threshold: A, B, C or D]`

Rules for this table:

- Quote exactly. Never paraphrase a source, never tidy its wording.
- Mark any source the merchant described rather than pasted as "(described, not pasted)".
- Label each term Consistent, Mismatch, Incomplete or Stale.
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

In cross-check mode, write one version of each term for every source to use, with every unresolved mismatch left as `[DECISION NEEDED: ...]`.

Unknowns stay as `[DECISION NEEDED: <question>]` inside the text. Never a plausible placeholder, because a plausible placeholder gets published.

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
- My code did not work, what now?
- Will I have to pay import duties or taxes?
- What happens if I refuse to pay duties on delivery?

Do not write an answer for a field still marked as a decision. An empty question with a note is honest; an invented answer is not.

---

## 4. Staff decision table

One row per rule: the rule, the answer, and the exception if any. This exists so two agents on the same day give the same answer, and so a merchant can hand it to a seasonal hire.

| Rule | Answer | Exception |
|---|---|---|

Keep it terse. It gets read under pressure.

---

## 5. Open decisions

Everything still marked. For each: the question, who has to decide it, and whether it blocks publication.

List every unresolved cross-check mismatch here too, with the sources that change once it is picked.

Separate the blocking items from the rest. A merchant with two hours before a sale needs to know which three things actually have to be answered first.

---

## 6. What your store cannot enforce

Only when `platform-limits.md` found something. For each: what the merchant intends, what the platform will actually do, and what it costs to cover the difference by hand.

This section is often the most valuable thing produced, and it is the one nobody asks for.
