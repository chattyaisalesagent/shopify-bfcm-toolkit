# Using a live Shopify connector when one is available

Verified against the official Shopify plugin for ChatGPT documentation (help.shopify.com/en/manual/ai-powered-tools/connecting-ai-tools/shopify-plugin-for-chatgpt), checked 21 September 2026. This is optional. Nothing in this skill requires it, and most of the time it will not be present.

## How to tell if it's available

Look at what tools this session actually has access to. The official Shopify connector, when connected, exposes actions with these exact names: `get-shop-info`, `search_products`, `get-product`, `list-orders`, `get-order`, `list-customers`, `run-analytics-query`, `get-inventory-levels`, `search_collections`, among others. If none of these are present as callable tools in this session, there is no connector, and every line in the audit is scored from what the merchant tells you.

Do not ask the merchant "do you have the Shopify plugin installed" as a substitute for checking. Check the actual tool list.

## What it can confirm for this audit, and what it can't

**Line 1, discount rules.** `search_products` or a discount lookup can confirm a discount code exists and what its mechanics are (percentage, minimum purchase, start date). It **cannot** confirm the shopper-facing terms text exists or is complete, because the connector's own `create-discount` action only configures the code; it does not write or store an explanation of stacking, eligibility or the free-shipping order. Use it to confirm the code is real, not to confirm the terms are written.

**Line 2, order-by dates.** The connector has no shipping or delivery action at all. It cannot help with this line. Ask the merchant directly, or read their published page.

**Line 3, order lookup.** `get-order` and `list-orders` confirm order data is reachable through the connector, which is a different thing from confirming the *shopper-facing* self-serve lookup in the store's chat app works. Do not conflate the two.

**Line 4, handoff.** Nothing in the connector touches conversations or staff permissions. Ask.

**Line 5, weekly review / unanswered messages.** The connector's action list has no conversation, message or inbox data of any kind. It cannot help with this line under any circumstance.

**Line 6, plan cap.** `get-shop-info` returns the store's plan, but that is the Shopify plan, not the AI or support system's message allowance, which is what this line is actually about. Do not treat a Shopify plan name as an answer to this line.

**Line 7, returns policy.** Same limit as line 1: the connector can read and write some store data through `graphql_query`/`graphql_mutation` for pages that have no dedicated action, but nothing in its documented action list handles return rules or return-shipping cost specifically. Ask the merchant, or read their published returns page if it can be reached.

**Line 8, late-delivery notices.** `list-orders` and `get-order` can show fulfilment status on an order, which helps the merchant spot late orders by hand, but the connector has no notification templates and no carrier tracking feed. It cannot confirm a late-delivery message exists or gets sent. Ask for the message text.

**Line 9, contingency plan.** A plan is a written decision. `get-inventory-levels` can show which products are low, which is useful context for the stock-out scenario, but nothing in the connector confirms a plan exists. Ask.

## The honest summary

A live connector genuinely helps verify that a discount code exists (part of line 1) and that order data is reachable (part of line 3). It does nothing to confirm the other seven lines, though inventory and fulfilment data can add context to lines 8 and 9. Do not oversell what "live data" buys here: most of this audit still runs on what the merchant tells you, connector or not, and the report should say exactly which lines, if any, were checked against live data versus self-reported.
