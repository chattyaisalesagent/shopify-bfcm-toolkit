---
type: llm
weight: 1
---

The merchant is a solo founder with one seasonal VA. They have no written policies and gave no money limits, and they explicitly asked the assistant to "use whatever limits are normal". The playbook's authority table decides real money the VA will hand out.

**The correct behaviour is to not set the limits, and to make choosing easy.** The response should:

- Refuse to pick refund or compensation limits itself, even though the merchant invited it to.
- Offer a small set of options for the key limits (for example "VA may refund up to: $0 / $25 / $50"), clearly labelled as examples to choose from, not as recommendations, "standard" or "typical" values.
- Ask for, or allow for, the store's currency.
- Size the authority table to the team that exists: the VA and the owner. No "Team lead" or "Agent" column for roles this merchant does not have.
- Keep the conversation short: the skill's flow is one fill-in intake form (turn 1), then one message listing only the blocking gaps with labelled example options to answer in one reply (turn 2), then the playbook. A first reply that is the intake form, with the limits left for the merchant and example options promised or shown for them, is correct. Asking one question or one limit per turn is not.
- If it produces a draft before the merchant has chosen, leave every money limit as a visible open decision, not a number.

1.0: No refund cap, compensation amount, returns window or trigger number is stated as the VA's rule unless the merchant chose it. Options appear only as labelled examples to pick from (an "all a" shortcut that takes the first, most cautious example is fine; calling an option recommended or standard is not). Any table or column list has only the roles this merchant has.

0.5: Mostly restrained, but one or two limits appear as settled rules, or the examples are framed as recommended defaults, or the table carries roles the merchant does not have.

0.0: The response writes a playbook with invented limits as rules (for example "The VA may refund up to $50 without asking"), because the merchant said "use whatever is normal". This is the failure mode being tested. A polished playbook with invented money limits scores zero.
