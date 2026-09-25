# The nine lines

Lines 1 to 6 follow the six-line scorecard in Chatty's "Before BFCM 2026" report. Two changes make it work for every store: line 3 counts Shopify's own Order status page, not only order lookup in a chat, and lines 3, 5 and 6 can be Not applicable when the store does not have the thing the line checks. Lines 5 and 6 also accept a first-season store's forecast in place of last year's numbers.

Each line scores Ready (2 points), Partial (1 point) or Missing (0 points). "Not applicable: <reason>" is allowed only on lines 3, 5 and 6, only when the condition below is true from what the merchant said. "Not scored: <what is missing>" is for a line that applies but cannot be judged.

Lines 7, 8 and 9 are additions, scored the same way but kept out of the score.

Before scoring, the audit asks what broke last peak season and how the store's support is set up (see the skill body).

## 1. Discount rules

- **Ready (2):** Terms written (stacking, minimum spend, start and end with timezone, exclusions) where whoever replies to shoppers can read them: staff, saved replies, any assistant.
- **Partial (1):** Written but out of their reach, or worded differently in different places.
- **Missing (0):** Only in the head of whoever runs the promotion.

**How to check.** Ask for the sale terms text. With a connector, `graphql_query` can read how a discount is set up (whether it combines with product, order or shipping discounts, minimum, dates), but a code existing is not the same as the terms being written; the text is what this line scores. If the terms appear in several places and disagree, the line is at most Partial.

## 2. Order-by dates per region

- **Ready (2):** Published for every region the store sells to.
- **Partial (1):** One general date, or dates for only some of the regions the store sells to.
- **Missing (0):** Not published.

**How to check.** Ask for the published cutoff text, or find it on the site.

## 3. Self-serve order status

Shopify gives every store an Order status page. Order confirmation emails can link to it, and once a tracking number is added at fulfilment, shoppers can follow the parcel there, in shipping notification emails and in the Shop app. Shoppers without an account can reach it with the order number plus their email or phone. Shopify Inbox also has a "Track my order" instant answer, on by default (Sales channels, Inbox, Chat settings, Instant answers). Sources: help.shopify.com/en/manual/fulfillment/setup/order-status-page/order-tracking, .../understanding-order-status-pages, help.shopify.com/en/manual/inbox/chat-settings-and-appearance/instant-answers (checked 24 September 2026).

- **Ready (2):** Orders ship with a tracking number, so the Order status page and shipping emails show tracking; if the store has a chat, its order lookup works too; tested on a real order this season.
- **Partial (1):** The Order status page works, but some orders ship without tracking, or nobody has tested it, or the chat's order lookup is off or untested.
- **Missing (0):** No tracking; every "where is my order" needs a person.
- **Not applicable:** The store ships nothing (digital products or services only).

**How to check.** Ask whether every order gets a tracking number at fulfilment, whether anyone has opened the shipping email link on a real order this season, and whether any chat on the store has order lookup switched on and tested. With a connector, `get-order` shows fulfilment and tracking on a real order; it does not prove the shopper-facing path was tested, so ask separately. This is set up in Shopify and the chat app, not in a kit tool.

## 4. Handoff to a person

- **Ready (2):** Rules for when a conversation goes to a person; that person sees the conversation so far and can approve refunds and address changes, or knows who can. If no bot replies and one person handles every conversation, Ready when that person can make those decisions.
- **Partial (1):** Handoff happens but the person has no context or no authority.
- **Missing (0):** No rules for when or how.

**How to check.** Ask who receives an escalated conversation, whether they see the history, and whether they can approve exceptions or must pass it on again. The mechanics live in the chat or helpdesk app; the authority is a written decision.

## 5. Weekly review of questions the assistant could not answer

- **Ready (2):** On a fixed weekday with a named owner, done at least twice already, or every week since the assistant went live if that was less than two weeks ago.
- **Partial (1):** Done now and then, not on a schedule.
- **Missing (0):** The list has never been opened.
- **Not applicable:** No AI assistant or bot replies to shoppers on its own; people handle every conversation. Fixed FAQ buttons such as Shopify Inbox instant answers do not count as an assistant. If Shopify Inbox's AI agent is switched on, the line applies.

**How to check.** Ask whether any assistant replies without a person, and if so when its list of unanswered or passed-on conversations was last opened.

## 6. Plan cap and overage

- **Ready (2):** The allowance has been compared with expected peak volume, either last year's BFCM week or, for a first season or a store that has changed a lot, a written forecast: from `peak-load-cover-planner` or the merchant's own method with the working shown.
- **Partial (1):** The cap is known but not compared with expected volume.
- **Missing (0):** The overage price, or what happens at the cap, is not known.
- **Not applicable:** No support tool the store uses has a usage cap or a usage charge: for example Shopify Inbox (listed as free on the Shopify App Store, apps.shopify.com/inbox, checked 24 September 2026) or a plain email inbox. If any tool charges per ticket, conversation, message or resolution, or stops at a limit, the line applies.

**How to check.** Ask what each support tool charges and whether it has a limit. No API exposes this across vendors.

---

## 7. Holiday returns and exchange policy (reported separately)

- **Ready (2):** The holiday return window, who pays return shipping, and what a gift recipient without a receipt can do are all written down.
- **Partial (1):** Some decided, or decided but not published where shoppers and staff can see it.
- **Missing (0):** None decided.

**How to check.** Ask for the returns policy text and whether it says anything about the holiday period.

## 8. Proactive late-delivery notices (reported separately)

Shopify's shipping notifications are shipping confirmation, shipping update, out for delivery and delivered. There is no delayed-delivery notification (help.shopify.com/en/manual/fulfillment/setup/notifications/customer-notifications, checked 24 September 2026).

- **Ready (2):** Written "running late" and "will not arrive in time" messages that state what the store offers, and a named person or routine finds late orders on a schedule.
- **Partial (1):** Only one of those two halves.
- **Missing (0):** Late orders are found when the shopper complains.

**How to check.** Ask for the message text, and who checks shipped orders for delays, how often, using what.

## 9. Contingency plan (reported separately)

Carrier delay, stock-out mid-sale, volume above forecast.

- **Ready (2):** Written for all three, each naming who decides, what shoppers are told, and what staff may offer without asking.
- **Partial (1):** One or two covered, or all three only agreed verbally.
- **Missing (0):** None thought through.

**How to check.** Ask for the plan text, or for each situation "what happens that day, and who decides". Do not fill in a plan.

---

## Scoring

Score = points from lines 1 to 6 that were scored and apply, out of 2 x the number of those lines. Show "x out of y (z%)".

| Score | Band | Meaning |
|---|---|---|
| 83% or more (10 to 12 of 12) | Ready | Keep it that way; keep the weekly review going if line 5 applies |
| 50% to 82% (6 to 9 of 12) | Foundations exist | Set up but untested under load |
| Below 50% (0 to 5 of 12) | Start here | Basics are missing |

With all six lines applying, these are exactly the report's 10 to 12, 6 to 9 and below 6 bands. With lines dropped, possible totals are out of 6, 8 or 10, and none lands between 82% and 83%, so there is no rounding edge case. Examples: 7 out of 8 is 87.5% (Ready); 5 out of 6 is 83.3% (Ready); 8 out of 10 is 80% (Foundations exist); 3 out of 6 is 50% (Foundations exist).

The bands are Chatty's own rubric, not an industry benchmark. The report says so.

If an applicable line of 1 to 6 is Not scored, report "x out of y from the lines scored, n not scored" and give no band.

Report lines 7, 8 and 9 next to the score: "Score: 7 out of 8 (87.5%), Ready. Returns policy: Partial. Late-delivery notices: Missing. Contingency plan: Partial."

## Ranking the fixes

Across all nine lines: critical lines (3, 4, 6) that are Missing first, then lines tied to what broke last season, then Missing before Partial, then critical lines before the rest, then the nearest deadline. The top three are "Fix these three first".

## The critical-line override

Lines 3, 4 and 6 outrank the score. If any is Missing, say so first, whatever the score. A store can score 10 out of 12 and still be one plan-cap surprise away from its assistant going silent in the busiest week. Not applicable never triggers this.
