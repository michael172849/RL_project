# Time, Location(Room Label), Posture
# 
from typing import Iterable
from agent.agent import Agent
from action import Action
from rules.rule import Rule
from model import Model
class Env():
    def __init__(self, 
                actions: Iterable[Action],
                rules: Iterable[Rule],
                agent: Agent,
                model: Model,
                ):
        self.actions = actions
        self.agent = agent
        self.rules = rules
        self.model = model
        self.state = None

    def reset(self):
        self.model.reset()
        self.state = self.model.state

    def step(self):
        if self.state is None:
            self.reset()
        r = 0
        for action in self.actions:
            r += action.stepReward(self.state['time'])
        
        for rule in self.rules:
            r += rule.check()
    
        a = self.agent.getAction(self.state)
        a['act'](self.state['time'])
        self.agent.update(r, a, self.state)
        self.model.step()
        self.state = self.model.state
        
    