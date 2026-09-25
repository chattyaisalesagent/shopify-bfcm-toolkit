# Worked example, 2026, counted by hand

Calendar anchors used for every weekday below: 1 November 2026 is a Sunday, so 26 November (Thanksgiving) is a Thursday, 24 December is a Thursday and 25 December is a Friday. The same cases run in `tests/delivery-cutoff-planner/`.

## Example 1: Christmas Eve target, carrier runs Saturday

Inputs: target Thu 24 Dec. Warehouse closed Sat and Sun, order cutoff 2 pm ET. Carrier closed Sun only. Transit 3 carrier days (from the transit time on the merchant's Standard rate in Shopify). Processing 2. Buffer 1.

| Date | Weekday | Warehouse open? | Carrier running? | Counted as |
|---|---|---|---|---|
| 24 Dec | Thu | yes | yes | delivery day (day 0) |
| 23 Dec | Wed | yes | yes | transit 1 |
| 22 Dec | Tue | yes | yes | transit 2 |
| 21 Dec | Mon | yes | yes | transit 3, ship day |
| 20 Dec | Sun | no | no | skipped: warehouse closed |
| 19 Dec | Sat | no | yes | skipped: warehouse closed |
| 18 Dec | Fri | yes | yes | processing 1 |
| 17 Dec | Thu | yes | yes | processing 2, order day |
| 16 Dec | Wed | yes | yes | buffer 1, cutoff date |

Publishable line: **Order by 2 pm ET, Wed 16 Dec for delivery to US by Thu 24 Dec.**

Check it forward: an order at 1 pm on Thu 17 Dec (no buffer) has order day Thu 17, is handed over on the 2nd warehouse open day after that (Fri 18 is 1, Mon 21 is 2), then travels 3 carrier days (Tue 22, Wed 23, Thu 24). It arrives Thu 24. The buffer moves the published date one more warehouse day back to Wed 16.

## Example 2: Christmas Day target the carrier does not deliver on

Inputs: target Fri 25 Dec. Warehouse and carrier both closed Sat, Sun and 25 Dec. Transit 2. Processing 1. Buffer 0.

| Date | Weekday | Warehouse open? | Carrier running? | Counted as |
|---|---|---|---|---|
| 25 Dec | Fri | no | no | skipped: carrier closed, no delivery |
| 24 Dec | Thu | yes | yes | delivery day (day 0) |
| 23 Dec | Wed | yes | yes | transit 1 |
| 22 Dec | Tue | yes | yes | transit 2, ship day |
| 21 Dec | Mon | yes | yes | processing 1, order day, cutoff date |

Cutoff: **Mon 21 Dec**.

Why the target is rolled back first: counting "start the day before the target" would count Thu 24 as a transit day and give Tue 22. An order on Tue 22 ships Wed 23 and needs 2 carrier days, Thu 24 and then the next carrier day, which is Mon 28. The promise breaks. Rolling the target back to the last day the carrier actually delivers fixes it.

## Example 3: range transit and Thanksgiving

Inputs: target Fri 4 Dec. Warehouse and carrier closed Sat, Sun and 26 Nov. Transit given as "5-8", so 8 is used. Processing 2. Buffer 1.

Delivery day Fri 4 Dec. Transit: Thu 3 (1), Wed 2 (2), Tue 1 (3), Mon 30 Nov (4), Sun 29 and Sat 28 skipped, Fri 27 (5), Thu 26 skipped (closed), Wed 25 (6), Tue 24 (7), Mon 23 (8, ship day). Processing: Sun 22 and Sat 21 skipped, Fri 20 (1), Thu 19 (2, order day). Buffer: Wed 18 (1).

Cutoff: **Wed 18 Nov**.

## Example 4: the carrier's published ship-by date

Inputs: the carrier's page says ship by Sat 19 Dec for delivery by 24 Dec. Warehouse closed Sat and Sun. Processing 1. Buffer 1.

The warehouse cannot hand over on Sat 19, so the ship day is Fri 18. Processing: Thu 17 (order day). Buffer: Wed 16. Cutoff: **Wed 16 Dec**.
