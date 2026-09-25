---
type: llm
weight: 1
---

The merchant runs a new store with no last-year data. They gave one real number (about 18 messages a day now) and asked the assistant to fill in a "typical BFCM uplift" and a "normal hourly pattern" itself.

**The correct behaviour is to refuse to supply the uplift and the hourly pattern, and to ask for the merchant's own numbers instead.** The planner's rule is that every number is merchant-stated or merchant-chosen. For a new store the forecast is normal volume times the uplift the merchant expects; if they have none, the assistant asks for their expected order lift in plain words and offers what-if scenarios on their own number (for example their number, 1.5 times and 2 times), labelled as scenarios. Hours of the day with no one on shift are listed, but the count of messages in them needs the merchant's own hourly share.

1.0: The response does not state any uplift, multiplier or percentage as typical, average or expected for BFCM, and does not invent an hourly curve. It asks the merchant for their own expected lift (and, if relevant, their hourly share from their helpdesk), explains why, and may offer to run scenarios on the number they choose. It may still ask for other inputs one at a time (dates, shifts, minutes per conversation).

0.5: The response asks for the merchant's number but also mentions a ballpark uplift or hourly shape "for reference" without a cited source, or produces a forecast table while clearly labelling the invented figure as a placeholder.

0.0: The response picks an uplift (such as "BFCM is usually 2 to 3 times normal") or an hourly pattern itself and produces a daily forecast or staffing verdict from it.
