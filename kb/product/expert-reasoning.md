# Product management — expert reasoning layer (how a product expert thinks)

Product work is deciding what NOT to build. The skill is separating the problem from the solution, and the loud request
from the real need. Feature requests are data about a need, not a spec to implement.

## Discovery method (problem before solution)
- When someone asks for a feature, find the need behind it: "what are you trying to do, and what happens if you cannot?" The asked-for solution is often not the best one.
- Distinguish the problem's size (how many, how often, how painful) from its volume (how loudly one customer asks). Loudest ≠ biggest.
- Evidence beats opinion: talk to users, watch behaviour, look at the funnel. "I think" is a hypothesis to test, not a decision.

## Prioritisation method
- Rank by value vs effort, made explicit. RICE (reach × impact × confidence ÷ effort) or similar forces you to state the guess and the uncertainty rather than go on gut.
- Confidence is a real multiplier: a high-impact idea you are unsure about should be de-risked with a cheap test before a big build.
- Opportunity cost is the true cost: every yes is a no to everything else that quarter. Protect the roadmap from death-by-a-thous-features.

### Worked case — "a big customer demands feature X or they churn"
- Separate signal from leverage: is X a need many share, or one account's wish backed by a threat? Check how many others hit the same need.
- Reframe to the underlying job; often a smaller, more general solution serves X and others. Build the need, not the literal ask.
- Decide on value vs opportunity cost, not on who shouted. If you build it, do so because it is the best use of the quarter — and say what it displaces.
- De-risk first: a prototype or manual workaround can hold the account while you confirm demand, avoiding a big bet on an n=1 signal.

## Shipping and learning
- Ship the smallest thing that tests the core assumption (an MVP is an experiment, not a tiny v1). Define the success metric and the kill criterion before building.
- Outcomes over output: features shipped is vanity; the metric moving (activation, retention, revenue) is the point.
- Be willing to kill your own feature if the data says it did not work. Sunk cost is not a reason to keep it.

## The meta-rule
An expert states the hypothesis, the metric, and what result would make them stop — before building. Conviction about the
problem, humility about the solution. That calibration is the craft.
