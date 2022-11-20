from __future__ import annotations
import dataclasses
from cmu_112_graphics.cmu_112_graphics import TopLevelApp, WrappedCanvas
from grids import Grid
# from eventsync import ESync


@dataclasses.dataclass
class AppData:
    grid: Grid
    def __hash__(self) -> int: return 0  # anti-MVC


def appStarted(app: TopLevelApp) -> None:
    data = AppData(
        grid=Grid('samplemap.png'),
    )
    app.data = data  # type: ignore

def redrawAll(app: TopLevelApp, canvas: WrappedCanvas) -> None:
    data: AppData = app.data  # type: ignore
    canvas.create_rectangle(0, 0, app.width, app.height, fill='#94CFE5')
    data.grid.draw(app, canvas, 48, (384, 384))


if __name__ == '__main__':
    app = TopLevelApp(autorun=False)
    app.timerDelay = 15  # approx 30 FPS
    app.run()
