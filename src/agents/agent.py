class Agent():
    """
    Base class for agent
    """
    def __init__(
        self, 
        actions : list):
        self.actions = actions      #List of actions


    def getAction(self, state):
        return actions[0].startAction, 0
    
    def update(self, reward, action, state, s_p):
        pass
