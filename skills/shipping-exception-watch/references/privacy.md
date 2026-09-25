# Privacy

An order export carries shoppers' names, emails, phone numbers, home addresses and order notes. None of that is needed to find a late parcel.

- **What the output may contain:** order number, carrier, tracking number, country, status and tracking detail as written in the file, and dates.
- **What it must never contain:** names, email addresses, phone numbers, street addresses, order notes, payment details. `scripts/watch.py` never reads those columns, even when they sit in the CSV.
- **No names, including first names.** The drafts greet the shopper with `[first name]`, which the merchant's email or helpdesk tool fills in when the message is sent to that order's customer. The merchant already has the name there, so pasting it into an AI chat adds risk and nothing else.
- **Same rule for the manual path.** Before the merchant pastes rows, tell them to delete every column except: order number, ship date (`Fulfilled at`), shipping country (only if the promise differs by country), delivery status, promised date if they have one, and for a tracking app or carrier export also carrier, tracking number, last scan date and status detail. Names, emails, phone numbers, addresses and `Notes` go. If they paste more anyway, do not repeat the extra fields back in the summary or the drafts.
- **Do not keep the file around** longer than the task needs, and do not paste customer rows into anything outside the merchant's own session.
