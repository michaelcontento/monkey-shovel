# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, with_statement

from PIL import Image, ImageFile
from shovel import task
from meta.utils import path_meta, path_generated, depends

ImageFile.MAXBLOCK = 2**20


def save(image, filename):
    image.save(filename, "JPEG", quality=98, optimize=True, progressive=True)


@task
def export():
    depends("meta.pxm.export")

    for filename in path_meta().files("screen-*.png"):
        image = Image.open(filename)

        # crop
        width, height = image.size
        box = (0, height - 768, width, height)
        cropped = image.crop(box)

        # overlay
        name = "".join(filename.namebase.split("-")[1:])
        overlayfile = path_meta() / "overlay-" + name + ".png"
        if overlayfile.exists():
            overlay = Image.open(overlayfile)
            cropped.paste(overlay, None, overlay)

        # save
        for x, y in ((1024, 768), (960, 640), (1136, 640), (1280, 720)):
            resized = cropped.resize((x, y), Image.ANTIALIAS)
            savename = "screen-" + name + "-" + str(x) + "x" + str(y) + ".jpg"
            save(resized, path_generated() / savename)
