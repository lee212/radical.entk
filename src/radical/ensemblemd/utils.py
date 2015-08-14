#!/usr/bin/env python

"""A collection of various utilities and helper functions.
"""

__author__    = "Ole Weider <ole.weidner@rutgers.edu>"
__copyright__ = "Copyright 2015, http://radical.rutgers.edu"
__license__   = "MIT"

import datetime
import math
import numpy as np

#------------------------------------------------------------------------------
#
def extract_timing_info(units, pattern_start_time_abs, step_start_time_abs, step_end_time_abs):
    """
    This function extracts timing from a set of CUs:

      * t_id_E: start of earliest input data staging operation
      * t_id_L: end of last input data staging operation
      * t_od_E: start of earliest output data staging operation
      * t_od_L: end of last output data staging operation
      * t_ex_E: start of earliest execution
      * t_ex_L: end of last last execution

    Timings are returned both as absolute and as relative measures.
    """
    #step_start_time_rel = step_start_time_abs - pattern_start_time_abs
    #step_end_time_rel = step_end_time_abs - pattern_start_time_abs

    step_execution_time_abs = None
    step_data_movement_time_abs = None

    step_total_time = step_end_time_abs - step_start_time_abs
    #all_id_start = []; all_od_start = []; all_ex_start = []
    #all_id_stop = []; all_od_stop = []; all_ex_stop = []

    all_id_dur_list = []
    all_od_dur_list = []
    all_ex_dur_list = []

    #t_id_E_abs = None; t_od_E_abs = None; t_ex_E_abs = None; t_startup_E_abs = None
    #t_id_L_abs = None; t_od_L_abs = None; t_ex_L_abs = None; t_startup_L_abs = None

    #t_id_E_rel = None; t_od_E_rel = None; t_ex_E_rel = None
    #t_id_L_rel = None; t_od_L_rel = None; t_ex_L_rel = None

    #Iterate through all the units of the stage/step and extract the timestamps
    for unit in units:

        missing_state_ip = False
        missing_state_op = False

        ex_start    = 0
        ex_stop     = 0
        id_start    = 0
        id_stop     = 0
        od_start    = 0
        od_stop     = 0


        #Execution time:
        if ((unit.start_time is not None) and (unit.stop_time is not None)):
            ex_start = unit.start_time
            ex_stop = unit.stop_time

        #Input Staging time + Output Staging time:
        for state in unit.state_history:

            #Input Staging start time:
            #To account for missing states, use both states - PendingInputStaging & StagingInput - using flags
            if state.state == "PendingInputStaging":
                if state.timestamp is not None:
                    id_start = state.timestamp
            else:
                missing_state_ip = True

            if ((missing_state_ip==True)and(state.state == "StagingInput")):
                if state.timestamp is not None:
                    id_start = state.timestamp
                else:
                    continue

            #Input Staging stop time:
            if state.state == "PendingExecution":
                if state.timestamp is not None:
                    id_stop = state.timestamp


            #Output Staging start time:
            #To account for missing states, use both states - PendingAgentOutputStaging & AgentStagingOutput - using flags
            if state.state == "PendingAgentOutputStaging":
                if state.timestamp is not None:
                    od_start = state.timestamp
            else:
                missing_state_op = True

            if ((missing_state_op==True)and(state.state == "AgentStagingOutput")):
                if state.timestamp is not None:
                    od_start = state.timestamp
                else:
                    continue

            #Output Staging stop time:
            if state.state == "Done":
                if state.timestamp is not None:
                    od_stop = state.timestamp

        all_ex_dur_list.append((ex_stop - ex_start).total_seconds())
        all_id_dur_list.append((id_stop - id_start).total_seconds())
        all_od_dur_list.append((od_stop - od_start).total_seconds())

    # Find the earliest / latest timings from the timing arrays
    '''
    if len(all_id_start) > 0:
        t_id_E_abs = min(all_id_start)
    if len(all_id_stop) > 0:
        t_id_L_abs = max(all_id_stop)
    if len(all_od_start) > 0:
        t_od_E_abs = min(all_od_start)
    if len(all_od_stop) > 0:
        t_od_L_abs = max(all_od_stop)
    if len(all_ex_start) > 0:
        t_ex_E_abs = min(all_ex_start)
    if len(all_ex_stop) > 0:
        t_ex_L_abs = max(all_ex_stop)
    '''

    #cases when CU does not reach PendingExecution Step
    '''
    if t_id_L_abs is None:
        t_id_L_abs = t_ex_E_abs
    '''

    # Determine the time 'origin' for relative timings
    '''
    if t_id_E_abs is not None:
        t_origin = t_id_E_abs
    else:
        t_origin = t_ex_E_abs

    if len(all_id_start) > 0:
        t_id_E_rel = step_start_time_rel + t_id_E_abs - t_origin
    if len(all_id_stop) > 0:
        t_id_L_rel = step_start_time_rel + t_id_L_abs - t_origin
    if len(all_od_start) > 0:
        t_od_E_rel = step_start_time_rel + t_od_E_abs - t_origin
    if len(all_od_stop) > 0:
        t_od_L_rel = step_start_time_rel + t_od_L_abs - t_origin
    if len(all_ex_start) > 0:
        t_ex_E_rel = step_start_time_rel + t_ex_E_abs - t_origin
    if len(all_ex_stop) > 0:
        t_ex_L_rel =step_start_time_rel +  t_ex_L_abs - t_origin
    '''

    '''
    #Old dataframe
    return {
        "step_start_time": {
            "abs": step_start_time_abs,
        #    "rel": step_start_time_rel
        },
        "step_end_time": {
            "abs": step_end_time_abs,
        #    "rel": step_end_time_rel
        },
        "first_data_stagein_started": {
            "abs": t_id_E_abs,
        #    "rel": t_id_E_rel
        },
        "last_data_stagein_finished": {
            "abs": t_id_L_abs,
        #    "rel": t_id_L_rel
        },

        "first_data_stageout_started": {
            "abs": t_od_E_abs,
        #    "rel": t_od_E_rel
        },
        "last_data_stageout_finished": {
            "abs": t_od_L_abs,
        #    "rel": t_od_L_rel
        },

        "first_execution_started": {
            "abs": t_ex_E_abs,
        #    "rel": t_ex_E_rel
        },
        "last_execution_finished": {
            "abs": t_ex_L_abs,
        #    "rel": t_ex_L_rel
        }
    }
    '''

    return {
        "execution_time": {
                "average":np.average(all_ex_dur_list),
                "error": (np.std(all_ex_dur_list)/len(all_ex_dur_list))
                },
        "data_movement_time": {
            "average": np.average(all_id_dur_list)+np.average(all_od_dur_list),
            "error": (math.sqrt(np.var(all_id_dur_list) + np.var(all_od_dur_list)))/len(all_id_dur_list)
             },
            
        "step_time": (step_end_time_abs - step_start_time_abs).total_seconds(),
        }
    

#------------------------------------------------------------------------------
#
def dataframes_from_profile_dict(profile):

    try:
        import pandas as pd
    except Exception, ex:
        print ex
        return None

    #cols = ['pattern_entity', 'value_type', 'first_started_abs', 'last_finished_abs','first_started_rel', 'last_finished_rel']
    #cols = ['pattern_entity', 'value_type', 'first_started_abs', 'last_finished_abs']
    cols = ['pattern_entity','value_type','average duration', 'error']
    df = pd.DataFrame(columns=cols)

    # iterate over the entities
    for entity in profile:
        #start_abs = entity['timings']['step_start_time']['abs']
        #end_abs = entity['timings']['step_end_time']['abs']
        step_duration_abs = entity['timings']['step_time']
        #start_rel = entity['timings']['step_start_time']['rel']
        #end_rel = entity['timings']['step_end_time']['rel']
        #df2 = pd.DataFrame([[entity['name'], 'pattern_step', start_abs, end_abs, start_rel, end_rel]],columns=cols)
        df2 = pd.DataFrame([[entity['name'], 'pattern_step', step_duration_abs,0]],columns=cols)
        df = df.append(df2, ignore_index=True )

        #start_abs = entity['timings']['first_data_stagein_started']['abs']
        #end_abs   = entity['timings']['last_data_stagein_finished']['abs']
        #start_rel = entity['timings']['first_data_stagein_started']['rel']
        #end_rel   = entity['timings']['last_data_stagein_finished']['rel']
        #df2 = pd.DataFrame([[entity['name'], 'data_stagein', start_abs, end_abs, start_rel, end_rel]],columns=cols)
        #df2 = pd.DataFrame([[entity['name'], 'data_stagein', start_abs, end_abs]],columns=cols)
        #df = df.append(df2, ignore_index=True )

        #start_abs = entity['timings']['first_execution_started']['abs']
        #end_abs   = entity['timings']['last_execution_finished']['abs']
        execution_time_average = entity['timings']['execution_time']['average']
        execution_time_error = entity['timings']['execution_time']['error']
        #start_rel = entity['timings']['first_execution_started']['rel']
        #end_rel   = entity['timings']['last_execution_finished']['rel']
        #df2 = pd.DataFrame([[entity['name'], 'execution', start_abs, end_abs, start_rel, end_rel]],columns=cols)
        df2 = pd.DataFrame([[entity['name'], 'execution', execution_time_average,execution_time_error]],columns=cols)
        df = df.append(df2, ignore_index=True )

        #start_abs = entity['timings']['first_data_stageout_started']['abs']
        #end_abs   = entity['timings']['last_data_stageout_finished']['abs']
        data_movement_time_average = entity['timings']['data_movement_time']['average']
        data_movement_time_error = entity['timings']['data_movement_time']['error']
        #start_rel = entity['timings']['first_data_stageout_started']['rel']
        #end_rel   = entity['timings']['last_data_stageout_finished']['rel']
        #df2 = pd.DataFrame([[entity['name'], 'data_stageout', start_abs, end_abs, start_rel, end_rel]],columns=cols)
        df2 = pd.DataFrame([[entity['name'], 'data_movement', data_movement_time_average,data_movement_time_error]],columns=cols)
        df = df.append(df2, ignore_index=True )

    return df
