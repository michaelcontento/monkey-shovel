# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, with_statement

from PIL import Image
from shovel import task
from meta.utils import path_meta, path_generated, path_data, depends


SIZES = ((320, 480), (640, 960), (640, 1136),
        (768, 1024), (1024, 768),
        (1536, 2048), (2048, 1536))


@task
def resize(size=SIZES):
    depends("meta.pxm.export")

    landscape = Image.open(path_meta() / "loading.png")
    portrait = landscape.rotate(90)

    for x, y in SIZES:
        if x > y:
            image = landscape
        else:
            image = portrait

        name = "loading-" + str(x) + "x" + str(y) + ".png"
        resized = image.resize((x, y), Image.ANTIALIAS)
        resized.save(path_generated() / name, "PNG")
