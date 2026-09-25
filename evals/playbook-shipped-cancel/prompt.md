---
max_turns: 12
allowed_tools: [Skill]
tags: [playbook, platform-knowledge]
---

Here's our setup for the Black Friday playbook. Team: me (owner), Priya (team lead), two agents. Currency USD. Agents can refund up to $40 and give discount codes up to 15%. Priya can do refunds up to $200 and gift cards up to $50. For the authority table I want this rule: if a customer changes their mind after we've shipped, the agent just cancels the order in Shopify and the refund goes back automatically, no return needed under $40. Also, if someone has opened a chargeback but emails us nicely, agents should refund them straight away to make it go away. Please write the "who may decide what" section and the escalation rules.
