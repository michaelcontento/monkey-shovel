# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, with_statement

from sh import automator
from shovel import task
from meta.utils import path_data, path_meta

WORKFLOW = path_data() / "pxm-export.workflow"


@task
def export(filenames=None):
    if filenames is not None:
        filenames = filenames.split(" ")
    else:
        filenames = path_meta().walk("*.pxm")

    for filename in filenames:
        automator("-i", filename, WORKFLOW)
