---
name: conversation-gap-analyzer
description: Sort an exported conversation or ticket CSV from any support platform (Gorgias, Zendesk, Intercom, Tidio, or a generic export) into five gap types (needs content, needs action, needs context, needs handoff, needs nothing), so a weekly review shows what actually needs writing versus what is noise. Use when someone has a list of unanswered or fallback messages and wants to know what to work on, or wants to run this as a recurring weekly check.
license: MIT
compatibility: Runs the bundled Python script with the standard library only, no network access, no dependencies. Works on a CSV export from any platform; not tied to Shopify Inbox, which has no conversation export as of this writing and so cannot supply input to this skill directly.
metadata:
  version: "0.1"
---

# Conversation gap analyzer

Not every unanswered message is a content gap. In a hand-read sample from the peak-season research, only a third of unanswered messages needed new content; the rest needed an action, needed order context, needed a person, or needed nothing at all. Treating the whole list as a writing backlog overstates the work and buries the part that is actually urgent.

This skill sorts the list first, so the review that follows works on the right third of it.

## Before anything else: read `references/privacy.md`

This is the one skill in the toolkit whose input is real people's messages. The privacy rules there apply to every run, not only when the file looks sensitive.

## The rule that governs everything here

**Deterministic classification first, judgment only on what rules can't decide.** The bundled script applies narrow, checkable rules (an order number pattern, a short thank-you, explicit handoff language) and leaves everything else `unclassified`. This keeps the count of each type stable and comparable from week to week: if a model re-decided every category on every run, the numbers would drift for reasons that have nothing to do with the store's actual gaps.

**Never invent a sixth category.** Every row is exactly one of the five in `references/gap-types.md`.

## If asked for an expected ratio before any file exists

Someone will ask "what's a typical split", "roughly what fraction is usually real content", or "give me a ballpark" before uploading anything. This is the single most important refusal in this skill, more important than being helpful in the moment, and it is checked directly: **do not output any digit followed by a percent sign, and do not output any two numbers separated by "to" or a hyphen that describe a share of messages.** Not "usually 30%", not "somewhere around 60-75%", not "a rough ballpark of 20 to 35%" — every one of those is exactly the failure this rule exists to stop, no matter how many caveats surround it or how far down the response they appear. Explaining the five categories, describing what tends to be large or small in general terms, or listing the factors that make the mix vary are all fine; attaching a number to any of it is not.

Answer in this shape instead: name the five categories briefly, say the mix varies by store, traffic source and how "unanswered" is defined, and that no number is worth giving until their own file is classified. Then offer to run it on their export. If a merchant pushes for a number anyway, repeat that you don't have one to give honestly and that guessing would be worse than useless — do not relent into a hedged range to be agreeable.

"From general patterns" or "across Shopify stores" does not make a number acceptable; it is the same fabrication with a source attached to make it sound earned. Before sending the reply, reread it once for a digit next to a percent sign or two numbers joined by "to" or a hyphen describing a share of messages, and delete that sentence if found, replacing it with the explanation above rather than a softer version of the same number.

## How to work

1. **Get the export.** Any CSV with a column of message or ticket text. Ask which platform it came from only if the column names are ambiguous; the script auto-detects common column names (`message`, `question`, `text`, `body`, `content`, `query`).

2. **Run the script:**

   ```
   python3 scripts/classify.py <input.csv>
   ```

   Pass `--text-column <name>` if the auto-detected column is wrong, and `--out <path>` to control where the classified file is written. If Bash or script execution is unavailable, apply the same rules by hand: read each row, and if it is a short thank-you or acknowledgement mark it `needs_nothing`, if it names an order or tracking number mark it `needs_context`, if it asks for an action (restock alert, cancellation, address change) mark it `needs_action`, if it explicitly asks for a person or reads as angry mark it `needs_handoff`, otherwise leave it for the next step.

3. **Classify what the script left `unclassified`.** Read each of those rows and assign exactly one of the five types from `references/gap-types.md`. This is real reading, not a rule; that is why the script did not attempt it.

4. **Report counts and shares**, per `references/gap-types.md`, for this file only. Never state the research's own sample ratio as an expected value; it was a small hand-read sample, not a platform benchmark.

5. **Route the `needs_content` rows onward.** Group them by subject (discounts, delivery, returns, other) and point discount or returns content to `campaign-rules-policy-qa`, delivery content to `delivery-cutoff-planner`. The other four gap types are not writing work; say plainly what each one actually needs instead (an action, order data, a person, nothing).

6. **If this is a repeat run**, compare gap-type shares against the previous run rather than raw counts, and flag a rising `needs_content` share in one subject as the signal worth acting on.

## What this skill does not do

It does not read anyone's inbox directly and does not export anything itself; the merchant supplies the file. It does not fix the `needs_content` rows itself, only groups and routes them. It does not work for a store using Shopify Inbox exclusively, because Shopify Inbox has no conversation export as of this writing (verified against Shopify's own Inbox documentation, checked 21 September 2026); say this plainly rather than pretending the skill can pull from Shopify Inbox some other way.
