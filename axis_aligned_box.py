from __future__ import annotations
import dataclasses
from custom_types import R2, R2Pair
from intersection import pathSegCollision


# bad code; do not use as basis for physics engine

def interpolateFloat(s: float, t: float, x: float) -> R2:
    return s*(1 - x) + t*x

def interpolateR2(s: R2, t: R2, x: float) -> R2:
    s0, s1 = s
    t0, t1 = t
    y = 1 - x
    return (s0*y + t0*x, s1*y + t1*x)


@dataclasses.dataclass
class AxisAlignedBox:
    position: R2
    velocity: R2
    size: R2
    mass: float

    def step(self, force: R2, deltaTime: float) -> None:
        fx, fy = force
        rx, ry = self.position
        vx, vy = self.velocity
        m = self.mass

        ax, ay = fx/m, fy/m
        vx_ = vx + ax*deltaTime
        vy_ = vy + ay*deltaTime
        rx_ = rx + (vx + vx_)/2 * deltaTime
        ry_ = ry + (vy + vy_)/2 * deltaTime

        self.position = rx_, ry_
        self.velocity = vx_, vy_

    def stepped(self, force: R2, deltaTime: float) -> AxisAlignedBox:
        copy = dataclasses.replace(self)
        copy.step(force, deltaTime)
        return copy

    def vertices(self) -> tuple[R2, R2, R2, R2]:
        rx, ry = self.position
        sx, sy = self.size
        hx, hy = sx/2, sy/2
        return (
            (rx - hx, ry - hy),
            (rx - hx, ry + hy),
            (rx + hx, ry - hy),
            (rx + hx, ry + hy),
        )


@dataclasses.dataclass
class AxisAlignedPlatform:
    position: R2
    width: float

    def segment(self) -> R2Pair:
        rx, ry = self.position
        w = self.width
        hw = w/2
        return ((rx - hw, ry), (rx + hw, ry))


@dataclasses.dataclass
class AASystem:
    boxes: list[AxisAlignedBox]
    platforms: list[AxisAlignedPlatform]
    gravAccel: R2

    def step(self, deltaTime: float) -> None:
        gx, gy = self.gravAccel

        for i, b in enumerate(self.boxes):
            b_ = b.stepped((b.mass*gx, b.mass*gy), deltaTime)
            *paths, = zip(b.vertices(), b_.vertices())

            x = (
                min(xs)
            if (xs:=[x for p in paths for pl in self.platforms
                    if (x:=pathSegCollision(p, pl.segment())) is not None]) else
                None
            )

            # bad approximation via interpolation
            b__: AxisAlignedBox
            if x is not None:
                _, ry = b.position
                rx_, ry_ = b_.position
                b__ = dataclasses.replace(
                    b,
                    position=(rx_, interpolateFloat(ry, ry_, x)),
                    velocity=(b_.velocity[0], 0),
                )
            else:
                b__ = b_

            self.boxes[i] = b__
