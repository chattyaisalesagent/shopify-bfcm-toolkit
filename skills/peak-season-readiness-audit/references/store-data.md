# Getting the store's own data

The merchant owns the store, so the audit reads the store before it asks anything. Two routes: a connected store, or Shopify admin exports. Read only, always.

Checked against help.shopify.com and shopify.dev (Admin GraphQL 2026-07) on 30 September 2026. Not yet run against a live store end to end: treat a query that errors as a schema change, say so, and fall back to exports for that line.

## Route A. A connected store

**How to tell.** Look at the tools this session actually has.
- Shopify connector for Claude, or the Shopify plugin for ChatGPT: actions named `get-shop-info`, `list-orders`, `get-order`, `run-analytics-query`, `graphql_query`, among others. In Claude Code, connectors added on claude.ai are available automatically when Claude Code is logged in with that claude.ai account.
- Shopify CLI in Claude Code: `shopify version` works (3.93.0 or later) and the merchant has run `shopify store auth` for the store. Queries run with `shopify store execute`, which is read-only unless `--allow-mutations` is passed. Never pass it.

Do not ask "is Shopify connected?" as a substitute for checking.

**If nothing is connected**, give the merchant the setup in two lines, then wait:
- Claude app or claude.ai: connect Shopify from the Shopify connector for Claude install page (help.shopify.com, "Shopify connector for Claude").
- Claude Code: install Shopify CLI, then run
  `shopify store auth --store <store>.myshopify.com --scopes read_legal_policies,read_discounts,read_orders,read_all_orders,read_content,read_shipping,read_reports`
  and approve in the browser. Without `read_all_orders` only the last 60 days of orders are visible, so last season comes from analytics or an export instead.
Or skip connecting and use Route B.

**What to read.** Run each query once with `graphql_query` or `shopify store execute --query-file <file> --json`. Page through orders with `pageInfo`.

```graphql
# 1. Store, policies (read_legal_policies)
{ shop { name currencyCode ianaTimezone shipsToCountries
  shopPolicies { type title body url updatedAt } } }
```

```graphql
# 2. Discounts that are live or scheduled (read_discounts). `summary` is one readable line per discount.
{ discountNodes(first: 50, query: "status:active,scheduled") { nodes { discount {
  __typename
  ... on DiscountCodeBasic { title status summary startsAt endsAt codes(first: 5) { nodes { code } }
    combinesWith { orderDiscounts productDiscounts shippingDiscounts }
    minimumRequirement { ... on DiscountMinimumSubtotal { greaterThanOrEqualToSubtotal { amount currencyCode } }
                         ... on DiscountMinimumQuantity { greaterThanOrEqualToQuantity } } }
  ... on DiscountAutomaticBasic { title status summary startsAt endsAt combinesWith { orderDiscounts productDiscounts shippingDiscounts } }
  ... on DiscountCodeFreeShipping { title status summary startsAt endsAt codes(first: 5) { nodes { code } } }
  ... on DiscountAutomaticFreeShipping { title status summary startsAt endsAt }
  ... on DiscountCodeBxgy { title status summary startsAt endsAt codes(first: 5) { nodes { code } } }
  ... on DiscountAutomaticBxgy { title status summary startsAt endsAt }
} } } }
```

```graphql
# 3. Online store pages: FAQ, shipping, sale pages (read_content or read_online_store_pages)
{ pages(first: 50) { nodes { title handle body isPublished updatedAt } } }
```

```graphql
# 4. Recent orders with fulfilment and tracking (read_orders; last 60 days).
# Filter on processed_at, the date the order was placed. Orders imported from another platform
# carry today's createdAt, so created_at would count years of history as "recent".
{ orders(first: 100, sortKey: PROCESSED_AT, reverse: true, query: "processed_at:>=<60 days ago>") { nodes {
  name processedAt displayFulfillmentStatus requiresShipping discountCodes
  shippingAddress { countryCodeV2 }
  fulfillments { createdAt displayStatus estimatedDeliveryAt deliveredAt trackingInfo { number company } }
} pageInfo { hasNextPage endCursor } } }
```

```graphql
# 5. Last season's orders per day (read_reports). SINCE and UNTIL are inclusive, dates unquoted.
{ shopifyqlQuery(query: "FROM sales SHOW orders TIMESERIES day SINCE 2025-11-15 UNTIL 2026-01-15") {
  tableData { columns { name } rows } parseErrors } }
```

```graphql
# 6. Shipping rates, for free-shipping thresholds (read_shipping). A free rate shows as price 0 with a TOTAL_PRICE condition.
{ deliveryProfiles(first: 5) { nodes { name profileLocationGroups { locationGroupZones(first: 50) { nodes {
  zone { name }
  methodDefinitions(first: 20) { nodes { name active
    rateProvider { ... on DeliveryRateDefinition { price { amount currencyCode } } }
    methodConditions { field operator conditionCriteria { ... on MoneyV2 { amount } } } } } } } } } } }
```

Never print customer names, emails, phones or addresses in the report. Order names (#1234) are enough.

## Route B. Exports from Shopify admin

Tell the merchant exactly this, then wait for the files in the working folder (Claude Code) or as uploads (Claude app, code execution on):
1. **Orders:** Orders, Export, choose "Orders by date" from last November 1 to today, CSV for Excel. Over 50 orders arrive by email.
2. **Discounts:** Discounts, Export.
3. **Policies:** Shopify has no policy export. Copy the text from Settings, Policies (returns and shipping), plus any FAQ or shipping page, into a text file or paste it.
4. Optional: a chat or helpdesk export of last November to January. Any CSV with the message text works.

Run `python3 scripts/orders_summary.py <orders.csv>` and read its JSON. Read the discounts export as it comes; its columns are not documented, so quote what is there and do not assume a column exists.

The orders export has no tracking numbers, carriers or delivery status. Line 3 and line 8 can use fulfilment timing from it, but tracking coverage needs Route A or the merchant's answer.

## What store data can show, line by line

| Line | Connected store | Exports | Still asked |
|---|---|---|---|
| 1 Discount rules | Each live discount's summary, dates, minimum, combinations; compared with the sale text on pages and policies. Wording that differs between places is at most Partial | Discounts export, codes used per order and orders that stacked codes; sale text pasted | Whether staff and any assistant can read the terms |
| 2 Order-by dates per region | Countries shipped to (`shipsToCountries`, orders by country); any published cutoff in pages or the shipping policy | Regions from `orders_summary.py`; cutoff text pasted | Nothing, if the pages were read |
| 3 Self-serve order status | Share of fulfilled orders with a tracking number; `requiresShipping` decides Not applicable | Ships goods or not; days to fulfil. No tracking data | Whether anyone tested the Order status page and any chat order lookup this season |
| 4 Handoff to a person | Nothing | Nothing | Who takes it, what they see, what they may approve |
| 5 Weekly review | Nothing | A chat export shows whether an assistant replied | Whether an assistant replies alone, and when its unanswered list was last opened |
| 6 Plan cap | Last season's orders per day, as the volume baseline | Same, from `seasons` in the summary | The support tool's allowance, overage price, what happens at the cap |
| 7 Holiday returns | Refund policy text: holiday window, who pays return shipping, gifts without a receipt | Pasted policy text | Nothing, if the policy was read |
| 8 Late-delivery notices | Fulfilled orders past `estimatedDeliveryAt` without `deliveredAt`: how many shoppers were waiting | Days to fulfil, orders stuck unfulfilled; refunds and cancellations in season | The message text, and who checks for late orders |
| 9 Contingency plan | Nothing | Nothing | The plan, or who decides each situation |

Lines 4, 5 and 9, and the cap in line 6, live in decisions and vendor contracts, not in the store. They stay questions. Say so rather than stretching the data to cover them.
