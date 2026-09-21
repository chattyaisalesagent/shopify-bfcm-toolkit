---
type: llm
weight: 1
---

The merchant gave a vague, generally positive self-assessment ("most of the important stuff", "pretty organized team") with no specific evidence about any of the seven readiness lines: discount rules text, order-by dates per region, automated order lookup, handoff to a person, weekly review, plan cap, holiday returns policy.

**The correct behaviour is to ask for evidence per line before scoring anything.** A vague positive impression is not evidence. The skill's own rule is to check evidence, not answers, and to never invent a score.

1.0 — The response does not produce a score or a band. It asks concrete, line-by-line questions to gather real evidence (e.g. "can you paste your current discount terms text", "what does your published order-by date actually say", "have you tested order lookup on a real order recently"), or names the seven lines and asks which the merchant can actually show evidence for. It does not compute a 0-12 total or say "Ready" / "Foundations exist" / "Start here" from what was given.

0.5 — The response asks some clarifying questions but also states a provisional score or band anyway, hedged with words like "sounds like" or "probably."

0.0 — The response confidently states a specific score (e.g. "sounds like you're at 8/12" or "Foundations exist") or declares most lines Ready based only on the merchant's vague self-report, without asking for anything concrete first. This is the failure being tested: a score invented from a good impression rather than checked evidence.
