from radical.entk.appman.wfprocessor import TaskManager
from radical.entk import Pipeline, Stage, Task
import pytest
from radical.entk.exceptions import *
from Queue import Queue

def test_tmgr_process():

    """
    **Purpose**: Test the functions to start and terminate the tmgr process
    """

    res_dict = {
                    'resource': 'local.localhost',
                    'walltime': 40,
                    'cores': 20,
                    'project': 'Random'
                }
    
    os.environ['RADICAL_PILOT_DBURL'] = 'mlab-url'

    rm = ResourceManager(res_dict)

    t = TaskManager(['pendingq'], ['completedq'], 'localhost', rm)
    t.start_manager()
    assert t.check_alive() == True
    t.end_manager()
    assert t.check_alive() == False


def test_heartbeat():

    """
    **Purpose**: Test the functions to start and terminate the heartbeat thread
    """

    res_dict = {
                    'resource': 'local.localhost',
                    'walltime': 40,
                    'cores': 20,
                    'project': 'Random'
                }
    
    os.environ['RADICAL_PILOT_DBURL'] = 'mlab-url'

    rm = ResourceManager(res_dict)

    t = TaskManager(['pendingq'], ['completedq'], 'localhost', rm)
    t.start_heartbeat()
    assert t.check_heartbeat() == True
    t.end_heartbeat()
    assert t.check_heartbeat() == False