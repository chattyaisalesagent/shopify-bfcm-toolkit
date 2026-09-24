# Handling the export

A conversation or ticket export contains shopper personal data: names, emails, phone numbers, order numbers, sometimes payment last-four digits. This is the one skill in the toolkit that touches personal data, and it is treated differently from the other three because of it.

## What to do

**Never quote raw message text in the summary report.** The report is counts and gap types, not a reading list. If an example is genuinely useful to illustrate a gap type, paraphrase it and strip anything identifying: no names, no emails, no order numbers, no exact phrasing that could be searched back to a real person.

**Never echo the file's contents back into the conversation** beyond the counts, the gap-type table, and short paraphrased examples as above. The classified CSV the script writes stays a file, not something read aloud row by row.

**Tell the merchant plainly, before running anything, what happens to the file.** In a local environment (Claude Code, Codex CLI), the file and its classified output stay on their machine; nothing is sent anywhere by this skill. In a hosted chat environment, be explicit that the file content is processed by that chat platform under its own data terms, and say so before the merchant uploads anything, not after.

**If the merchant pastes message text directly into the chat** instead of uploading a file, the same rule applies to the output: summarize and count, do not repeat identifying detail back.

## Why this matters more here than in the other three skills

`campaign-rules-policy-qa` and `delivery-cutoff-planner` work from merchant-supplied facts and decisions, not shopper data. `peak-season-readiness-audit` reads store configuration, not individual shoppers. This skill is the only one whose input is, by definition, a list of real people's messages. Treat it accordingly, every time, not only when the file looks sensitive.
