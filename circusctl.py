#!/bin/python
# -*- coding: utf-8 -*-
'''
:maintainer: Moeen Mirjalili (momirjalili@gmail.com)
:maturity: 16.07.2016
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


def list_(name=None):
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
    try:
        watchers = _send_message("list", name=name)
    except CallError as ce:
            return ce.message
    return watchers.get("watchers") or watchers.get("pids")


def version():
    '''
    Returns installed circus version.

    CLI Example:

        salt '*' circusctl.version
    '''
    return ".".join(map(str, circus.version_info))


def stats(name=None, process=None, extended=None):
    '''
    Get process infos
    =================

    You can get at any time some statistics about your processes
    with the stat command.

    CLI Example:
        salt '*' circusctl.stats
        salt '*' circusctl.stats name
        salt '*' circusctl.stats name process
        salt '*' circusctl.stats name process True
    '''
    try:
        stats = _send_message("stats",
                              name=name,
                              process=process,
                              extended=extended)
    except CallError as ce:
        return ce.message
    return stats.get('infos') or stats.get('info')


def status():
    '''
    Get the status of a watcher or all watchers
    ===========================================

    This command start get the status of a watcher or all watchers.
    '''
    statuses = _send_message("status")
    return statuses["statuses"]


def options(name):
    '''
    Get the value of all options for a watcher
    ==========================================

    This command returns all option values for a given watcher.
    '''
    options = _send_message("options", name=name)
    return options["options"]


def dstats():
    '''
    Get circusd stats
    =================

    You can get at any time some statistics about circusd
    with the dstat command.
    '''
    dstats = _send_message("dstats")
    return dstats


def start(name):
    '''
    Start the arbiter or a watcher
    ==============================

    This command starts all the processes in a watcher or all watchers.
    '''
    result = _send_message("start", name=name)
    return result["status"]


def stop(name):
    '''
    '''
    result = _send_message("stop", name=name)
    return result["status"]


def reload(name):
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
    result = _send_message("reload", name=name)
    return result["status"]


def signal(name, signum, pid=None, childpid=None, children=False,
           recursive=False):
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


def _send_message(command, **properties):
    # check if circusct.endpoint is in minion config
    endpoint = __salt__['config.get']('circusctl.endpoint') or \
                DEFAULT_ENDPOINT_DEALER
    log.debug(endpoint)
    props = dict((k, v) for k, v in properties.iteritems() if v)
    log.debug(properties)
    log.debug(props)
    client = CircusClient(endpoint=endpoint)
    result = client.send_message(command, **props)
    return result
