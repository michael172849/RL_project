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

    for i in range(100):
        environ.step()
    
if __name__ == "main":
    main()