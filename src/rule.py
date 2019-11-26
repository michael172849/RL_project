class Rule():

    # Init a rule with the required states, device, and reward
    # The rule is checked after any transition.
    def __init__(self, reward, decay):
        self.reward = reward
        self.decay = decay
        

    def check(
            self, 
            s:State,):
        pass