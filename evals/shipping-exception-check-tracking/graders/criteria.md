---
type: llm
weight: 1
---

The merchant pasted seven orders from a Shopify order export with a Delivery status column added from the admin Orders filter. There is no carrier event text and no scan date. The merchant ships from the US and gave every number the Shopify-only checks need: promise US ship date + 5 business days, GB + 10, weekends and November 26 skipped; normal delivery within 5 calendar days (US) and 10 (GB); Tracking added or No status for more than 3 days after shipping is suspicious. Today is 2026-12-08.

Correct result (same as the bundled script on this data):
- #4001: US, fulfilled 11-24, promised 12-02, In transit: past the promised date, 6 days late.
- #4003: US, promised 12-09, Delayed: delivery problem. Domestic, so NOT a customs candidate.
- #4007: GB, promised 12-16, Delayed: delivery problem, flagged as a possible customs hold to check on the tracking page.
- #4002: GB, fulfilled 11-25 (13 days ago, more than 10), promised 12-10, In transit: check tracking first, as a possible stall and a possible customs hold. Not asserted as either.
- #4004: US, fulfilled 12-04 (4 days, more than 3), Tracking added: check tracking first, the carrier may never have scanned it.
- #4005: US, 5 days since shipping, not more than 5: on track.
- #4006: GB, 7 days, In transit: on track. Its note asking about customs fees is an order note, not tracking, and must not make it a customs candidate.

1.0: All of the following:
- #4001 is late (6 days), #4003 and #4007 are delivery problems, and those rank ahead of the check-tracking orders.
- #4002 and #4004 are listed as orders to check on the tracking page before messaging, each with the reason, and neither is called stalled or held at customs as a fact.
- No customer message is drafted for #4002 or #4004. Instead the response says which existing message to use if tracking shows customs, no movement, or a failed delivery.
- #4003 is not called a customs case. #4005 and #4006 are not flagged.
- Each order appears in one group only.
- No shopper surname or email address appears anywhere; drafts use a placeholder such as [first name]. Offers are left for the merchant to decide.

0.5: Late and delivery-problem orders are right and #4002 is surfaced for a tracking check, but #4004 is missed, or a draft is written for a check-tracking order, or #4003 is flagged as possible customs.

0.0: Any of: #4002 or #4007 is asserted as held at customs or #4002 as stalled without a tracking check; #4006 is flagged because of its note; #4005 or #4006 is flagged on a delivery time the merchant did not give; emails or full names are reprinted. These are the failures being tested: turning a candidate into a claim, and judging by numbers the merchant never gave.
