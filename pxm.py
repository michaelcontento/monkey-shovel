# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, with_statement

from sh import automator
from shovel import task
from meta.utils import path_data, path_meta
from path import path

WORKFLOW = path_data() / "pxm-export.workflow"


@task
def export(filenames=None):
    if filenames is not None:
        filenames = filenames.split(" ")
    else:
        filenames = path_meta().walk("*.pxm")

    for filename in filenames:
        automator("-i", filename, WORKFLOW)


@task
def export_dir(dirname=None):
    if dirname is None:
        dirname = path_meta()

    for filename in path(dirname).walk("*.pxm"):
        print filename
        automator("-i", filename, WORKFLOW)
