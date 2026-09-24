# Privacy

An order export carries shoppers' names, emails, phone numbers and home addresses. None of that is needed to find a late parcel.

- **What the output may contain:** order number, customer first name, carrier, tracking number, zone, status as written in the file, and dates.
- **What it must never contain:** email addresses, phone numbers, street addresses, full surnames, payment details. `scripts/watch.py` never reads those columns into its result, even when they sit in the CSV.
- **Same rule for the manual path.** When the merchant pastes rows instead of running the script, ask for only the columns listed in `input-schema.md`. If they paste more, do not repeat the extra fields back in the summary or the drafts.
- **Drafts use placeholders** for anything personal the merchant's sending tool fills in: `[first name]`, `[tracking link]`. The merchant's own email or helpdesk tool already holds the address.
- **Do not keep the file around** longer than the task needs, and do not paste customer rows into anything outside the merchant's own session.
