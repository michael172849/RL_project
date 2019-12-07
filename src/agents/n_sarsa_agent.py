from agents.agent import Agent
class nSarsaAgent(Agent):
    """
    Base class for agent
    """
    def __init__(
        self, 
        actions : list):
        self.actions = actions      #List of actions


    def getAction(self, state):
        return {'act':self.actions[0].startAction, 'id':0}
    
    def update(self, reward, action, state):
        pass
