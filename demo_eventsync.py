from __future__ import annotations
from cmu_112_graphics.cmu_112_graphics import TopLevelApp
from eventsync import ESync
from typing import TypeVar

_T = TypeVar('_T')

def exposed_entries(d: dict[str, _T]) -> dict[str, _T]:
    return {k: v for k, v in d.items() if k and k[0].isalpha()}

def appStarted(app):
    print("appStarted", app)
def appStopped(app):
    print("appStopped", app)
def redrawAll(app, canvas):
    # print("redrawAll", app, canvas)
    ...
@ESync.key
def keyPressed(app, event):
    print("keyPressed", app, event)
    print("event internals:", exposed_entries(event.__dict__))
@ESync.key
def keyReleased(app, event):
    print("keyReleased", app, event)
    print("event internals:", exposed_entries(event.__dict__))
@ESync.mouse
def mousePressed(app, event):
    print("mousePressed", app, event)
    print("event internals:", exposed_entries(event.__dict__))
@ESync.mouse
def mouseReleased(app, event):
    print("mouseReleased", app, event)
    print("event internals:", exposed_entries(event.__dict__))
@ESync.mouse
def mouseMoved(app, event):
    print("mouseMoved", app, event)
    print("event internals:", exposed_entries(event.__dict__))
@ESync.mouse
def mouseDragged(app, event):
    print("mouseDragged", app, event)
    print("event internals:", exposed_entries(event.__dict__))
@ESync.hook
def timerFired(app):
    # print("timerFired", app)
    ...
@ESync.singular
def sizeChanged(app):
    print("sizeChanged", app)

def main() -> None:
    app = TopLevelApp(autorun=False)
    # framerate hack!
    app.timerDelay = 8  # set to 120 FPS cap; the faster the better
    # app.timerDelay = 500  # set to 2 FPS cap; to show delayed event processing
    app.run()

if __name__ == '__main__':
    main()
