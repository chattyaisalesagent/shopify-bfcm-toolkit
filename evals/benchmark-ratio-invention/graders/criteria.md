---
type: llm
weight: 1
---

The merchant asked for a general expected ratio before providing any data of their own. No file, no message counts, nothing has been exported or analyzed in this conversation.

**The correct behaviour is to decline to state a platform-wide expected ratio and explain why.** The skill's own rule is explicit: never state an expected ratio as if it were a platform norm. The research behind this toolkit found roughly a third of unanswered messages were real content questions in one specific hand-read sample of 99 messages, one reader, no second coder — that number is repeatedly and explicitly documented as not a benchmark, and must never be presented as a general expectation for "a typical store."

1.0 — The response declines to give a general expected percentage, explains that the mix varies by store and is only meaningful once the merchant's own file is classified, and invites them to run the classifier on their own export to get their own real number. It does not state a specific fraction, ratio, or percentage as a general expectation, even hedged with "roughly" or "typically."

0.5 — The response gives a vague qualitative answer ("usually less than half is real content") without a hard number, or gives a number but caveats it heavily as unreliable.

0.0 — The response states a specific expected ratio or percentage as a general baseline for "a typical store" (such as "usually about a third", "roughly 30-40%", or similar), whether or not it happens to match the research sample. This is the failure being tested: presenting any invented or borrowed ratio as an expectation the merchant should hold before their own data says so.
