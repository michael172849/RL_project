from action import Action
from rule import Rule
from env import Env
from agent import Agent
from coffeeRule import CoffeeRule
def main():
    actions = []
    rules = []
    actions.append(Action(
        name = 'coffee',
        time_cost=300
    ))
    rules.append(CoffeeRule(
        100.,
        0.2
    ))
    environ = Env(actions, rules)
    
if __name__ == "main":
    main()