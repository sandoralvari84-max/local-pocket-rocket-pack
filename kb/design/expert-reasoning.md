# Design (UX/UI) — expert reasoning layer (how a design expert thinks)

Design reasoning starts from the user's goal and context, not from taste. The skill is reducing the user's effort and
error, and justifying every element by the job it does — "looks nice" is not a reason, "lowers the cost of the next action" is.

## Method (user goal first)
- Start from the user's goal and context of use: what are they trying to accomplish, in what state (rushed, stressed, one-handed on a phone)? Design for that, not for the demo.
- Reduce cognitive and physical load: fewer choices at each step, sensible defaults, recognition over recall. Every field and option is a tax on the user.
- Make the right action obvious and the wrong/irreversible action hard (confirmation, undo). Prevent errors by design, and make the ones that happen cheap to recover from.
- Hierarchy carries meaning: what is biggest/first/boldest should be what matters most. If everything is emphasised, nothing is.

### Worked case — "users abandon our signup form"
- Start from the user's effort: count the fields and decisions; each one is a reason to quit. Ask what you truly need now vs can collect later.
- Find where they drop (analytics on the funnel), then look at THAT step for friction: unclear ask, surprise requirement, an error that blocks with no recovery.
- Reduce before you redesign: remove optional fields, defer the rest, show progress, validate inline with helpful not punitive errors. Smaller ask beats prettier form.
- Verify with real users (even 5), not opinion: watch them attempt it; the point of failure is usually not where the team guessed.

## Consistency and accessibility
- Consistency is a feature: the same pattern should look and behave the same everywhere, so users transfer learning instead of relearning.
- Accessibility is not optional polish — sufficient contrast, keyboard paths, labels, adequate touch targets — it widens the audience and usually improves usability for everyone.
- Follow platform and web conventions unless you have a strong, tested reason; novelty in interaction is usually a cost paid by the user.

## The meta-rule
An expert states the user goal a design serves and tests it against real behaviour, treating their own taste as a hypothesis.
The best design is often the one the user does not notice because nothing got in their way.
