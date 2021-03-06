# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, with_statement

from PIL import Image
from shovel import task
from meta.utils import path_meta, path_generated, path_data, depends


SIZES = (36, 48, 57, 72, 76, 96, 114, 120, 135, 144, 152, 256, 512, 1024)


@task
def resize(size=SIZES):
    depends("meta.pxm.export")

    icon = Image.open(path_meta() / "icon.png")
    rounded = Image.open(path_data() / "icon-mask.png")
    rounded.paste(icon, None, rounded)

    for size in SIZES:
        for image, suffix in ((icon, ""), (rounded, "rounded-")):
            name = "icon-" + suffix + str(size) + "x" + str(size) + ".png"
            resized = image.resize((size, size), Image.ANTIALIAS)

            if size == 135:
                resized.save(path_generated() / name.replace(".png", ".jpg"), "JPEG", quality=100, optimize=True, progressive=True)
            else:
                resized.save(path_generated() / name, "PNG")
