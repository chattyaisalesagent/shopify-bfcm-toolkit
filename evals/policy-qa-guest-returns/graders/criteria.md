---
type: llm
weight: 1
---

Two verified Shopify facts are being tested, both of which end up word for word in a saved reply that staff send to shoppers.

**1. Guest buyers can self-serve a return.** With the new customer accounts and self-serve returns on, a shopper signs in with the email address on the order and a 6-digit verification code sent to that email. No password is needed, and every order adds the buyer to the store's customer list, so a buyer who checked out as a guest can sign in and request a return themselves. The groups that genuinely need a person are gift recipients (the code goes to the buyer's email, not theirs) and anyone who wants an exchange (exchanges cannot be requested through self-serve returns). Legacy customer accounts do not support self-serve returns, but the merchant said they use the new ones.

**2. The checkout message, quoted exactly.** When a code cannot be combined with the discounts already applied, Shopify checkout shows: Discount couldn't be used with your existing discounts. A saved reply that quotes it should use exactly that text so the shopper recognises it.

**Scoring.**

1.0 Says the "guest return" reply is wrong, and the fixed version tells a guest buyer to sign in with their order email and the 6-digit code and request the return themselves, with no password. Keeps a person route only for gift recipients or exchanges, if it mentions them. The fixed "code not working" reply quotes the checkout message exactly as "Discount couldn't be used with your existing discounts" (straight or curly apostrophe is fine; capitalisation and wording must match), and states BF25 does not combine with other codes or automatic discounts, as the merchant said. Does not invent rules the merchant did not give.

0.5 Gets one of the two facts right, or gets the guest fact right but hedges it ("guests may be able to"), or paraphrases the checkout message instead of quoting it.

0.0 Keeps or repeats the claim that guest buyers cannot start a return online or need a person or an account password. Also zero for inventing a checkout message such as "Some discount codes couldn't be used together" or "These codes can't be combined" and presenting it as what checkout shows.
