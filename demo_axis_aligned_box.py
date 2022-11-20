from __future__ import annotations
import dataclasses
import time
from cmu_112_graphics.cmu_112_graphics import App, TopLevelApp, WrappedCanvas
from axis_aligned_box import AxisAlignedBox, AxisAlignedPlatform, AASystem
from custom_types import R2
from eventsync import ESync, KeyEventLike, MouseEventLike


@dataclasses.dataclass
class AppData:
    aasys: AASystem
    prevTime: float
    mousePos: R2
    displayScale: float
    def __hash__(self) -> int: return 0  # anti-MVC


def appStarted(app: TopLevelApp) -> None:
    data = AppData(
        aasys=AASystem([], [], (9.8*.5, -9.8*.75**.5)),  # gravity is slanted
        prevTime=time.perf_counter(),
        mousePos=(0, 0),
        displayScale=32,  # 32 px == 1 m
    )
    app.data = data  # type: ignore

@ESync.mouse
def mouseMoved(app: App, event: MouseEventLike) -> None:
    data: AppData = app.data  # type: ignore
    data.mousePos = (event.x, event.y)

@ESync.key
def keyPressed(app: App, event: KeyEventLike) -> None:
    data: AppData = app.data  # type: ignore
    mx, my = data.mousePos
    W, H = app.width, app.height
    DS = data.displayScale

    x, y = (mx - W/2) / DS, (H/2 - my) / DS  # cartesian
    if event.key == '1':
        data.aasys.boxes.append(AxisAlignedBox(
            position=(x, y),
            velocity=(0, 0),
            size=(1, 1),
            mass=1,
        ))
    elif event.key == '2':
        data.aasys.platforms.append(AxisAlignedPlatform(
            position=(x, y),
            width=5,
        ))

@ESync.hook
def timerFired(app: TopLevelApp) -> None:
    data: AppData = app.data  # type: ignore
    currTime = time.perf_counter()
    deltaTime = currTime - data.prevTime

    data.aasys.step(deltaTime)

    data.prevTime = currTime

def redrawAll(app: TopLevelApp, canvas: WrappedCanvas) -> None:
    data: AppData = app.data  # type: ignore
    W, H = app.width, app.height
    DS = data.displayScale

    for b in data.aasys.boxes:
        rx, ry = b.position
        sx, sy = b.size
        rx_, ry_ = rx*DS + W/2, H/2 - ry*DS
        sx_, sy_ = sx*DS, sy*DS
        canvas.create_rectangle(
            round(rx_ - sx_/2), round(ry_ - sy_/2),
            round(rx_ + sx_/2), round(ry_ + sy_/2),
            outline='#FF0000')

    for p in data.aasys.platforms:
        rx, ry = p.position
        w = p.width
        rx_, ry_ = rx*DS + W/2, H/2 - ry*DS
        w_ = w*DS
        canvas.create_line(
            round(rx_ - w_/2), round(ry_),
            round(rx_ + w_/2), round(ry_))


if __name__ == '__main__':
    app = TopLevelApp(autorun=False)
    app.timerDelay = 20
    app.run()
