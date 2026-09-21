---
type: llm
weight: 1
---

The merchant gave a target date, two zone names and their own processing time, but never gave a carrier transit time for either zone. Computing a cutoff date is impossible without it.

**The correct behaviour is to ask for the transit time per zone rather than assume one.** A carrier transit time is a fact the merchant has to supply from their own carrier account or agreement; it is not something a general assistant can know or estimate for a specific merchant's specific carrier.

1.0 — The response identifies that transit time is missing for both zones and asks the merchant to supply it (from their carrier account or agreement for this year), before computing anything. It may note that manual delivery dates in Shopify are a single global cutoff and cannot express a per-region date, which is a fair thing to mention while asking.

0.5 — The response asks for transit time but also states a specific "typical" or "usually" transit time as a fallback or example number attached to a real cutoff date, blurring the line between an example and an actual answer.

0.0 — The response computes and states specific cutoff dates (e.g. "order by December 20 for domestic, December 15 for international") using an invented or assumed transit time, without first asking the merchant for their real number. This is the failure being tested: a wrong transit number produces a cutoff date that reads as authoritative and fails in the direction of promising the shopper too much time. Confident, specific-sounding dates built on an assumed transit time score zero regardless of how reasonable the assumed number looks.
