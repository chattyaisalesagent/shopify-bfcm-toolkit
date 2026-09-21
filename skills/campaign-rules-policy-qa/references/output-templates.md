# Output

Four artefacts, plus a platform note when one is needed. Produce them in this order. If the merchant asked only for a check, the first artefact may be short or absent and the findings come first.

Write files when the environment allows it and the merchant wants them; otherwise put the same content in the reply. The shape matters more than the delivery.

---

## 1. Findings, when auditing

Lead with this. Ordered by damage, not by where they appear in the text.

**Contradictions.** Quote both statements, say why they cannot both hold, and say which one the merchant has to change. Do not choose for them.

**Missing fields.** Name the field and what a shopper cannot work out without it. A bare list of field names does not tell the merchant why it matters.

**Ambiguities.** Quote the sentence, give the two readings, and say which decision resolves it.

Keep it to what is actually wrong. A finding list padded with observations buries the contradiction at the top.

---

## 2. Shopper-facing terms

Plain sentences, ordered the way a shopper hits the questions: what the offer is, what it applies to, what it does not, when it starts and ends with a timezone, what happens to returns, what happens if the code fails.

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
- My code did not work, what now?

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

Separate the blocking items from the rest. A merchant with two hours before a sale needs to know which three things actually have to be answered first.

---

## 6. What your store cannot enforce

Only when `platform-limits.md` found something. For each: what the merchant intends, what the platform will actually do, and what it costs to cover the difference by hand.

This section is often the most valuable thing produced, and it is the one nobody asks for.
