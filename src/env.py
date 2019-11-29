# Time, Location(Room Label), Posture
# 
from agent import Agent
from action import Action
from rule import Rule
class Env():
    def __init__(self, 
                actions: Iterable[Action],
                rules: Iterable[Rule]):
        self.actions = actions
        self.agent = Agent(actions)
        self.rules = rules

    def step(self):
        r = 0
        for action in self.actions:
            r += action.reward()
        
        for rule in self.rules:
            r += rule.checkRule()
    
        a = self.agent.getAction
        
    