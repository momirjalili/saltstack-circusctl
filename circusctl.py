#!/bin/python
# -*- coding: utf-8 -*-
'''
:maintainer: Moeen Mirjalili (momirjalili@gmail.com)
:maturity: 16July2016
:requires: none
:platform: all
'''
try:
    import circus
    from circus.client import CircusClient
    from circus.util import DEFAULT_ENDPOINT_DEALER
    from circus.exc import CallError
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

import salt.utils
import logging

__func_alias__ = {
    'list_': 'list',
}

log = logging.getLogger(__name__)

__virtualname__ = "circusctl"

def __virtual__():
    '''
    '''
    if not salt.utils.which('circusctl'):
        return False
    if HAS_LIBS:
        return __virtualname__
    return False


def list_(endpoint=None):
    '''
    '''
    watchers = _send_message("list", endpoint=endpoint)
    return watchers["watchers"]


def version():
    '''
    Returns installed circus version.

    CLI Example:

        salt '*' circusctl.version
    '''
    return ".".join(map(str, circus.version_info))


def stats(endpoint=None):
    '''
    '''
    stats = _send_message("stats", endpoint=endpoint)
    return stats["infos"]


def status(endpoint=None):
    '''
    '''
    statuses = _send_message("status", endpoint=endpoint)
    return statuses["statuses"]


def options(name, endpoint=None):
    '''
    '''
    options = _send_message("options", name=name, endpoint=endpoint)
    return options["options"]


def dstats(endpoint=None):
    '''
    '''
    dstats = _send_message("dstats", endpoint=endpoint)
    return dstats


def start(name, endpoint=None):
    '''
    '''
    result = _send_message("start", name=name, endpoint=endpoint)
    return result["status"]


def stop(name, endpoint=None):
    '''
    '''
    result = _send_message("stop", name=name, endpoint=endpoint)
    return result["status"]


def reload(name, endpoint=None):
    '''
    '''
    result = _send_message("reload", name=name, endpoint=endpoint)
    return result["status"]


def signal(name, signum, pid=None, childpid=None, children=False,
           recursive=False, endpoint=None):
    '''
    '''
    result = _send_message(
        "signal",
        name=name,
        signum=signum,
        pid=pid,
        childpid=childpid,
        recursive=recursive,
        endpoint=endpoint
    )
    return result["status"]


def _send_message(command, endpoint=None, **props):
    if not endpoint:
        endpoint = DEFAULT_ENDPOINT_DEALER
    client = CircusClient(endpoint=endpoint)
    try:
        result = client.send_message(command, **props)
    except CallError as ce:
            return ce.message
    return result
