from state import State
class Rule(object):
    # Init a rule with the required states, device, and reward
    # The rule is checked after any transition.
    def __init__(self, reward, decay):
        self.reward = reward
        self.decay = decay      # decay of reward in seconds
        
    def check(
            self, 
            s:State,):
        pass

    def reset(self):
        pass