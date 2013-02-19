# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, with_statement

from path import path
from os.path import dirname
from sh import shovel as depends


def path_data():
    return path(dirname(__file__)) / "data"


def path_meta():
    return path("meta")


def path_generated():
    generated = path_meta() / "generated"

    if not generated.exists():
        generated.mkdir()

    return generated
