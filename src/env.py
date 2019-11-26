# Time, Location(Room Label), Posture
# 
from agent import Agent
from action import Action
class Env():
    def __init__(self, 
                actions: Iterable[Action]):
        super().__init__()
        self.actions = actions
        self.agent = Agent(actions)

    def step(self):
        r = 0
        for action in self.actions:
            r += action.reward()
        
        for rule in self.rules:
            r += rule.checkRule()
    
        a = self.agent.getAction
        
    