from action import Action
from env import Env
from agents.agent import Agent
from agents.n_sarsa_agent import nSarsaAgent
from rules.coffeeRule import CoffeeRule
from rules.ovenRule import OvenRule
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
        0.2,
        actions[0],
    ))
    agent = nSarsaAgent(
        actions
    )
    environ = Env(actions, rules, agent, DataModel("coffee_guy"))
    environ.run(1000)
    
if __name__ == "__main__":
    main()