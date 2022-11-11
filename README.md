# cmu_112_grafixplore

Truth: `cmu_112_graphics.py` ~~sucks~~ isn't that great. Here we explore better
ways to use it.

## OK. But what exactly does this do?

Oh you know, cool stuff, like,

`ESync` singleton object from `eventsync.py` exports decorators for
synchronizing event processing to the call to `timerFired`, so you won't have
to worry about race conditions when making a game with it. (Fun fact: objects
are closures in disguise, and *vice versa*!)

`intersection.py` exports `intersection` and `pathSegCollision` for basically
computing line segment intersections given endpoints, and can be used for e.g.
continuous collision detection, although more work is needed for performance.

`grids.py` is *supposed* to make it easy to create grid-based maps for 2D games.
There's nothing in it yet.

More physics simulation stuff may come later.

## How can I use this?

Use as a reference for your own 15-112 term projects, if… you're a 112 student.
I don't think the Integrity policy allows directly using the code here? Or you
can cite it and then use it, I guess?

## But why are you doing this?

…It's fun? …Procrastination, kinda.
