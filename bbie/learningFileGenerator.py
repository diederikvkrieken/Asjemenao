from copy import deepcopy
import pickle
'''
This is the storage file generator ful multiple-version behaviour learning.

To generate a storage file, import this file and run create_ML_file(args)

!Remember to re-import if you ran this with non-default values for some of the arguments!
!Otherwise, things may not work as you intend!
'''

def create_ML_file(goal, behavior_name, id_list, max_duration, top_nr, use_lower=True, confidence_level=95, min_to_train=5, max_tries = 10):
    '''
    goal is the location of the file to be written to.
    behavior_name is the name fo the behavior the file is for, without the underscore of the number.
    id_list is a list of behavior id's to use/learn for.
    max_duration is a maximum cutoff time for the behavior
    top_nr is the number of results which should be returned when selecting behaviors.
    use_lower determines if you use the lower bound of the confidence interval (faster = better) or the upper one (longer = better)
    confidence_level is the confidence level for the interval in percents (95 for 95%).
    min_to_train is the minimum number of times each behavior has to be executed before training is considered complete.
    '''
    # Check the inputs.
    if not isinstance(goal, str):
        raise SyntaxError("goal should be a string!")
    if not isinstance(behavior_name, str):
        raise SyntaxError("behavior_name should be a string!")
    if not isinstance(id_list, list):
        raise SyntaxError("idlist should be a list!")
    if not isinstance(use_lower, bool):
        raise SyntaxError("use_lower should be a boolean!")
    if not (isinstance(confidence_level, int) or isinstance(confidence_level, float)):
        raise SyntaxError("confidence_level should be an int or float!")
    if not isinstance(top_nr, int):
        raise SyntaxError("top_nr should be an int!")
    if not isinstance(max_duration, int):
        raise SyntaxError("max_duration should be an int!")
    if not isinstance(min_to_train, int):
        raise SyntaxError("min_to_train should be an int!")
    
    # Generate the list of dicts for the behavior versions.
    behaviors = range(len(id_list))
    for i in behaviors:
        behaviors[i] = {'id': id_list[i], 'completion_times': [], 'non_cutoff_times': [], 'failed_times': [], 'upper': deepcopy(max_duration), 'lower': 0, 'times_completed': 0, 'times_run': 0, 'times_failed': 0}
    
    # Add this list and the other values to a dict.
    usedDict = {'behavior_name': behavior_name, 'behaviors': behaviors, 'use_lower': use_lower, 'confidence_level': confidence_level, 'top_nr': top_nr, 'max_duration': max_duration, 'training_completed': False, 'min_to_train': min_to_train, 'max_tries': max_tries}
    
    # And create the file.
    output=open(goal, 'wb')
    pickle.dump(usedDict, output)
    output.close()  
