# Roster template

Present the roster in this layout. One row per day across the whole window, weekends included. Do not collapse days into ranges, because days off and weekends make neighbouring days different. Shifts the draft added are marked "(added)".

| Date | Day | Phase | Forecast | Hours needed | On shift (shift times) | Hours available | Gap | Carried in | Left at end of day | Uncovered hours |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-27 | Fri | BFCM week | 198 | 19.8 | Mai 09:00-17:00, Lan 13:00-21:00 | 12.0 | 7.8 | - | 7.8 | 00:00-09:00, 21:00-24:00 |
| 2026-11-28 | Sat | BFCM week | 165 | 16.5 | Mai 10:00-16:00 (added), Lan 10:00-14:00 | 7.5 | 9.0 | 7.8 | 16.8 | 00:00-10:00, 16:00-24:00 |

"Gap" is that day's work minus that day's hours. "Carried in" is work left from the day before. "Left at end of day" is what is still waiting when the last shift ends; it carries to the next day. With an hourly share from the merchant, add a column "Messages while nobody is on" with the count and the hours.

## How the draft fills gaps

The draft only uses people the merchant said can take extra days, on the weekdays they named, with the shift times the merchant gave for an added day. Walk the days in order. When the day's work plus carried-over work is more than the hours on shift, add the first person in the merchant's team order who:

1. is not already working that day,
2. lists that weekday as a day they can add,
3. is not on a day off or outside their start and end dates,
4. would not go over the longest run of working days allowed (the merchant's rule, or six),
5. would stay within their weekly hours (Monday to Sunday), if the merchant gave a limit.

Repeat until the day is covered or nobody is left. Never move a regular shift, cancel a day off or add someone the merchant did not name. The draft is a proposal for the merchant to confirm, and every added shift says so.

## Under the table

**Before and after.** Days ending with work waiting and hours left on the last day, first with the merchant's own shifts, then with the draft.

**Need extra help.** Every day that still ends with work waiting after the draft, with the hours. These are the days a new person, longer shifts or less volume would have to cover. For each, say what one extra shift of a length the merchant already uses would cover: "one more 8-hour shift on Saturday 28 November covers 6.0 hours at 75 percent answering time." Show the arithmetic.

**Per person view.** For each person: days worked, total shift hours, days added by the draft, longest run of working days. Flag anyone over the limit as `[DECISION NEEDED: <name> works <n> days in a row from <date> to <date>, confirm or change]`. An owner rostered every day of the window is flagged the same way.

**Uncovered hours.** List only. Do not propose who or what should cover them.

**Seasonal hires.** If the merchant adds a person, give them a start date at least a week before their first busy day so they can learn the policies (the Peak Season Playbook brief is written for this).
