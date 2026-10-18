# Software engineering — practices (mentor-curated seed, round 1)

## Software development life cycle (SDLC)
- Phases: requirements → design → implementation → testing → deployment → maintenance.
- Waterfall runs them in sequence; Agile runs them in short iterations with feedback.
- Agile Manifesto values: individuals & interactions, working software, customer collaboration, responding to change.

## Methodologies
- Scrum: fixed-length sprints, backlog, daily standup, review, retrospective; roles product owner / scrum master / team.
- Kanban: continuous flow, limit work-in-progress, pull work as capacity frees.

## Test-driven development (TDD)
- Red–green–refactor: write a failing test, make it pass simply, then clean up.
- Benefits: design pressure toward small units, a safety net, living documentation.
- Test pyramid: many unit, fewer integration, few end-to-end tests.

## CI/CD
- Continuous Integration: merge to main often; every push runs automated build + tests.
- Continuous Delivery/Deployment: automated pipeline to staging/production behind gates.
- Keep the build green; fast feedback; one-click (or automatic) reproducible deploys.

## Design patterns (Gang of Four categories)
- Creational: Factory, Builder, Singleton. Structural: Adapter, Decorator, Facade, Composite.
- Behavioural: Strategy, Observer, Command, State, Iterator.
- Patterns are a shared vocabulary; apply when the problem fits, don't force them.

## Refactoring
- Improve internal structure without changing behaviour; rely on tests to stay safe.
- Smells: long methods, duplicated code, large classes, long parameter lists, feature envy.
- Common moves: extract function/variable, rename, inline, introduce parameter object.

## Principles
- DRY, KISS, YAGNI; SOLID for OO design; separation of concerns; high cohesion, low coupling.
- Code is read far more than written — optimise for the reader.

## Sources (authoritative)
- Agile Manifesto — https://agilemanifesto.org/
- Refactoring (Martin Fowler) — https://refactoring.com/
- Refactoring Guru (patterns & smells) — https://refactoring.guru/
- Scrum Guide — https://scrumguides.org/
- Google Engineering Practices — https://google.github.io/eng-practices/
