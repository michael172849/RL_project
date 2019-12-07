from action import Action
from env import Env
from agent import *
from rules import *
from dataModel import DataModel

def main():
    actions = []
    rules = []
    actions.append(Action(
        name = 'preheat',
        time_cost=300
    ))
    rules.append(OvenRule(
        100.,
        0.2
    ))
    agent = nSarsaAgent(
        actions
    )
    environ = Env(actions, rules, agent, DataModel("coffee_guy"))

    for i in range(100):
        environ.step()
    
if __name__ == "main":
    main()