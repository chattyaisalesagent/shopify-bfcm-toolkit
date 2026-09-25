# First step for each line that is not Ready

Every line that is not Ready gets a first step the merchant can do in under 30 minutes in Shopify admin or their own chat or helpdesk app, then the kit tool that finishes the job, if one exists. Not applicable lines get no step.

Shopify admin paths below were checked on help.shopify.com on 24 September 2026: discount combinations (manual/discounts/discount-combinations), store policies (manual/checkout-settings/refund-privacy-tos), tracking numbers and the Order status page (manual/fulfillment/fulfilling-orders/adding-tracking-numbers, manual/fulfillment/setup/order-status-page), Shopify Inbox instant answers (manual/inbox/chat-settings-and-appearance/instant-answers), customer notifications (manual/fulfillment/setup/notifications/customer-notifications).

| Line | First step (under 30 minutes) | Then |
|---|---|---|
| 1. Discount rules | In Shopify admin, Discounts, open each sale code and note its Combinations (product, order, shipping discounts), minimum and active dates. Put them in one short paragraph on the FAQ page and in saved replies. | `campaign-rules-policy-qa`: authoring mode if no text exists, audit mode if it does, cross-check mode if the terms appear in several places |
| 2. Order-by dates per region | For each region, write down the carrier and this year's transit time from the carrier account or its current-year holiday page. | `delivery-cutoff-planner`, then replace every old date with its dates: FAQ, banners, and Settings, Policies, Shipping policy (Shopify links the shipping policy from product pages and the cart) |
| 3. Self-serve order status | Fulfil one real order with a tracking number (typed in at fulfilment, or added by a Shopify Shipping label), open the link in its shipping confirmation email as the shopper would, and check the Order status page shows tracking. If the store has a chat, switch on its order lookup and test the same order. In Shopify Inbox: Sales channels, Inbox, Chat settings, Instant answers, Track my order. | Set up in Shopify and the chat app. No kit tool does this. |
| 4. Handoff to a person | Write down which conversations go to which person (refund requests, address changes, upset shoppers) and set the chat or helpdesk to pass them on with the conversation attached (an assignment rule, a tag, or a handoff trigger, whatever the app calls it). | The mechanics are in the chat or helpdesk app; no kit tool does them. Who may approve what, up to how much: `peak-season-playbook` |
| 5. Weekly review | In the chat app, open the conversations the assistant could not answer or passed on, fix the answers behind the top five, and book the same 30 minutes every week with a named owner. | Set up in the chat app. No kit tool does this. |
| 6. Plan cap and overage | From the helpdesk or chat app's billing page, write down the included allowance, the overage price and what happens at the cap. Send the vendor whatever the page does not answer: "What is our included allowance this billing period? What is the overage price per unit past that? What happens the moment we hit the cap: does the assistant stop, queue to a person, or keep billing? Is there a way to cap spend?" | `peak-load-cover-planner` (daily volume forecast and estimated bill past the cap) |
| 7. Holiday returns policy | In Settings, Policies, Return and refund policy, check whether it states the holiday window, who pays return shipping and what a gift recipient without a receipt can do. Note which of the three is undecided. | `campaign-rules-policy-qa` (post-holiday returns) |
| 8. Late-delivery notices | Shopify sends shipping confirmation, shipping update, out for delivery and delivered emails, but no delayed-delivery email. Name who checks fulfilled orders for late ones, and on which weekday. | Messages: `delivery-cutoff-planner` (its three delivery templates). Finding late orders from November to January: `shipping-exception-watch` |
| 9. Contingency plan | For each situation (carrier delay, stock-out mid-sale, volume above forecast), write down who decides. | `peak-season-playbook` (its three contingency plans). If there is no volume forecast, `peak-load-cover-planner` first |

## How to phrase the chat-app steps

Lines 3, 4 (mechanics) and 5 are done in whatever chat app or helpdesk the store uses, or in Shopify itself for line 3. Say so plainly: "This is set up in your chat or helpdesk app, not in a tool in this kit." Describe what to set up, not which app to use. Do not describe any app as better, do not suggest switching or adding an app, and do not mention Chatty. If the merchant names their app, point to the equivalent setting in that app's own help pages and do not guess its menu names. The Shopify Inbox path above is verified and can be named when the merchant uses Inbox.

## What does not have a tool

Plan cap is the one line where part of the fix cannot be produced by anything in this kit: overage behaviour is vendor-specific and often undocumented, so the honest deliverable is the forecast plus the vendor questions, not a fake automated check.

A merchant reading the report should never think every line has a button to fix it inside this kit. When the step leads to Shopify admin, their chat app or their vendor, the report says so in the same breath as the score.
