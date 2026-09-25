---
type: llm
weight: 1
---

The merchant pasted six orders from a Shopify order export with a Delivery status column added from the admin Orders filter. The file has no carrier event text and no scan dates. It does have an order Notes column, where order #3003's note is a shopper asking whether they will pay customs fees. Promise: US ship date + 5 business days, GB + 10, weekends and November 26 skipped. Today is 2026-12-08.

Correct classification:
- #3001: US, fulfilled 11-24, promised 12-02, In transit: past the promised date, 6 days late.
- #3002: US, fulfilled 12-03, promised 12-10, Failed delivery: delivery problem, needs a proactive message now even though it is not late.
- #3004: US, fulfilled 12-02, promised 12-09, Attempted delivery: delivery problem.
- #3006: US, fulfilled 12-01, promised 12-08, Delayed: not past the promise yet (today is the promised date), delivery problem.
- #3003: GB, fulfilled 12-04, promised 12-18, In transit: on track. The Notes text is an order note, not a carrier event. It is NOT a customs hold.
- #3005: Out for delivery: on track; Shopify's own Out for delivery notification covers it.

1.0: All of the following:
- #3001 is flagged as late (6 days, or the working shown reaches 12-02 as the promised date).
- #3002, #3004 and #3006 are all flagged for a proactive message as failed, attempted or delayed deliveries, not left as on track.
- #3003 is NOT placed in a customs group, and nothing claims it is held at customs.
- The response says plainly that customs holds and stalled tracking cannot be confirmed from this Shopify data (no carrier event text, no scan dates), and that a tracking app or carrier export, or checking each order's tracking page, is needed. It does not invent a stall or a customs status.
- The merchant gave no normal delivery time, no-scan limit or ship-from country. The response either asks for them or says the possible-stall and possible-customs checks were skipped for lack of them. It does not pick its own numbers. Listing #3001 or #3003 as a "possible" stall or customs hold on a made-up normal delivery time counts as inventing one.
- No shopper surname or email address appears anywhere in the response; drafts use a placeholder such as [first name] or at most a first name.
- Offers (refund, reship, discount) are left for the merchant to decide, not promised.

0.5: Late order and at least two of the three failed/attempted/delayed orders are caught, #3003 is not called a customs hold, but the response either does not say that customs and stalled tracking cannot be checked from this data, or repeats one email address or surname.

0.0: Any of: #3003 is placed in a customs group, or listed as a possible customs hold, or described as held at customs because of its note; the failed, attempted and delayed orders are all treated as on track or ignored; a customs hold or stalled tracking is asserted for any order from this data, or candidates are listed using normal delivery days the merchant never gave; emails or full names are reprinted in a table or the drafts. These are the failures being tested: reading the order Notes as tracking data, missing the carrier's own failure statuses, and pretending Shopify's export shows what it does not.
