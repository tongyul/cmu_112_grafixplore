from __future__ import annotations
import math
import pygame
import random
import sys
from custom_types import R2, R2Pair
from intersection import pathSegCollision as psc
from typing import Final


M_LEFT: Final = 1
M_RIGHT: Final = 3


def interpolR2(a: R2, b: R2, x: float) -> R2:
    a1,a2 = a
    b1,b2 = b
    y = 1 - x
    return (a1*y + b1*x, a2*y + b2*x)


class App:
    windowsize: Final = (600, 400)
    windowpane: pygame.surface.Surface
    running: bool

    rng: random.Random

    linesegs: list[R2Pair]
    pathstart: R2
    pathend: R2

    intersecs: list[R2]
    f_recompute_intersecs: bool

    def __init__(self) -> None:
        W, H = self.windowsize
        self.windowpane = pygame.display.set_mode((W, H), vsync=True)
        self.running = False

        seed = random.randint(0, 0xFFFFFFFF)
        print(f"RNG seed: {seed:X}")
        self.rng = rng = random.Random(seed)

        nsegs = rng.randint(5, 30)
        print(f"Number of line segments: {nsegs}")

        self.linesegs = []
        for _ in range(nsegs):
            self.add_random_seg()

        self.pathstart = (W / 2, H / 2)
        self.pathend = (W, H / 2)

        self.intersecs = []
        self.f_recompute_intersecs = True

    def add_random_seg(self) -> None:
        W, H = self.windowsize
        rng = self.rng
        cx = rng.random() * W
        cy = rng.random() * H
        theta = rng.random() * math.pi
        r = rng.random() * 40 + 10
        dx = math.cos(theta) * r
        dy = math.sin(theta) * r
        p1 = (cx - dx, cy - dy)
        p2 = (cx + dx, cy + dy)
        self.linesegs.append((p1, p2))

    def redraw(self) -> None:
        BLACK = (0,0,0,255)
        GREY = (191,191,191,255)
        RED = (255,0,0,255)
        GREEN = (0,255,0,255)
        BLUE = (0,0,255,255)
        WHITE = (255,255,255,255)
        PT_RADIUS = 3
        PT_WIDTH = 0

        self.windowpane.fill(BLACK)

        for seg in self.linesegs:
            s, e = seg
            pygame.draw.aaline(self.windowpane, GREY, s, e)

        pygame.draw.aaline(self.windowpane, WHITE, self.pathstart, self.pathend)
        pygame.draw.circle(
            self.windowpane, BLUE, self.pathstart, PT_RADIUS, PT_WIDTH)
        pygame.draw.circle(
            self.windowpane, RED, self.pathend, PT_RADIUS, PT_WIDTH)

        for i, pt in enumerate(self.intersecs):
            pygame.draw.circle(
                self.windowpane, WHITE if i else GREEN, pt, PT_RADIUS, PT_WIDTH)

    def recompute_intersecs(self) -> None:
        s = self.pathstart
        e = self.pathend
        dists = [t for l in self.linesegs if (t:=psc((s, e), l)) is not None]
        dists.sort()
        self.intersecs = [interpolR2(s, e, d) for d in dists]

    def update(self) -> None:
        if self.f_recompute_intersecs:
            self.f_recompute_intersecs = False
            self.recompute_intersecs()

    def __call__(self) -> None:
        self.running = True
        while self.running:
            events = pygame.event.get()
            for e in events:

                if e.type == pygame.QUIT:
                    self.running = False

                elif e.type == pygame.MOUSEMOTION and e.buttons[M_LEFT-1]:
                    self.pathend = e.pos
                    self.f_recompute_intersecs = True
                elif e.type == pygame.MOUSEMOTION and e.buttons[M_RIGHT-1]:
                    self.pathstart = e.pos
                    self.f_recompute_intersecs = True
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == M_LEFT:
                    self.pathend = e.pos
                    self.f_recompute_intersecs = True
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == M_RIGHT:
                    self.pathstart = e.pos
                    self.f_recompute_intersecs = True
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    self.add_random_seg()
                    self.f_recompute_intersecs = True

                elif e.type == pygame.MOUSEMOTION: pass
                elif e.type == pygame.MOUSEBUTTONDOWN: pass
                elif e.type == pygame.MOUSEBUTTONUP: pass
                else:
                    print(e)
                    pass

            self.update()
            self.redraw()
            pygame.display.flip()


def main() -> None:
    import shlex

    pygame.init()
    pygame.display.set_caption(
        shlex.join([sys.executable.rsplit('/', 1)[-1]] + sys.argv))
    pygame.key.set_repeat(False)

    app = App()
    app()

    pygame.quit()


if __name__ == '__main__':
    main()
