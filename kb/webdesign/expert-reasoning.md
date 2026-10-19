# Web design & front-end — expert reasoning layer (how a web expert thinks)

Web reasoning balances three forces that pull against each other: user-perceived performance, accessibility, and
maintainability. The skill is building for the worst realistic device and network first, then enhancing — not the reverse.

## Method (constraints first)
- Design for the constraint, not the demo machine: a mid-range phone on a slow network is the real baseline. What is instant on your laptop can be unusable in the field.
- Performance is perceived, not just measured: get meaningful content on screen fast (minimise render-blocking, prioritise above-the-fold), then load the rest. Users judge the first second.
- Semantic HTML is the foundation of both accessibility and SEO: the right element (button, nav, heading order, labels) gives you keyboard support, screen-reader meaning, and crawlability almost for free. Reaching for a div+JS reimplementation is a smell.
- Progressive enhancement: the core content and actions should work without the heavy JS; enhancement layers on top. A blank page when a script fails is a design failure.

### Worked case — "the page is slow to load"
- Measure what "slow" means: is it time-to-first-content, time-to-interactive, or a janky scroll? Each has a different cause; profile before changing anything.
- Common culprits in order: unoptimised/oversized images, render-blocking JS/CSS, too much JavaScript shipped and executed, and no caching. Attack the biggest byte/blocking cost first.
- Fix with the cheap wins first: right-sized/next-gen images with explicit dimensions, lazy-load below the fold, defer non-critical JS, cache static assets. Measure again on the throttled baseline, not the laptop.
- Verify on a real mid-range device and a throttled network; a Lighthouse score on fast hardware can hide the actual experience.

## Responsiveness and resilience
- Build fluid/responsive from the start; a fixed desktop layout retrofitted to mobile is always worse than mobile-considered-first.
- Handle the failure states: slow image (reserve space to avoid layout shift), offline, empty, and error. The happy path is the easy half.
- Minimise and version your dependencies; every library you ship is bytes the user downloads and a surface you maintain.

## The meta-rule
An expert decides on the real-world baseline device and network and measures there, treating a fast-laptop impression as
unverified. Fast, accessible, and maintainable are not a trade to dodge — they usually come from the same good decisions.
