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
    Only load the module if circus is installed.
    '''
    if not salt.utils.which('circusctl'):
        return False
    if HAS_LIBS:
        return __virtualname__
    return False


def list_(name=None, endpoint=None):
    '''
    Get list of watchers or processes in a watcher
    The response return the list asked. the mapping returned can either be
    'watchers' or 'pids' depending the request.

    CLI Example:

    To get the list of all the watchers:
        salt '*' circusctl.list

    To get the list of active processes in a watcher:
        salt '*' circusctl.list watcher_name
    '''
    watchers = _send_message("list", name=name, endpoint=endpoint)
    return watchers.get("watchers") or watchers.get("pids")


def version():
    '''
    Returns installed circus version.

    CLI Example:

        salt '*' circusctl.version
    '''
    return ".".join(map(str, circus.version_info))


def stats(endpoint=None):
    '''
    Get process infos
    =================

    You can get at any time some statistics about your processes
    with the stat command.
    '''
    stats = _send_message("stats", endpoint=endpoint)
    return stats["infos"]


def status(endpoint=None):
    '''
    Get the status of a watcher or all watchers
    ===========================================

    This command start get the status of a watcher or all watchers.
    '''
    statuses = _send_message("status", endpoint=endpoint)
    return statuses["statuses"]


def options(name, endpoint=None):
    '''
    Get the value of all options for a watcher
    ==========================================

    This command returns all option values for a given watcher.
    '''
    options = _send_message("options", name=name, endpoint=endpoint)
    return options["options"]


def dstats(endpoint=None):
    '''
    Get circusd stats
    =================

    You can get at any time some statistics about circusd
    with the dstat command.
    '''
    dstats = _send_message("dstats", endpoint=endpoint)
    return dstats


def start(name, endpoint=None):
    '''
    Start the arbiter or a watcher
    ==============================

    This command starts all the processes in a watcher or all watchers.
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
    Reload the arbiter or a watcher
    ===============================

    This command reloads all the process in a watcher or all watchers. This
    will happen in one of 3 ways:

    * If graceful is false, a simple restart occurs.
    * If `send_hup` is true for the watcher, a HUP signal is sent to each
      process.
    * Otherwise:
        * If sequential is false, the arbiter will attempt to spawn
          `numprocesses` new processes. If the new processes are spawned
          successfully, the result is that all of the old processes are
          stopped, since by default the oldest processes are stopped when
          the actual number of processes for a watcher is greater than
          `numprocesses`.
        * If sequential is true, the arbiter will restart each process
          in a sequential way (with a `warmup_delay` pause between each
          step)
    '''
    result = _send_message("reload", name=name, endpoint=endpoint)
    return result["status"]


def signal(name, signum, pid=None, childpid=None, children=False,
           recursive=False, endpoint=None):
    '''
    Send a signal
    =============

    This command allows you to send a signal to all processes in a watcher,
    a specific process in a watcher or its children.
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


def _send_message(command, endpoint=None, **properties):
    if not endpoint:
        endpoint = DEFAULT_ENDPOINT_DEALER
    if properties and all(properties.values()):
        props = properties
    else:
        props = {}
    client = CircusClient(endpoint=endpoint)
    try:
        result = client.send_message(command, **props)
    except CallError as ce:
            return ce.message
    return result
