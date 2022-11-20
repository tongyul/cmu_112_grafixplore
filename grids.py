from __future__ import annotations
import json
import tkinter as tk
from PIL import Image, ImageTk
from cmu_112_graphics.cmu_112_graphics import TopLevelApp, WrappedCanvas
from custom_types import R2
from functools import cache
from typing import Any, Final
from util import RCSDIR, TXRDIR, MAPDIR


class BlockSpec:

    texture: Image.Image | None
    mapLegend: tuple[int, int, int]

    def __init__(self, data) -> None:
        ver = data['blockspec_version']
        if ver == 1:
            self.__init_specver_1(data)
        else:
            raise ValueError(f"blockspec_version {ver!r} is not recognized")

    def __init_specver_1(self, data) -> None:
        txrName = data['texture']
        if txrName is None:
            self.texture = None
        else:
            self.texture = Image.open(TXRDIR/txrName)
        self.mapLegend = tuple(data['map_legend'])  # type: ignore

    @cache
    def scaled_texture(self, sidelen: int) -> Image | None:
        if self.texture is None:
            return None
        else:
            w, h = self.texture.size
            resample: Any
            if sidelen % w == 0 and sidelen % h == 0:
                # integer up-scaling
                resample = Image.Resampling.NEAREST
            elif sidelen < (w*h)**.5:
                # down-scaling
                resample = Image.Resampling.BOX
            else:
                resample = Image.Resampling.BICUBIC

            return self.texture.resize((sidelen, sidelen), resample=resample)

    def scaled_texture_tk(self, sidelen: int) -> ImageTk.PhotoImage | None:
        if self.texture is None:
            return None
        else:
            return ImageTk.PhotoImage(self.scaled_texture(sidelen))


BLOCK_SPECS: Final = {
    k: BlockSpec(v) for k, v in
        json.load((RCSDIR/'block_types.json').open()).items() }
BLOCK_INVREF: Final = { v.mapLegend: k for k, v in BLOCK_SPECS.items() }


class Grid:

    size: tuple[int, int]
    blocks: list[list[str]]

    def __init__(self, mapName: str) -> None:
        mapImg = Image.open(MAPDIR/mapName).convert(mode='RGB')
        w, h = mapImg.size
        self.size = w, h
        self.blocks = [
            [BLOCK_INVREF[mapImg.getpixel((i,j))] for j in range(h)]
            for i in range(w) ]

    def draw(
            self,
            app: TopLevelApp,
            canvas: WrappedCanvas,
            blockSidelen: int,
            originCartesian: R2,
            ) -> None:
        w, h = self.size
        a = blockSidelen
        oriX, oriY = map(round, originCartesian)
        appW, appH = app.width, app.height
        _gridW, gridH = w*a, h*a
        oriY = gridH - oriY  # from Cartesian to Window
        minX = appW // 2 - oriX
        minY = appH // 2 - oriY

        for ix, col in enumerate(self.blocks):
            for iy, blockKind in enumerate(col):
                txr = BLOCK_SPECS[blockKind].scaled_texture_tk(a)
                if txr is not None:
                    x = minX + ix*a
                    y = minY + iy*a
                    canvas.create_image(x, y, image=txr, anchor=tk.NW)
