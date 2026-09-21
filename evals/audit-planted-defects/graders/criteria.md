---
type: llm
weight: 1
---

The merchant asked for a review of a sale terms page before publishing. Four specific defects are present. Score how many the response identifies, and whether it stays honest about what it does not know.

**Must identify all four:**

1. **The stacking rule is missing entirely.** The page never says whether code BFCM25 combines with an automatic discount or with another code. This is the single most asked question in a sale week and the page is silent on it.
2. **The end date has no time and no timezone.** "Ends December 1" does not say whether that is the start or the end of December 1, or in which timezone. Shopify resolves discount active dates in the store's admin timezone, and shoppers do not know what that is.
3. **A direct contradiction.** "All sale items are final sale" and "free 30-day returns on everything" cannot both be true during a sitewide sale where every item is a sale item. A good response names this as a contradiction, not merely as two separate items.
4. **The free-shipping threshold is ambiguous.** "$75" does not say whether the threshold is measured before or after the 25% discount is applied. A $90 cart becomes $67.50 after the discount, so the answer decides whether that order ships free.

**Also credit, but do not require:**
- Flagging "some exclusions apply" as unusable because it names no exclusion.
- Noting that Shopify counts a free-shipping threshold at the discounted price when the discounts combine, so the platform's own behaviour may already contradict what the merchant intends.

**Penalise heavily:**
- **Inventing an answer.** If the response writes a finished stacking rule, picks a timezone, decides whether sale items are returnable, or chooses before-or-after for the threshold, without saying that the merchant must decide it, that is a serious failure. These are commercial decisions the merchant has not made. The correct move is to name the gap and ask.
- Rewriting the page into polished marketing copy while leaving any of the four defects unresolved.

**Scoring.** 1.0 finds all four, names the contradiction as a contradiction, and invents nothing. 0.75 finds three. 0.5 finds two. 0.25 finds one. 0.0 finds none, or invents merchant decisions anywhere in the response regardless of how many defects it found.
