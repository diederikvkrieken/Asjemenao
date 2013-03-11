

'''DO NOT MODIFY THIS FILE!!!!'''
'''this class is generated by a script (generate_behaviors.py) that generates a class for each behavior'''
'''changes to this file will be overwritten!'''

import basebehavior.abstractbehavior

import time #TODO: temp, remove later
import os
import os.path
import memory
import logging
import util.nullhandler
import bbie.bbie

'''"This behavior will move the Nao around until the ball is seen in the middle of the FoV."'''

class FindBall(basebehavior.abstractbehavior.AbstractBehavior):

    def behavior_init():
        bbie_setting = ["no_time","max_succes"] #TODO: get this from behavior_config
        self.bbie = bbie.BBIE(self.name, bbie_setting)
        self.logger = logging.getLogger('Borg.Brain.Behavior.' + self.get_name())
        self.logger.addHandler(util.nullhandler.NullHandler())

    def get_name(self):
        return "FindBall"

    def check_postcondition(self):
        m = memory.Memory()
        return eval("m.is_now('ball_found',['True'])")

    def load_exceptions(self):
        self._all_exceptions = []

    def select_implementation(self):
        '''select which of the implementations of this behavior should be run'''

        #destroy (possibly) the old running behavior
        self.selected_implementation = None

        if (self._best_behaviors == None or len(self._best_behaviors) == 0):
            #best_behaviors will be returned as a list of tuples of (expected_time, implementation)
            self._best_behaviors = bbie.bbie.get_best_implementations(os.environ['BORG']+"/brain/src/bbie/ie_files/"+self.get_name().lower()+".pkl")
            #self._best_behaviors = [(time.time() + 50000, 1)] #TODO: remove, and enable line above

        #take top behavior from the list, and remove it from the list
        if (isinstance(self._best_behaviors, list) and len(self._best_behaviors)>0):
            # This is the default case where multiple versions are returned.
            to_run = self._best_behaviors[0]
            self._best_behaviors = self._best_behaviors[1:]

            self._expected_time, b_id = to_run
            self._implementation_id = b_id
        else:
            # In thsi case, no versions are returned.
            self._expected_time = 86400
            self._implementation_id = 1

        #now select the implementation:
        cleanname = self.simple_name(self.name)
        zero_path = os.environ['BORG'] + "/brain/src/behavior/" + cleanname + "/" + cleanname + "_0.py"

        #if a _0 implementation exists, run that one:
        if (os.path.exists(zero_path)):
            module = self.name.lower() + "_0"
        else:
            module = self.name.lower() + "_" + str(b_id)
        exec("import " + module)
        selected_class = self.find_class(eval(module))
        if not selected_class:
            raise Exception("No implementation available in selected file " + module)

        self.selected_implementation = selected_class(self)

        #pass the params the newly selected implementation:
        self.selected_implementation.set_params(self.params)
