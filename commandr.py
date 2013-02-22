# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, with_statement

from hashlib import md5
from json import dumps as json_dumps
from meta.utils import path_meta, depends
from path import path
from shovel import task
from subprocess import Popen, PIPE
from sys import exit
from copy import deepcopy
from os import environ
from yaml import load as yaml_load


def config_expand(root, config):
    '''performs format(**root) on all string values in the given dict'''
    if isinstance(config, str):
        return config.format(**root)
    elif isinstance(config, dict):
        for key, value in config.items():
            if isinstance(value, list):
                config[key] = [config_expand(root, x) for x in value]
            else:
                config[key] = config_expand(root, value)
    return config


def config_expand_loop(config):
    '''calls config_expand() until all template vars are replaced / expanded'''
    def dict_hash(data):
        return md5(json_dumps(data, sort_keys=True)).hexdigest()

    last_hash = None
    while True:
        config = config_expand(config, config)
        current_hash = dict_hash(config)

        if last_hash == current_hash:
            break
        else:
            last_hash = current_hash


# see: http://www.xormedia.com/recursively-merge-dictionaries-in-python/
def dict_merge(a, b):
    '''recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and b have a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.'''
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


def config_load():
    '''load the commandr config files from the users home dir and the local
    meta/ folder and merge them together into one'''
    global_config = dict()
    local_config = dict()

    global_config_file = path("$HOME").expand() / ".commandr.yml"
    if global_config_file.exists():
        global_stream = open(global_config_file, 'r')
        global_config = yaml_load(global_stream)

    local_config_file = path_meta() / "commandr.yml"
    if local_config_file.exists():
        local_stream = open(local_config_file, 'r')
        local_config = yaml_load(local_stream)

    return dict_merge(global_config, local_config)


def get_target_for_vendor(target):
    if target == "amazon":
        return "android"
    elif target == "google":
        return "android"
    elif target == "samsung":
        return "android"
    else:
        return target


def run_commands(commands):
    # some settings should contains lists but are None if they're not filled
    if commands is None:
        return

    for command in commands:
        child = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        (stdoutdata, stderrdata) = child.communicate()

        # TODO use --verbose for this?
        if "DEBUG" in environ:
            print command

        if child.returncode != 0:
            print "!!!!! COMMAND FAILED WITH RETURNCODE " + str(child.returncode)
            print command
            if len(stdoutdata) > 0:
                print "!!!!! STDOUT:"
                print stdoutdata
            if len(stderrdata) > 0:
                print "!!!!! STDERR:"
                print stderrdata
            exit(1)


def config_inject_defaults(config, vendor, mode, mainfile, target):
    config["dirs"]["current"] = path(".").realpath()
    config["dirs"]["home"] = path("$HOME").expand()

    config["args"] = dict()
    config["args"]["vendor"] = vendor
    config["args"]["config"] = mode
    config["args"]["mainfile"] = mainfile
    config["args"]["target"] = target
    config["args"]["mainfile_without_ext"] = path(mainfile).namebase


def replace_templates(config):
    for tpl in path(".").walk("*.tpl"):
        new_text = tpl.text().format(**config)
        new_tpl = tpl.parent / tpl.namebase
        new_tpl.write_text(new_text)


def run(vendor, mode, mainfile):
    print "----> Reading configuration files"
    config = config_load()
    target = get_target_for_vendor(vendor)
    config_inject_defaults(config, vendor, mode, mainfile, target)
    config_expand_loop(config)

    print "----> Replacing template files"
    replace_templates(config)

    print "----> Execute app_before commands"
    run_commands(config["commands"]["app_before"]["all"])
    if vendor != target:
        run_commands(config["commands"]["app_before"][target])
    run_commands(config["commands"]["app_before"][vendor])

    print "----> Execute app commands"
    run_commands(config["commands"]["app"]["all"])
    if vendor != target:
        run_commands(config["commands"]["app"][target])
    run_commands(config["commands"]["app"][vendor])

    print "----> Execute app_after commands"
    run_commands(config["commands"]["app_after"]["all"])
    if vendor != target:
        run_commands(config["commands"]["app_after"][target])
    run_commands(config["commands"]["app_after"][vendor])

    print "----> Done"


def detect_mainfile():
    return path(".").glob("*.monkey")[0]


@task
def build(target="all", mode="release", mainfile=None):
    target = target.lower()
    mode = mode.lower()
    if mainfile is None:
        mainfile = detect_mainfile()

    if target == "all":
        for target in ("Amazon", "Google", "Samsung", "iOS"):
            print "##### " + target
            build(target, mode, mainfile)
            print ""
    else:
        run(target, mode, mainfile)
