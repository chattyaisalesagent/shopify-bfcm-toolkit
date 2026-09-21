# Ebook to product mapping

Product discovery for a possible Shopify peak-season toolkit, traced line by line to the research that motivates it.

**Research input:** `CHATTY/.claude/skills/creating-ebook/projects/bfcm-2026-state-of-cx/bfcm-2026-state-of-cx.pdf`, 27 pages, public English edition as rebuilt 21 September 2026. Measurement notes: `DATA-NOTES.md`. Editorial decisions, including what was cut and why: `REVIEW-ACTIONS.md`.

**Status:** discovery. No plugin, skill list or MVP scope has been decided. Nothing in this document is a commitment to build.

**The "Existing solution" column is now verified.** Every entry was checked against vendor documentation on 21 September 2026, covering Shopify, Shopify Sidekick, Shopify Inbox, Shopify Knowledge Base, Gorgias, Zendesk, Intercom and Tidio. Sources and the items that could not be verified are in `docs/skill-opportunity-assessment.md`. Four MVP decisions changed as a result, and each says so in its Reason cell.

---

## 1. The research in one paragraph

Peak season is not one support spike. It is a sequence of four phases, and each phase asks a different question, so each set of answers has a different deadline. Across all stores, BFCM week ran 62% above the four weeks before it, but early December ran 45% above for 23 consecutive days, so the long exposure is December rather than the sale. The subject changes with the phase: discounts peak in sale week, delivery before the holiday, stock after it, and returns peaks in none of them. The order of work is set by what the store sells, not by a shared calendar. And the three subjects a store's own content least often answers are discounts, returns and delivery, because all three depend on the rules of one sale or the state of one order rather than on the product catalogue.

**The product-relevant consequence.** Every finding terminates in merchant-side work: a decision to make, a rule to write down, a date to publish, a list to sort. None of it exists anywhere until the merchant creates it, which is why a shopper-facing assistant cannot originate any of it. That is the only space a toolkit could legitimately occupy.

---

## 2. Evidence discipline

Binding constraints on the product, derived from the weaknesses the ebook itself discloses on page 24 and from the revision decisions made during its review.

| Constraint | Origin | Enforcement in any product built |
|---|---|---|
| The 33-of-99 manual sample is not a platform benchmark | One reader, 99 messages, no second coder, page 15 | No expected ratio of real questions to noise is ever quoted. A triage workflow reports the merchant's own counts from the merchant's own file |
| "12 in 100" was a misleading unit and was removed from the ebook | Readers took 100 as the sample size | Use the measured share change, 0.88% to 12.10%, and state that per-industry sample sizes are not published |
| 62% is platform-wide, not a store forecast | Median store grew 31%; the quietest quarter fell to 0.73x, page 5 | Any projection starts from the merchant's own history and presents a range. 62% is never a default |
| Not every unanswered message is a content gap | The manual sample split across missing content, action requests, short replies and off-topic messages | Triage must route to at least four outcomes. A single "write content" bucket is a defect |
| Different wording does not prove the same intent | 13.5% exact-repeat measures text, not meaning, page 16 | Wording work is framed as "does your setup handle these phrasings", never as intent coverage |
| An illustrative incident is not a failure pattern | Page 18 comes from forum posts and app reviews, with no frequency measured | Those items ship as a pre-season check list carrying no prevalence claim |
| Measured, observed, inferred and recommended stay separate | The ebook labels its own evidence this way | Every generated artefact carries the same four labels |

---

## 3. Traceability table

| Ebook page/section | Finding or recommendation | Merchant job to be done | Existing solution | Remaining gap | Merchant judgment required? | Candidate solution | MVP decision | Reason |
|---|---|---|---|---|---|---|---|---|
| p2, p5, Part 1 | Messages per day ran 62% above the pre-sale baseline in BFCM week and 45% above for 23 days in December | Estimate the support load this store should plan for | Zendesk Explore forecasts seasonally; its usage Forecast tab watches the allowance; Shopify holds no conversation history | No tool joins a seasonal forecast of the store's own volume to that store's plan limit and overage price. Zendesk owns both halves and has never joined them | Yes. Which scenario to staff for is a risk call | Skill with deterministic script | Defer | Real and sharp, but it needs a volume export that a Shopify Inbox merchant does not have |
| p2, p5 | Platform-wide growth differs from the median store: 1.31x median, 0.73x for the quietest quarter, 2.13x and above for the busiest | Avoid treating an average as a personal forecast | None | Nothing in the stack prevents the error, and the ebook itself had to be corrected twice for it | Yes | Documentation | Include | A reasoning error to design against, not a feature. It becomes a hard rule inside the projection script |
| p7, p8, Part 2 | Each phase lifts a different subject; the five measured subjects cover about one tenth of all messages | Know which body of content is due before which phase | Shopify's retail holiday calendar lists shopping events, not store tasks | None of them map shopper intent to a content deadline | Low. The pattern is given, the dates are the merchant's | Documentation | Combine with another workflow | Reference data consumed by the planning workflow, not a workflow itself |
| p9 | Discount-related messages at toy stores moved 0.88% to 12.10% between phases, while the share fell at electronics stores | Choose the priority order for this store's category | None | No tool knows which subject a given category should prepare first | Yes. Only the merchant knows their real mix | Reusable prompt | Combine with another workflow | A branch inside the planner. A lookup table does not justify a skill |
| p10 | Sale week is the season's peak for discount questions, with five named rules shoppers ask about | Decide and write the discount rules: stacking with automatic discounts, eligibility of already-reduced items, returnability of discounted items, free-shipping threshold order, start and end times with timezone, exclusions, gift exchange | Shopify configures every mechanic: combines-with per class, active dates in the admin timezone, thresholds at the discounted price, final-sale flags. Sidekick writes blog posts, product copy, images, segments, discounts. **The official Shopify plugin for ChatGPT (OAuth-connected, not on the App Store, installed from within ChatGPT) has a `create-discount` action: percentage-off only, whole store, product or collection, with a minimum purchase, a start date and usage rules. It cannot edit an existing code and cannot create a fixed-amount discount.** (help.shopify.com/en/manual/ai-powered-tools/connecting-ai-tools/shopify-plugin-for-chatgpt, checked 21 Sep 2026) | **No discount-terms page type exists among Shopify's six policy templates.** Policy text is absent from Sidekick's documented output. The Knowledge Base app's auto-facts exclude discounts. Checkout says only "Some discount codes couldn't be used together." **The ChatGPT plugin configures a new code; it does not write the shopper-facing explanation of stacking, eligibility of reduced items, or the free-shipping threshold order, does not audit an existing terms page for contradictions, and its own docs state a connected AI tool "can't issue refunds... or process returns" even with write access approved** | Yes, on every field | Reusable skill | Include | The highest-frequency gap in the research. A real merchant-facing Shopify-ChatGPT connector exists and was missed in the first capability sweep; it narrows this row (code creation is no longer un-automatable) but does not close it (the explanation text, the audit, and returns remain untouched) |
| p11 | Delivery peaks at 5.27% from 2 to 24 December, the longest phase of the season | Publish order-by dates per region, and write the three delivery templates: dispatched, running late, will not arrive in time | Automated delivery dates render only within 4 to 5 days and same-region; manual dates are a single global setting with a hard noon cutoff; Shop Promise is US-only and top 1% of shippers | Nothing back-solves a target date into per-zone last-order dates. **Shopify ships no delayed-delivery notification template at all**, and its carrier-deadline post was still the Dec 2025 edition on 21 Sep 2026 | Yes. The cutoff is a promise the merchant has to keep | Skill with deterministic script | Include | The date arithmetic is deterministic and checkable; the buffer is a judgment the script must ask for rather than assume |
| p12 | Stock questions peak at 2.24% after the holiday, while total volume is already back to normal | Fix the holiday returns window, the exchange process, who pays return shipping, and gifts without a receipt | Return rules cover window, return-shipping cost, restocking fee and final sale; self-serve returns run from the store and the Shop app | **A seasonal window is inexpressible**: rules offer only N days from delivery, and changes apply to future orders only. Self-serve excludes exchanges outright and excludes guests and gift recipients. Nothing turns return rules into published policy text | Yes | Reusable skill | Combine with another workflow | Identical field-and-output shape to the discount row, so one skill with three packs rather than three skills |
| p10, p11, p12 | Each phase page lists the questions a store must have an answer ready for | Audit whether existing pages actually answer those questions | Shopify's Knowledge Base app logs answered and unanswered questions; SEO tools do keyword gap analysis; helpdesks audit their own bot knowledge | Nothing grades published pages against shopper questions. The Knowledge Base app is driven by external AI-agent traffic, is reactive, and never reads the store's pages | Yes, to judge sufficiency | Reusable skill | Research further | Attractive, but it needs either page fetching or a lot of pasting. Value depends on how the input is obtained |
| p13, p14 | Discounts, returns and delivery run short of a matching answer 1.7x, 1.6x and 1.4x as often as size questions | Find out which subjects this store is least ready to answer | None | A merchant cannot reproduce the reference group the index is built on | Yes, to interpret | Skill with deterministic script | Combine with another workflow | Subject counts fall out of the triage workflow for free. The index itself is not reproducible outside the research |
| p14 | "No answer ready" means no matching content was found, not that the shopper was abandoned | Read the metric correctly before acting on it | None | The phrase is routinely misread as a failure rate | No | Documentation | Include | A glossary entry reused by every workflow and every output |
| p15 | An unanswered-message list mixes missing content, action requests, short replies and off-topic messages | Triage the export before planning any writing | **Intercom Fin Recommendations already names three of five buckets** (content, customer-data, action), gated behind a paid add-on with no export. Gorgias and Zendesk export CSV | No vendor has a needs-a-handoff or a needs-nothing type. Intercom removed its ambiguity bucket; Gorgias discards the handover reason. **Shopify Inbox has no export at all** | Yes, on edge cases | Skill with deterministic script | Defer | Best frequency argument in the research, but the gap narrowed, the most Shopify-native merchant cannot export, and it is the only workflow carrying shopper personal data |
| p15, p21 | Keep order numbers in the list; they signal a workflow break rather than a content gap | Route order numbers to the order-lookup check instead of the writing queue | None | — | No | Skill with deterministic script | Combine with another workflow | A classification rule inside the triage script |
| p16 | Only 13.5% of messages repeat an earlier message word for word | Test whether the store's content and chosen assistant handle several expressions of one intent | Intercom Batch test takes up to 50 questions and **accepts CSV upload**; everyone else tests one question at a time | Intercom states outright that none of its tools generate paraphrased variations. The generation step ships nowhere merchant-facing | Yes, to judge the answers | Reusable skill | Defer | Revised upward: because Intercom ingests a CSV it cannot generate, a skill that produces the test set has an immediate home and needs no integration |
| p19, p20 | Turn on automated order lookup, then test it on a real order, an unknown number and a late shipment | Verify the order-lookup path end to end | Commodity. Shopify Inbox lists order lookups and carries AI context on handoff; Gorgias authenticates by one-time code and edits orders; Zendesk ships 16 Shopify actions | None worth building. Transcript carry-over is universal, so handoff with context is not a differentiator | Yes, for the handoff rules | No additional product needed | Reject | Verified commodity across five vendors |
| p19, p20, p23 | Handoff needs rules, a summary and someone with authority | Define escalation triggers and name who can approve an exception | Routing exists in every helpdesk; Zendesk and Intercom document AI-written summaries | The authority policy is undocumented in most stores, but writing it is a governance act | Yes | Human or qualified professional responsibility | Defer | Commercial authority cannot be automated. At most it can be elicited and recorded |
| p18, p19, p20 | Volume rises in the month the plan cap is most likely to break; ask what happens at the cap and who receives those questions | Verify limits, overage pricing and fallback behaviour of whichever support or AI system the store runs | Vendor pricing pages. Intercom hard-limits to handover, Zendesk offers a do-not-allow-overage switch, Gorgias auto-bills | Gorgias Basic includes 30 AI interactions against 300 tickets, overage above the in-plan rate, and one resolution burns two meters. Nothing warns a merchant before the season | Yes | Reusable skill | Defer | Merges with the volume projection into one capacity workflow, deferred with it |
| p21 | Review for one hour each week, and once a day during BFCM week, routing each item by type of gap | Keep the review running through the whole season | Saved views and task managers | No routing logic, and no cadence tied to the phases of the season | Yes | Multi-skill plugin | Defer | Wraps the triage workflow, so it defers with it |
| p18 | Some assistants stop answering at the cap; a chat widget can cover the checkout button on mobile | Check the store on a real phone and confirm cap behaviour before the season | Theme preview and CRO audit apps | Nothing checks a chat widget against a checkout button | No | Documentation | Include | These are illustrative incidents. A check list is honest; an automated scan would imply a prevalence we never measured |
| p19 | Six-line readiness scorecard, with plan cap, order lookup and handoff outranking the total score | Score readiness and decide what to fix first | **Shopify publishes a 25-step, three-phase BFCM checklist** already naming discount terms, extended holiday returns, support volume and FAQ updates | It is undated prose that produces no artifact, and there is no readiness score in the admin | Yes | No additional product needed | Reject | The check-if-Shopify-already-does-this flag fired. Another checklist is redundant. What is missing is the artifacts it asks for |
| p20, p22 | Deadlines of 1 Nov, 15 Nov and 15 Dec, each traced to a finding, plus the October to mid-January calendar | Produce a dated plan for this store, this market, this year | Agencies publish dated 8-week and 90-day BFCM timelines in volume; Shopify Flow can execute a dated plan | Nothing derives deadlines from the store's own facts: its processing time, zones, return window and carrier mix | Yes. Markets, carriers and holidays differ | Reusable skill | Reject | Weakest gap of the set. The market is saturated with free generic timelines. Only the store-derived dates are defensible, and those belong to the delivery workflow |
| p6 | US seasonal hiring at a 15-year low; 41% of shoppers say a brand-owned assistant raises purchase confidence | Understand the context | Not applicable | Not applicable | No | No additional product needed | Reject | Third-party context with no merchant task attached |
| p23 | Capability mapping for one named vendor | Choose a support vendor | Not applicable | Not applicable | Yes | No additional product needed | Reject | Vendor-specific, and excluded by the independence requirement |
| p24 | Seven stated limits: not representative of Shopify, keyword undercounting, one season only, machine-assigned labels, counted by message, no revenue link | Do not over-generalize the research | Not applicable | Research of this kind is routinely over-claimed once it reaches marketing | No | Documentation | Include | The constraints in section 2 are the enforcement mechanism for this row |
| p12, p24 | The holiday returns policy text itself | Publish a policy that holds up | Shopify's policy generator offers six templates, none for sale terms | Consumer-law obligations vary by market | Yes | Human or qualified professional responsibility | Include | Ships as a warning in the output, never as generated legal text |

---

## 4. Discovery questions answered

**1. What merchant jobs does the ebook reveal?** Eleven distinct ones survive the table: project the load, decide and publish discount rules, compute and publish delivery cutoffs, decide and publish post-holiday returns and stock answers, audit existing pages against the season's questions, triage an unanswered-message export, keep that triage on a weekly cadence, verify support capacity and cap behaviour, test several phrasings, score readiness, and produce a dated plan.

**2. Which occur often enough to justify a reusable workflow?** Only one is weekly: the triage. Three are once-per-season but high-consequence and highly structured: discount rules, delivery cutoffs, returns and stock. One is once-per-season and cheap: the scorecard. The rest are one-off or occasional, which is an argument for documentation rather than a skill.

**3. Which are already adequately solved?** Order lookup and handoff routing, almost certainly. Discount configuration, delivery date display and the returns engine, partially: the platform enforces the rules but does not publish the explanation. Pending verification of what Shopify Sidekick and the official BFCM checklists already cover, which is the single largest open risk in this document.

**4. Which need only a normal prompt?** Industry priority order, phrasing variations, and arguably the scorecard. None of them carry fixed fields, deterministic logic or a validation step, which is what separates a skill from a prompt.

**5. Which need deterministic scripts or structured validation?** Volume projection, because percentile arithmetic done in prose is unreliable. Delivery cutoff computation, because it is working-day arithmetic across regions and carrier dates. Triage classification, because consistency across a few hundred rows and across weeks is the whole point, and a language model re-deciding categories each run would destroy week-to-week comparability.

**6. Which need live data to be worth doing?** Order-lookup testing and phrasing tests against a running assistant. Both are deferred for that reason. Everything else can run on merchant answers plus an exported file.

**7. Which require merchant judgment and must not be automated?** Every field of the discount rules, the delivery buffer behind each cutoff, the length of the returns window, who pays return shipping, and the escalation triggers. The product's job is to ask well and record faithfully, not to answer.

**8. Which involve authority that must stay with a qualified human?** Exception and refund authority, and the legal sufficiency of a published returns policy in a given market.

**9. Can a useful MVP be built without MCP?** Provisionally yes. The three strongest workflows consume merchant answers and one uploaded CSV. This is answered properly in the MCP section of `docs/skill-opportunity-assessment.md` once the platform constraints are verified.

**10. Smallest coherent set of skills?** Between two and four, with a scorecard as the entry point. The detailed proposal, ranking and the case for each is in `docs/skill-opportunity-assessment.md`. This document deliberately stops short of proposing them, because the grouping and ranking is a separate decision that must be able to conclude "build nothing".

---

## 5. Platform-neutral translation

The research was measured on one vendor's platform. Any product built from it is not. Each vendor-specific phrase resolves to a neutral job.

| Research phrasing | Merchant job to be done |
|---|---|
| Review the unanswered messages in the assistant | Analyze a conversation, ticket or AI-fallback export from any support platform |
| Prepare content for the assistant's knowledge base | Prepare approved source content for product pages, policy pages, staff responses, helpdesks and AI assistants |
| Check the plan cap and overage | Verify the limits, overage behaviour and fallback behaviour of whichever support or AI system the merchant uses |
| Test wording variations against the assistant | Test whether the merchant's content and chosen support system handle several expressions of the same intent |
| No answer ready | No matching approved content was found for the question |

The test for independence: a merchant who has never heard of the vendor behind the research must be able to run every workflow using files they can export from whatever they already run.

---

## 6. Product origin statement

Internal, for architecture and scope decisions:

> The toolkit is the practical companion to the BFCM readiness ebook developed in this project. The ebook explains what changes across peak season and where merchants are often unprepared. The toolkit converts those insights into guided, repeatable workflows that merchants can run against their own store information.

Public-facing:

> Built from peak-season customer-conversation research, this independent toolkit helps Shopify merchants turn readiness insights into store-specific decisions, tests and action plans.

The toolkit does not prove the research, and the research does not describe every Shopify store.

---

## 7. What happens next

1. `docs/skill-opportunity-assessment.md`: group the jobs into workflows, remove what existing tools already serve, reject anything that is only a writing prompt, merge overlaps, propose between zero and five skills, rank them, and recommend the smallest coherent MVP or none.
2. `docs/platform-compatibility.md`: verified packaging and execution constraints, with sources and dates. This also resolves every _(provisional)_ entry above.
3. Decision gate. No `SKILL.md`, plugin manifest or scaffold before approval.
