# Skill opportunity assessment

Which peak-season merchant workflows, if any, deserve to be reusable skills.

**Inputs:** `docs/ebook-to-product-mapping.md` for the research, `docs/platform-compatibility.md` for the packaging constraints, plus a capability sweep of Shopify, Shopify Sidekick, Shopify Inbox, Shopify Knowledge Base, Gorgias, Zendesk, Intercom and Tidio, all URLs checked 21 September 2026.

**Status:** recommendation only. No `SKILL.md`, manifest or scaffold exists.

---

## 1. The finding that reframes the product

Shopify publishes a real BFCM checklist: 25 steps in three phases at https://www.shopify.com/blog/bfcm-checklist. It already tells merchants to state discount terms clearly, to consider extending the returns window for the holidays, to prepare support for the volume, and to update the FAQ page with current shipping windows, return policies and sale terms.

It is undated prose. It has no per-region cutoffs, no milestones, and it produces nothing.

> **Do not build another checklist. Build the artifacts Shopify's checklist tells merchants to produce and then does not produce for them.**

That single sentence removes one candidate from this assessment and sharpens the rest. Everything below is judged on whether it produces a usable artifact that nothing else produces.

---

## 2. Grouping and elimination

Eleven merchant jobs came out of the mapping. Applying the brief's filters in order:

**Removed as adequately served.** Order lookup and handoff. This is a 2026 commodity: Shopify Inbox lists order lookups and carries AI context to staff on handoff; Gorgias authenticates by one-time code and can cancel orders, edit addresses and reship; Zendesk ships 16 Shopify actions; Intercom and Tidio both return order status. Guest WISMO is already solved outside chat by the order status page and Track with Shop. "Handoff with context" is not a differentiator, because transcript carry-over is universal. **Rejected.**

**Removed as redundant.** A readiness checklist, for the reason in section 1. The scoring and routing idea survives only as an entry point inside the product, not as a thing worth building on its own.

**Removed as a generic writing prompt.** Industry priority order. It is a lookup with four branches.

**Merged.** Volume projection and plan-cap verification are one question, not two: can this store's peak load get through its plan without a surprise bill or a silent shutdown. Seasonal intent data and phase deadlines are reference material consumed by other skills, not skills.

**Survivors: five candidates.**

---

## 3. The five candidates

### S1. Sale terms and holiday policy writer

- **Name.** `sale-terms-writer`
- **User.** The person who runs the promotion. Often the owner in a small store, a marketing or ops lead in a larger one.
- **Trigger.** "Write our BFCM discount terms", "what do we tell customers about stacking codes", "extend our returns policy for the holidays".
- **Job to be done.** Decide, record and publish the shopper-facing rules for this sale and this holiday season, in one text that a product page, a policy page, a staff macro and any AI assistant can all use.
- **Required inputs.** Merchant answers only. Whether codes stack with automatic discounts, eligibility of already-reduced items, returnability of discounted items, free-shipping threshold order, start and end times with timezone, product and region exclusions, gift exchange handling, the holiday returns window, who pays return shipping, restocking fees, and how a gift without a receipt is handled.
- **Workflow.** Elicit each field, one at a time, refusing to guess. Flag conflicts between answers. Emit the approved text in three registers: a shopper-facing terms block, short FAQ answers, and a staff-facing decision table. Then warn where the merchant's platform cannot express what they just decided.
- **Outputs.** `sale-terms.md`, `holiday-returns.md`, `faq-answers.md`, and a `platform-limits.md` listing the decisions their platform cannot enforce.
- **Merchant decisions that cannot be automated.** Every field. The skill's job is to ask well and record faithfully.
- **Existing alternatives.** Shopify configures the mechanics completely: combines-with settings per discount class, a cap of five product or order codes plus one shipping code, active dates resolved in the store's admin timezone, free-shipping thresholds counted at the discounted price, final-sale flags in return rules. Sidekick generates blog posts, product descriptions, images, marketing copy, segments, discount codes and Flow automations. Shopify's policy generator offers six templates: return, privacy, terms of service, shipping, legal notice, subscription.
- **Differentiation.** **There is no discount-terms or sale-terms page type among those six templates.** Policy text is absent from Sidekick's documented content list. The Knowledge Base app's auto-generated facts draw on language, customer-account, shipping and return-rule settings, and not on discounts. Checkout tells the shopper only "Some discount codes couldn't be used together", never why or which combination would work. Shopify holds every input in structured form and publishes none of it as prose. Against a generic assistant, the difference is the fixed field list, the refusal to invent an answer the merchant has not given, and the platform-limits warning.
- **Without MCP.** Fully. Nothing but merchant answers.
- **Without live Shopify data.** The merchant states their settings rather than the skill reading them. Friction is low, because a person who is deciding these rules is looking at the discount screen anyway. A future integration could pre-fill and, more usefully, detect a contradiction between the published text and the live configuration.
- **Evaluation.** `claude plugin eval`, two arms. Case: "help me write our BFCM discount terms". Graders: `tool_used` that the skill fired, `file_exists` for the artifact, and an `llm` rubric scoring field coverage against the fixed list and penalising any invented merchant fact. The without-plugin arm should lose on coverage and on invention.
- **Recommendation: include. First vertical slice.**

### S2. Delivery cutoff planner

- **Name.** `delivery-cutoff-planner`
- **User.** Whoever owns fulfilment.
- **Trigger.** "When do customers have to order to get it before Christmas", "we need a message for late deliveries".
- **Job.** Back-solve a per-region last-order date from carrier transit times, the store's own processing time and a chosen buffer, publish it, and write the messages for the days it does not hold.
- **Inputs.** Shipping zones, carrier transit estimates per zone, own processing time, non-working days, the target arrival date, and the buffer the merchant is willing to promise.
- **Workflow.** Working-day arithmetic per zone, deterministic and reproducible. Then three templates: dispatched, running late, will not arrive before the holiday.
- **Outputs.** A per-zone cutoff table, publishable copy, and the three templates.
- **Cannot be automated.** The buffer. It is a promise the merchant has to keep, and it is the whole risk of the exercise.
- **Existing alternatives.** Shopify's automated delivery dates predict from the store's own fulfilment history but render only when the prediction is within five days in the US or four in the EU, and only when origin and destination are in the same region. Manual delivery dates are a **single global setting with a hard, non-configurable noon origin-local cutoff**. Shop Promise renders a real countdown but is US-domestic only, invite-assessed, and described by Shopify as the top 1% of shippers. The Delivery Promise API carrying cutoff times is restricted to approved partners. Shopify publishes carrier deadlines as a blog post.
- **Differentiation.** Nothing back-solves a target date into per-zone last-order dates for an ordinary merchant. Two sub-gaps are unambiguous. Shopify's built-in customer notifications are exactly order confirmation, cancelled, refund, shipping confirmation, shipping update, out for delivery and delivered: **there is no delayed-delivery template at all.** And Shopify's own carrier-deadline post was still the December 2025 edition when checked on 21 September 2026, so merchants have no current-year source from the platform.
- **Without MCP.** Yes, with merchant-supplied carrier dates.
- **Without live data.** The carrier deadlines are the weak point. The skill must ask for them rather than assert them, because publishing a wrong cutoff is worse than publishing none.
- **Evaluation.** A fixture with three zones and known answers. `file_exists` for the table, a `regex` or script check that the computed dates match the fixture exactly, and an `llm` rubric on the late-delivery template. Date arithmetic is either right or wrong, which makes this the easiest of the five to validate.
- **Recommendation: include. Second slice.**

### S3. Support load and cap check

- **Name.** `peak-load-check`
- **User.** Whoever owns the support budget.
- **Trigger.** "Will our plan survive BFCM", "how many conversations should we expect".
- **Job.** Project this store's peak load from its own history and join it to its own plan limit and overage price.
- **Inputs.** A volume export or counts by week, the plan's included allowance, the overage price, and the documented behaviour at the cap.
- **Workflow.** Percentile arithmetic on the store's own history, presented as a range. The platform figure of 62% is never a default. Then a vendor question list for the things no API exposes: what happens at the cap, who receives the questions, is there a spend ceiling.
- **Outputs.** A projection with a range, a cost exposure estimate, and the question list to send the vendor.
- **Cannot be automated.** The risk appetite, and every answer that has to come from the vendor.
- **Existing alternatives.** Zendesk Explore has genuine seasonal forecasting, Holt-Winters, needing at least two cycles. Zendesk WFM forecasts inbound volume up to a year out. Zendesk's resolution usage Forecast tab shows current average daily use, projected use by renewal and when the limit is reached. Intercom's WFM forecasting is early access and framed as headcount.
- **Differentiation.** **No tool joins a seasonal forecast of the store's own volume to that store's AI plan limit and overage price.** Zendesk owns both halves in one product and has never joined them: the seasonal model is wired to ticket counts, while the Forecast tab that watches the allowance is a short moving average with no seasonality, so it will tell a merchant on 1 November that they are fine because October was quiet. Gorgias has nothing in-product and its own BFCM article sends merchants to compute it by hand in a third-party spreadsheet. Tidio returns zero hits across its help centre. Shopify has no conversation history to forecast from. The exposure is real and specific: on Gorgias Basic, 300 tickets include only 30 AI interactions, overage runs above the in-plan rate, and an AI resolution that does not hand over burns both meters.
- **Without MCP.** Yes, from an export or from counts.
- **Without live data.** This is the candidate most weakened. A merchant on Shopify Inbox has no conversation history to project from at all, and Shopify Inbox reports only assisted sessions, assisted orders, satisfaction and response time.
- **Evaluation.** A fixture history with known percentiles, checked numerically, plus a rubric that fails any output presenting a single number without a range.
- **Recommendation: defer to v2.** Real gap, verified and sharp, but it depends on an export that the most Shopify-native merchant does not have.

### S4. Conversation gap triage

- **Name.** `conversation-gap-triage`
- **User.** Whoever runs the weekly review.
- **Trigger.** "What should we write next", a weekly cadence during the season.
- **Job.** Sort an export of unresolved or fallback conversations into needs content, needs an action or workflow, needs context, needs a handoff, needs nothing, and keep the counts comparable week to week.
- **Inputs.** A CSV export from any helpdesk, inbox or fallback log.
- **Workflow.** Deterministic classification first so that the numbers are stable across runs, model judgement only on what the rules cannot decide, then counts by subject and by gap type, compared against the previous week.
- **Outputs.** A classified CSV, counts by type, and a shortlist of what to write next.
- **Cannot be automated.** Edge cases, and the decision about what to fix first.
- **Existing alternatives, and this is where the whitespace narrowed.** **Intercom's Fin Recommendations already names three of the five buckets correctly:** content gap, customer data gap described as needing information from an external system such as order status, and action gap described as needing to take an action in another system. Gorgias Opportunities has two content-flavoured types and does export the underlying tickets to CSV. Zendesk exports CSV and reports outcomes. Tidio lists unanswered questions with intent and occurrence counts, but for live chat only, not email.
- **Differentiation.** Narrower than the research alone suggested, but real. **No vendor has a needs-a-handoff type and none has a needs-nothing type.** Intercom removed its ambiguity bucket deliberately. Gorgias knows why it escalated and discards the reason, keeping only a tag and an outcome. Intercom's taxonomy, the only correct one, sits behind a paid add-on and has no documented export, so it cannot be compared across seasons or carried between vendors. And a cross-vendor triage that works on any CSV is something no vendor has an incentive to build.
- **Without MCP.** Yes, from a CSV.
- **Without live data.** **The blocking problem: Shopify Inbox has no conversation export at all**, in the UI or the API, and no unanswered metric. The merchant closest to Shopify is exactly the merchant who cannot run this skill.
- **Privacy.** The highest risk of the five by a distance. Conversation exports carry shopper emails, names, phone numbers and order numbers. Any version of this must strip or refuse to echo personal data, and must say plainly what leaves the merchant's machine.
- **Evaluation.** A labelled fixture of a few hundred rows with a known distribution, scored on classification agreement, plus a rerun check that the same input produces the same counts.
- **Recommendation: defer to v2.** The weekly cadence is the strongest argument in the research, and the privacy work and the export gap are the strongest arguments against shipping it first.

### S5. Paraphrase test-set builder

- **Name.** `paraphrase-test-builder`
- **User.** Whoever owns the assistant or the help content.
- **Trigger.** "Does our assistant handle this question asked differently".
- **Job.** Turn one intent into a graded test set the merchant can actually run in the tool they already have.
- **Inputs.** The intent, the approved answer, and the tool the merchant uses.
- **Workflow.** Generate realistic rephrasings including the ungrammatical and multilingual ones, produce an expected-answer key and a pass or fail rubric, and export in the shape the merchant's tool ingests.
- **Outputs.** A test-set CSV, an answer key, a grading sheet.
- **Cannot be automated.** Judging the answers, unless the tool grades them.
- **Existing alternatives.** Intercom's Batch test is the only bulk tool: questions from past conversations, manual entry, **or CSV upload**, capped at 50 per group. Fin Simulations grade pass or fail but only for workflow procedures. Gorgias, Tidio's Lyro Playground, Zendesk's test widget and Shopify's Knowledge Base test box are all one question at a time.
- **Differentiation.** Intercom states outright that none of its tools generate paraphrased variations, and Zendesk's own best-practice doc instructs humans to ask the same question in different ways, which is shipping the chore rather than the feature. **The gap is precisely the generation step, and Intercom's batch test accepts CSV upload, so a skill that produces the CSV plugs straight into a tool that already exists and cannot make its own input.** That is unusually clean: no integration needed, and the artifact has an immediate home.
- **Without MCP.** Yes.
- **Without live data.** It cannot run the test or grade it. It produces the input and the rubric.
- **Evaluation.** A rubric on variation quality, checking that variations preserve the intent and cover ungrammatical, abbreviated and multilingual forms, plus a format check against the target tool's import shape.
- **Recommendation: defer, but flag.** The most surprising result of the research, and the cheapest of the five to build. It is deferred only because it serves a narrower user than S1 and S2 and because the research behind it is the weakest claim in the ebook. It should be reconsidered immediately after the first slice.

---

## 4. Ranking

Scored 1 to 5, higher is better, except cost where higher means cheaper.

| | S1 sale terms | S2 delivery cutoff | S3 load and cap | S4 triage | S5 paraphrase |
|---|---|---|---|---|---|
| Problem frequency | 4 once per sale, several per year | 3 once per season | 2 once per season | **5 weekly** | 3 per intent |
| Merchant value | **5** | **5** | 4 | 4 | 3 |
| Differentiation | **5** verified cleanest gap | **5** no delayed template exists | 4 sharp but narrow | 2 Intercom names three of five | 4 generation step is absent |
| Works without MCP | **5** | 4 needs carrier dates | 3 needs an export | 2 Shopify Inbox cannot export | **5** |
| Ease of validation | 3 rubric-based | **5** arithmetic is right or wrong | 4 numeric | 3 needs a labelled fixture | 2 quality is subjective |
| Privacy risk, inverted | **5** none | **5** none | 4 volumes only | **1 shopper PII** | **5** none |
| Implementation cost, inverted | 4 | 3 date arithmetic and fixtures | 3 | 2 classifier and fixtures | **5** |
| **Total** | **31** | **30** | **24** | **19** | **27** |

S4 ranks lowest despite having the best frequency argument in the research. That is the honest result: the weekly cadence is real, and it is outweighed by a narrowed gap, a hard export blocker on the most Shopify-native stack, and the only serious privacy exposure in the set.

---

## 5. MCP decision

| Workflow | Doable from answers and files | Needs live data | Manual friction | Does MCP materially improve it | Defer MCP |
|---|---|---|---|---|---|
| S1 sale terms | Everything | Nothing | Low. The merchant is looking at the discount screen anyway | Only for a genuinely new capability: detecting where published text contradicts live configuration | Yes |
| S2 delivery cutoff | Zones, processing time, buffer | Carrier deadlines, and they change yearly | Medium. Transit times must be gathered | Convenience only, unless it reads live shipping profiles | Yes |
| S3 load and cap | Counts, allowance, price | Volume history, cap behaviour | High if no export exists | Yes for history, but cap behaviour is undocumented by vendors and no API exposes it | Yes |
| S4 triage | Classification of a supplied CSV | The export itself | High, and impossible on Shopify Inbox | It would solve the export blocker, which is the main objection | No. Reconsider with the skill |
| S5 paraphrase | Everything except running the test | Running and grading | Low | Yes, it would close the loop, but the tools that could run it are per-vendor | Yes |

**Conclusion: no MCP in the MVP.** Both recommended skills complete their job from merchant answers alone. MCP earns its place only where it adds a capability rather than convenience, and the clearest such case, contradiction detection between published terms and live configuration, is a v2 idea that should follow evidence of repeated use.

---

## 6. Should this be built at all

The brief allows the answer to be no. It is not no, but the argument against deserves stating.

**Against.** Shopify's checklist already names the work. Sidekick already writes content. A capable assistant with a good prompt can draft discount terms today. The whole product could be a well-written document.

**For.** Three gaps were verified against primary documentation rather than asserted. There is no discount-terms page type among Shopify's six policy templates and policy text is absent from Sidekick's documented output. There is no delayed-delivery notification template in Shopify at all, and the platform's own carrier-deadline post was nine months stale when checked. And no tool joins a seasonal volume forecast to a plan's cap and overage price, in a market where one vendor's entry plan includes thirty AI interactions and bills two meters per resolution.

**The honest test.** `claude plugin eval` runs a with-plugin and a without-plugin arm and reports the delta. If S1 cannot beat a plain request to the same model on field coverage and on refusing to invent merchant facts, then S1 is documentation and should ship as documentation. **That measurement should gate the MVP, not follow it.** Write the eval cases before the skill.

---

## 7. Recommended MVP

**Two skills, no MCP, no scorecard, no checklist.**

1. `sale-terms-writer`, built first, evaluated before anything else is written.
2. `delivery-cutoff-planner`, built second, with the delayed-delivery template as its sharpest single piece.

Both produce an artifact on the day they run, both work for every Shopify merchant regardless of which support tool they use, both need nothing exported and nothing connected, and both fill a gap verified against Shopify's own documentation.

**Positioning.** Not a readiness checker. The thing that produces what the checklist asks for.

**Deferred with reasons recorded:** S3 load and cap, S4 triage, S5 paraphrase builder.
**Rejected:** order lookup and handoff, a readiness checklist, a generic dated plan, industry priority lookup.

---

## 8. Open questions

1. Does S1 beat the no-plugin arm? If not, the product is a document. This is answerable before writing the skill.
2. Where do carrier deadlines come from each year, given that Shopify's own post goes stale? Ask the merchant, curate a source, or state the limitation.
3. Is the deferral of S4 permanent? Its weekly frequency is the strongest usage argument in the whole research, and it fails on export access and privacy rather than on value.
4. Does an artifact-producing skill even need a plugin, or would two standalone skills distribute better? A plugin buys namespacing and one install; two skills are simpler to publish.
5. Several Shopify negatives rest on documentation silence rather than an explicit statement. Sidekick is the one worth re-checking before launch, since it is the fastest-moving of them.

---

## 9. Sources for the load-bearing claims

All checked 21 September 2026. These are the claims an MVP decision rests on, so each carries its primary source. Vendor help centres mostly render no last-updated date; where one exists it is noted.

**Shopify already does this**
- BFCM checklist, 25 steps in three phases: https://www.shopify.com/blog/bfcm-checklist
- Policy generator, six templates and no sale-terms type: https://help.shopify.com/en/manual/checkout-settings/refund-privacy-tos
- Sidekick documented output: https://help.shopify.com/en/manual/shopify-admin/productivity-tools/sidekick/generate-content
- Discount combinations and the five-plus-one code cap: https://help.shopify.com/en/manual/discounts/discount-combinations
- Return rules: window, return-shipping cost, restocking fee, final sale: https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/return-rules
- Self-serve returns, which exclude exchanges and require an account: https://help.shopify.com/en/manual/fulfillment/managing-orders/returns/self-serve-returns/setup
- Manual delivery dates, a single global setting with a hard noon origin-local cutoff: https://help.shopify.com/en/manual/fulfillment/setup/delivery-expectations/manual-delivery-dates
- Shop Promise eligibility, US-domestic and top 1% of shippers: https://help.shopify.com/en/manual/fulfillment/setup/shop-promise/eligibility
- The complete customer notification list, containing no delayed-delivery template: https://help.shopify.com/en/manual/fulfillment/setup/notifications/customer-notifications
- Carrier deadlines published as a blog post, still the December 2025 edition when checked: https://www.shopify.com/blog/holiday-shipping-deadlines
- Shopify Inbox reporting, four metrics and no unanswered measure: https://help.shopify.com/en/manual/inbox/conversations
- Inbox agent order lookups, requiring sign-in: https://help.shopify.com/en/manual/inbox/assigning-your-ai-staff-member
- Knowledge Base app query log, answered and unanswered only: https://help.shopify.com/en/manual/promoting-marketing/knowledge-base/understanding-faq-metrics

**Helpdesk vendors**
- Intercom Fin Recommendations, the three named gap types, article dated 14 May 2026: https://www.intercom.com/help/en/articles/11390088-optimize-fin-instantly-with-the-help-of-ai
- The Pro add-on gate, $99/mo for 1,000 conversations: https://www.intercom.com/help/en/articles/13868265-pro-add-on
- Intercom Batch test, CSV upload and a 50-question cap: https://www.intercom.com/help/en/articles/10521711-batch-test-fin-ai-agent
- Intercom stating it does not generate paraphrases: https://www.intercom.com/help/en/articles/14077180-simulations-vs-batch-tests-vs-previews
- Gorgias Opportunities, two knowledge-flavoured types with CSV export: https://docs.gorgias.com/en-US/continuously-improve-ai-agent-with-opportunities-(beta)-4858461
- Gorgias billing, both meters charged when the AI resolves without handover: https://docs.gorgias.com/en-US/how-youre-billed-for-using-gorgias-199385
- Gorgias pricing, Basic at 300 tickets and 30 AI interactions with $1.50 overage against an in-plan rate of $0.85 to $1.00: https://www.gorgias.com/pricing
- Zendesk resolution usage Forecast tab, a 7 to 30 day moving average with 80% and 100% warnings: https://support.zendesk.com/hc/en-us/articles/8922391373978
- Zendesk Explore seasonal forecasting, Holt-Winters, needing at least two cycles: https://support.zendesk.com/hc/en-us/articles/4408832082970
- Zendesk AI agent outcome reporting, effective 18 May 2026, naming outcomes and not reasons: https://support.zendesk.com/hc/en-us/articles/10677925692698
- Tidio Lyro Suggestions, live chat only and not available for tickets: https://help.tidio.com/hc/en-us/articles/24182486548892-Lyro-Suggestions

**Corrections to common assumptions, worth recording**
- Shopify Inbox was not folded into Sidekick. It survives and was repositioned in Spring '26. What was sunset is the Shop app's buyer-to-merchant inbox, 19 February 2025: https://changelog.shopify.com/posts/sunsetting-shop-inbox-on-shop-app
- There is no Summer '26 Edition. The latest are Winter '26 and Spring '26, 17 June 2026. Third-party posts calling Spring '26 "Summer 2026" are wrong.
- Salesforce signed a definitive agreement to acquire Intercom, now named Fin, on 15 June 2026. Signed, not closed. Any pricing claim about Fin has a shelf life.

**Why the remaining order-lookup slice still does not become a skill.** The one defensible gap there is guest order lookup in chat: Shopify's Inbox agent requires sign-in, while Shopify's own 2020 Shopify Chat did email plus order number. Closing it needs live order data and an identity check, which is an app or an integration, not packaged instructions. It stays rejected for this product.

**Claims deliberately not made.** Peak-season volume multipliers circulating as "2 to 4 times" or "80% higher" come from vendor blogs, not from Shopify or any helpdesk vendor. Zendesk's allowance model is described two different ways across two official pages, so no per-unit Zendesk figure is quoted here. Fin Voice pricing is contact-sales and the figure circulating in blogs is unverified. Several Shopify negatives rest on documentation silence rather than an explicit denial, Sidekick's inability to write policy text among them; that one is the fastest-moving and should be re-checked before any launch.

---

## 10. Evaluation of the three named hypotheses

Supplied as hypotheses, not requirements: **Campaign Rules & Policy QA**, **Customer Conversation Gap Analyzer**, **Peak-Season Readiness Audit**. Each is judged against the research, the verified capability sweep, and whether it holds up without MCP.

### H1. Campaign Rules & Policy QA — validate, with one revision

**Verdict: accept, and merge the authoring case into it.**

This is the strongest of the three and it lands on the cleanest verified gap. Shopify holds every input in structured form, combines-with settings per discount class, active dates in the admin timezone, free-shipping thresholds at the discounted price, final-sale flags, and publishes none of it as prose. There is no sale-terms page type among the six policy templates. Policy text is absent from Sidekick's documented output. Checkout tells the shopper only that some codes could not be used together.

**Where the QA framing beats the authoring framing I proposed.** Three reasons, and this is a genuine improvement on `sale-terms-writer`:

1. **The trigger is more common.** Most merchants have *something* written. "Check what we have" fires more often than "write this from scratch".
2. **It has an objective grader.** Field coverage against a fixed list, and contradiction detection between stated terms, is checkable. An eval can score it without a rubric argument, which matters because the eval gates the MVP.
3. **It finds a class of defect authoring cannot.** A merchant can have complete terms that contradict their configured discount, or a returns policy that contradicts their final-sale flags. Nothing checks that today.

**The revision.** Do not split QA from authoring. They share the same field list, the same output shape and the same platform-limits warnings; the only difference is whether the field arrives from an existing document or from a question. One skill, two entry modes: audit what exists, then fill what is missing.

**Scope note.** The name bundles campaign rules and policy, which matches the research: discounts, returns and delivery are the three subjects stores least often have an answer for, and the first two share a field-and-output shape. The third does not, see H4 below.

**Without MCP:** complete. The merchant pastes what they have and states their settings. MCP would later add one genuinely new capability, reading the live discount configuration to detect a contradiction the merchant cannot see. That is v2.

### H2. Customer Conversation Gap Analyzer — validate the problem, defer the build

**Verdict: real gap, wrong slot for the first release.**

The problem is confirmed by the research, and it is the only recommendation in the ebook that recurs weekly. But the capability sweep narrowed the whitespace and surfaced a hard blocker:

- **Intercom Fin Recommendations already names three of the five buckets** correctly: content gap, customer data gap, action gap. It is gated behind a $99/mo add-on and has no documented export.
- **Nobody has a needs-a-handoff bucket and nobody has a needs-nothing bucket.** Intercom tried an ambiguity bucket and removed it as vague. Gorgias knows why it escalated and keeps only a tag and an outcome field, discarding the trigger.
- **Shopify Inbox has no conversation export at all**, in the UI or the API, and reports only assisted sessions, assisted orders, satisfaction and response time. **The merchant closest to Shopify cannot run this skill.**
- It is the only workflow in the set that handles shopper personal data.

**If it is built anyway, four conditions are non-negotiable.** It must consume any vendor's CSV rather than one vendor's shape. It must strip or refuse to echo personal data and say plainly what stays local. Classification must be deterministic first so week-over-week counts stay comparable, with model judgement only on what the rules cannot decide. And it must ship a path for merchants with no export, which realistically means working from a pasted sample and reporting proportions rather than counts.

**Without MCP:** yes, given a CSV. MCP is the one thing that would fix the export blocker, which is why this is the single workflow where deferring MCP and deferring the skill go together.

### H3. Peak-Season Readiness Audit — reject as stated, revise into something real

**Verdict: reject the questionnaire, keep the evidence check.**

**Why it is rejected as stated.** Shopify publishes a 25-step, three-phase BFCM checklist that already tells merchants to state discount terms clearly, to consider extending the returns window for the holidays, to prepare support for the volume, and to update the FAQ page with shipping windows, return policies and sale terms. A skill that asks a merchant those same questions and scores the answers adds a score to a list that already exists. The market is also saturated with free agency checklists.

**The distinction that decides it.** Does the audit check *answers*, or does it check *evidence*?

- Checking answers is a questionnaire. Redundant.
- Checking evidence, meaning the store's actually published pages against the questions the season produces, is genuinely absent. SEO tools define a content gap as a keyword a competitor ranks for. Helpdesk tools audit the bot's own knowledge base. Shopify's Knowledge Base app is the closest, and it is reactive, driven by external AI-agent traffic rather than the store's own shoppers, and it never reads the store's pages.

**The revision.** This is not a third skill. It is the front door and the closing check of H1: tell me what is missing, help me decide it, then verify I published it. Folding it in removes a skill from the count and makes H1's eval stronger, because "did the audit find the planted defect" is a harder and more honest test than "did it write something reasonable".

**Cost of the revision.** It needs the merchant's pages. Fetching them is possible where the agent has network access and impossible where it does not, so the skill must accept pasted text as the fallback. That is the same degradation rule the platform constraints already impose on every script.

### H4. What the three hypotheses miss

**Delivery cutoffs are absent from all three, and they are the second-strongest verified gap.**

- December is the longest exposure of the season: 23 consecutive days at 45% above baseline, against seven days at 62%.
- Delivery is the most-asked subject in every one of the four phases, at 4.91%, 4.17%, 5.27% and 3.98%, while discounts peak at 2.64%.
- **Shopify's built-in customer notifications contain no delayed-delivery template at all.** Order confirmation, cancelled, refund, shipping confirmation, shipping update, out for delivery, delivered. Nothing for the day it goes wrong.
- Nothing back-solves a target arrival date into per-zone last-order dates. Manual delivery dates are a single global setting with a hard noon cutoff; Shop Promise is US-only and top 1% of shippers; the Delivery Promise API is restricted to approved partners; Shopify's own carrier-deadline post was still the December 2025 edition when checked.

A peak-season toolkit whose scope stops at discounts and policy covers the loudest week and misses the longest month.

### Revised recommendation

| Hypothesis | Verdict | Becomes |
|---|---|---|
| Campaign Rules & Policy QA | Validate, revised | **Skill 1**, with audit and authoring as two entry modes |
| Peak-Season Readiness Audit | Reject as stated, merged | The front door and closing check of Skill 1 |
| Customer Conversation Gap Analyzer | Problem validated, build deferred | v2, with four conditions attached |
| Not proposed, recommended | New | **Skill 2**, delivery cutoffs and the three delivery templates |

Two skills, which is the same count and nearly the same total scope as the original recommendation, arrived at from the opposite direction. The naming and the QA framing are improvements and are adopted.

---

## 11. Correction, 21 September 2026: a real merchant-facing Shopify-ChatGPT connector exists

The capability sweep behind sections 1–10 missed this. Found by chasing a concrete user report of the Plugins tab in ChatGPT, not by re-running the original research.

**What it is.** The official "Shopify plugin for ChatGPT" (help.shopify.com/en/manual/ai-powered-tools/connecting-ai-tools/shopify-plugin-for-chatgpt). OAuth-connected: a merchant signs in and approves data access, then works with products, collections, inventory, orders, customers, discounts and analytics from inside a ChatGPT conversation. It is not on the Shopify App Store; it installs from a link inside ChatGPT itself. This is a different thing from Shopify Agentic Storefronts (shopper-facing product discovery and checkout), which is what the earlier research found and is all it found.

**The action relevant to Skill 1: `create-discount`.** Percentage-off only, scoped to the whole store, a product or a collection, with a minimum purchase requirement, a start date and usage rules. Two hard limits stated in Shopify's own docs: it cannot edit a code that already exists, and it cannot create a fixed-amount discount.

**What this changes.** The "Existing solution" cell for the discount-rules row in `ebook-to-product-mapping.md` now names this connector. Code *creation* is no longer something only a human clicking through the admin can do; it can be done conversationally.

**What this does not change.** The gap Skill 1 fills was never code creation. It was the shopper-facing explanation: does this code stack, is a reduced item eligible, which price the free-shipping threshold measures, what a shopper is told when the code fails. `create-discount` does not produce any of that text, and nothing in the plugin's action list audits an existing terms page for the kind of contradiction `audit-planted-defects` tests for. The connector configures; it does not explain or check.

**A finding that strengthens Skill 1's returns-policy half.** The plugin's own documented limits state plainly: *"A connected AI tool can't issue refunds, cancel or capture orders, mark orders as paid, process returns, or create and adjust gift cards. These actions are blocked even when you approve write access."* Even the vendor's own most-capable connector refuses returns work by design. That is independent confirmation of something this assessment already concluded from Shopify's self-serve returns documentation: returns needs a human, or needs the kind of policy-writing help this skill gives, not a connector.

**Skill 2 is untouched.** The connector's action list has no shipping, delivery, or cutoff-date action of any kind.

**Process note.** This was found through a user showing me their own ChatGPT screen and a follow-up web search, not through the original multi-agent capability sweep. The sweep searched Shopify's manual, Sidekick's docs, and mainstream helpdesks; it did not search "Shopify plugin for ChatGPT" as its own term, which is why the connector installs from inside ChatGPT rather than from Shopify's own app listings, and would not surface from a Shopify-side search alone.
