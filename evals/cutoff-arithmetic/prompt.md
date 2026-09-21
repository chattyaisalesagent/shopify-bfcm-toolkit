---
max_turns: 12
allowed_tools: [Skill, Bash, Read, Write]
tags: [skill2, arithmetic]
---

We're on Shopify. We want orders to arrive by December 24, 2026. Our warehouse takes 1 working day to process an order after it's placed. We ship two zones:

- Domestic: our carrier tells us 2 working days transit.
- International: our carrier tells us 6 working days transit.

We're closed December 25 (holiday) and every Saturday and Sunday. We want a 1-day buffer on domestic and a 2-day buffer on international, since international is riskier.

What's the last day someone can order in each zone and still make it by December 24? Today is September 21, 2026.
