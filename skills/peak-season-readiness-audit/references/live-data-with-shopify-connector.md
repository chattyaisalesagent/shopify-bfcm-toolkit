# Using a live Shopify connector when one is available

Verified against the official Shopify plugin for ChatGPT documentation (help.shopify.com/en/manual/ai-powered-tools/connecting-ai-tools/shopify-plugin-for-chatgpt) and the Shopify connector for Claude documentation (help.shopify.com/en/manual/ai-powered-tools/connecting-ai-tools/shopify-connector-for-claude), both checked 24 September 2026. Both expose the same action names. This is optional. Nothing in this skill requires it, and most of the time it will not be present.

## How to tell if it's available

Look at what tools this session actually has access to. The official Shopify connector, when connected, exposes actions with these exact names: `get-shop-info`, `search_products`, `get-product`, `list-orders`, `get-order`, `list-customers`, `run-analytics-query`, `get-inventory-levels`, `search_collections`, `graphql_query`, `graphql_schema`, among others. If none of these are present as callable tools in this session, there is no connector, and every line in the audit is scored from what the merchant tells you.

Do not ask the merchant "do you have the Shopify plugin installed" as a substitute for checking. Check the actual tool list.

## What it can confirm for this audit, and what it can't

**Line 1, discount rules.** There is no dedicated action that reads or lists discounts. `search_products` searches the product catalog only (by keyword or by a filter such as price, tag or status) and says nothing about discounts. `create-discount` only creates new percentage-off codes. To read an existing discount, use `graphql_query`, which reads Admin API data for parts of the store with no dedicated action (check the fields with `graphql_schema` first): it can show whether a code exists, its value, minimum, active dates and which discount classes it combines with. It **cannot** confirm the shopper-facing terms text exists or is complete. Use it to confirm the code is real and to compare its setup with the pasted terms, not to confirm the terms are written.

**Line 2, order-by dates.** The connector has no shipping or delivery action at all. It cannot help with this line. Ask the merchant directly, or read their published page.

**Line 3, self-serve order status.** `get-order` shows an order's fulfilment status, so it can show whether recent fulfilled orders carry tracking. That is evidence for half of the line. It does not show that anyone opened the Order status page or tested a chat's order lookup as a shopper would. Ask separately.

**Line 4, handoff.** Nothing in the connector touches conversations or staff permissions. Ask.

**Line 5, weekly review / unanswered messages.** The connector's action list has no conversation, message or inbox data of any kind. It cannot help with this line under any circumstance.

**Line 6, plan cap.** `get-shop-info` returns the store's plan, but that is the Shopify plan, not the support tool's allowance, which is what this line is about. Do not treat a Shopify plan name as an answer to this line, and do not use it to mark the line Not applicable.

**Line 7, returns policy.** Same limit as line 1: the connector can read and write some store data through `graphql_query`/`graphql_mutation` for pages that have no dedicated action, but nothing in its documented action list handles return rules or return-shipping cost specifically. Ask the merchant, or read their published returns page if it can be reached.

**Line 8, late-delivery notices.** `list-orders` and `get-order` can show fulfilment status on an order, which helps the merchant spot late orders by hand, but the connector has no notification templates and no carrier tracking feed. It cannot confirm a late-delivery message exists or gets sent. Ask for the message text.

**Line 9, contingency plan.** A plan is a written decision. `get-inventory-levels` can show which products are low, which is useful context for the stock-out scenario, but nothing in the connector confirms a plan exists. Ask.

## The honest summary

A live connector genuinely helps verify how a discount is set up, through `graphql_query` (part of line 1), and whether fulfilled orders carry tracking (part of line 3). It does nothing to confirm the other seven lines, though inventory and fulfilment data can add context to lines 8 and 9. Do not oversell what "live data" buys here: most of this audit still runs on what the merchant tells you, connector or not, and the report should say exactly which lines, if any, were checked against live data versus self-reported.
