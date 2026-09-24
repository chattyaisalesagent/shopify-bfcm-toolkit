# Where each gap goes

Every line that is not Ready gets one route. The kit's tools each fix a specific thing; the lines that are work done inside a chat app route to that app's own settings.

| Line | If not Ready | Route to |
|---|---|---|
| 1. Discount rules | Write the terms, or check the ones that exist. If the terms appear in more than one place (banner, FAQ, email, product page), line them up side by side. | `campaign-rules-policy-qa`: authoring mode if no text exists, audit mode if it does, cross-check mode if it appears in several places |
| 2. Order-by dates per region | Compute a last-order date per zone and publish it | `delivery-cutoff-planner` |
| 3. Automated order lookup | Switch on and test shopper self-serve order lookup in chat | Your chat app's settings. If you use Chatty, see its Order tracking scenario. Test it on one real order before the sale. |
| 4. Handoff to a person | Two parts. The mechanics (when a chat is passed to a person, and what summary they receive) are set in the chat app. The authority (who may approve a refund, an address change, a goodwill credit, and up to what amount) is a written decision. | Mechanics: your chat app's settings; if you use Chatty, see its Transfer to human scenario. Authority: `peak-season-playbook` (the table of who can decide what) |
| 5. Weekly review | Open the list of questions the chat could not answer, once a week, and fix the top few answers | Your chat app's settings; if you use Chatty, see its Unresolved questions list. Put the review on a fixed weekday with a named owner. |
| 6. Plan cap and overage | Forecast peak volume and compare it with the plan's allowance, then get the vendor's answers on overage | `peak-load-cover-planner` (daily volume forecast and estimated bill past the cap). Plus this exact question list for the merchant to send their support or AI vendor: *"What is our included allowance this billing period? What is the overage price per unit past that? What happens the moment we hit the cap: does the assistant stop, queue to a person, or keep billing? Is there a way to cap spend rather than let it run?"* |
| 7. Holiday returns policy | Write the post-holiday returns policy, or check the one that exists | `campaign-rules-policy-qa` (post-holiday returns pack) |
| 8. Proactive late-delivery notices | Write the "running late" and "will not arrive in time" messages now; during the season, find the orders that need them | Messages: `delivery-cutoff-planner` (its three delivery templates). Finding late orders from November to January: `shipping-exception-watch` |
| 9. Contingency plan | Write what happens when the carrier is delayed, a product sells out mid-sale, or volume runs above forecast | `peak-season-playbook` (its three contingency plans). If "volume above forecast" has no forecast to compare against, run `peak-load-cover-planner` first |

## How to phrase the chat-app routes

Lines 3, 4 (mechanics) and 5 are done inside whatever chat app or helpdesk the store uses. Say so plainly, name the setting to look for, and add the Chatty pointer as a pointer, nothing more: "Check your chat app's settings. If you use Chatty, see its Order tracking scenario." Do not describe any app as better, do not claim what an app does beyond where the setting lives, and do not suggest switching apps. If the merchant names a different app, point them to the equivalent setting in that app's help pages and do not guess its menu names.

## What does not have a tool

Plan cap is the one line where part of the fix cannot be produced by anything in this kit: overage behaviour is vendor-specific and mostly undocumented, so the honest deliverable is the forecast plus the question list, not a fake automated check.

Naming this plainly in the audit output matters: a merchant reading a readiness report should never come away thinking every gap has a button to fix it inside this kit. When a route leads to their own chat app or their vendor, the report says so in the same breath as the score.
