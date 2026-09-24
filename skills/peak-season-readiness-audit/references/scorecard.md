# The nine lines

Lines 1 to 6 are verbatim from the readiness scorecard in the peak-season research (Chatty, "Before BFCM 2026", page 19). Each line scores Ready (2 points), Partial (1 point) or Missing (0 points). Lines 7, 8 and 9 are additions, scored the same way but kept out of the 0 to 12 total so that total stays comparable to the published bands.

Before scoring any line, the audit asks what broke last peak season (see the skill body). Nothing on that list is a score by itself; it ranks the fixes and challenges self-reports.

## 1. Discount rules

- **Ready (2):** Written down and readable by the assistant handling shopper questions.
- **Partial (1):** Written but not loaded anywhere the assistant or staff can reach it.
- **Missing (0):** Only in the head of whoever runs the promotion.

**How to check.** Ask for the current or planned sale terms text. If a connector is available, `search_products` or a discount lookup can confirm a code exists, but existence of a code is not the same as the terms being written down; the terms text itself is what this line scores. If the same terms appear in several places (banner, FAQ, email) and they disagree, the line is at most Partial. Route per `references/routing.md`.

## 2. Order-by dates per region

- **Ready (2):** Published for every region the store sells to.
- **Partial (1):** One general date only, not broken out by region.
- **Missing (0):** Not published anywhere.

**How to check.** Ask for the published cutoff text, or find it on the site. Route per `references/routing.md`.

## 3. Automated order lookup

- **Ready (2):** Shoppers can self-serve, tested on a real order.
- **Partial (1):** The feature exists but has not been tested end to end.
- **Missing (0):** Every lookup still needs a person.

**How to check.** Ask whether order lookup is switched on in the chat app or helpdesk the store uses, and whether anyone has tested it on a real order recently. If a connector is available, `get-order` or `list-orders` confirm the underlying data is reachable, but do not confirm the shopper-facing self-serve path works; ask separately. This is set up inside the chat app, not in this kit. Route per `references/routing.md`.

## 4. Handoff to a person

- **Ready (2):** Rules, a summary, and someone with the authority to act.
- **Partial (1):** Handoff happens but the person receiving it has no context.
- **Missing (0):** No rules for when or how a handoff happens.

**How to check.** Ask who receives an escalated conversation, whether they get a summary or just a raw transcript, and whether that person can actually approve exceptions (refunds, address changes) or has to escalate again. The mechanics live in the chat app; the authority (who may decide what) is a written decision. Route per `references/routing.md`.

## 5. Weekly review

- **Ready (2):** Run for at least two consecutive weeks already.
- **Partial (1):** Done occasionally, not on a cadence.
- **Missing (0):** The list of unanswered messages has never been opened.

**How to check.** Ask when the store last reviewed its unanswered or fallback message list, and whether it happens on a schedule. The list lives in the chat app. Route per `references/routing.md`.

## 6. Plan cap and overage

- **Ready (2):** Compared against last year's BFCM week volume.
- **Partial (1):** The cap is known but has not been compared against expected load.
- **Missing (0):** The overage price is not known at all.

**How to check.** Ask what plan or tier the store's support or AI system is on, what the included allowance is, and what happens at the cap. No API reliably exposes this across vendors. Route per `references/routing.md`, which covers both the load comparison and the question list for the vendor.

---

## 7. Holiday returns and exchange policy (added, reported separately)

Added because it traces to its own finding in the research (stock and returns questions peak after the holiday, and returns is the subject stores are least often ready to answer even outside the holiday).

- **Ready (2):** The holiday returns window, who pays return shipping, and the gift-without-receipt case are all written down.
- **Partial (1):** Some of these are decided but not all, or decided but not published anywhere a shopper or a staff member can see them.
- **Missing (0):** None of this has been decided.

**How to check.** Ask for the current returns policy text and whether it says anything specific about the holiday period. Route per `references/routing.md`.

## 8. Proactive late-delivery notices (added, reported separately)

Shopify's built-in notifications include shipping update and delivered, but no delayed-delivery message. A store that has nothing prepared learns about a late order when the shopper writes in.

- **Ready (2):** Written messages exist for both "running late" and "will not arrive in time", with what the store offers stated, **and** a named person or a set routine finds late orders (past the promised date, tracking not moving) on a schedule so the message goes out before the shopper asks.
- **Partial (1):** One of the two halves only: messages are written but nobody is assigned to spot late orders, or someone watches for late orders but the messages would be written on the day.
- **Missing (0):** Late orders are discovered when the shopper complains.

**How to check.** Ask the merchant to paste the late-delivery message text, and ask who checks shipped orders for delays, how often, and using what. A described but unpasted message is self-reported. Route per `references/routing.md`.

## 9. Contingency plan (added, reported separately)

Three situations that recur every peak season: the carrier is delayed, a product sells out mid-sale, and message volume runs above forecast.

- **Ready (2):** A written plan exists for all three, and each names who decides, what shoppers are told, and what staff may offer without asking (for example the maximum goodwill credit).
- **Partial (1):** One or two of the three are covered, or all three are agreed verbally but nothing is written that a seasonal hire could follow.
- **Missing (0):** None of the three has been thought through.

**How to check.** Ask for the plan text, or for each situation ask "what happens the day this happens, and who decides". Score only from what they show or say; do not fill in a plan. Route per `references/routing.md`.

---

## Scoring

Sum lines 1 to 6 only, 0 to 12.

| Total | Band | Meaning |
|---|---|---|
| 10 to 12 | Ready | What remains is keeping the weekly review going |
| 6 to 9 | Foundations exist | Untested under load. Start with the lines scored Partial |
| Below 6 | Start here | Start with two lines scored Missing, prioritised by which deadline in the season is nearest |

Report lines 7, 8 and 9 alongside the total, not folded into it: "6-line score: 8/12 (Foundations exist). Returns policy: Partial. Late-delivery notices: Missing. Contingency plan: Partial."

A line you could not judge is reported as "Not scored: <what is missing>", never given a level. If any of lines 1 to 6 is unscored, report the total as "x/12 from the lines scored, n lines not scored" rather than a band.

## The critical-line override

Lines 3, 4 and 6 (order lookup, handoff, plan cap) outrank the total. If any of the three is Missing, say so first, before the total, regardless of what the total is. A store can score 10/12 and still be one plan-cap surprise away from the AI going silent in the busiest week.
