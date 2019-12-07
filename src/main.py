import numpy as np
from deviceAction.ovenAction import OvenAction
from env import Env
from agents.agent import Agent
from agents.n_sarsa_agent import nSarsaAgent
from agents.tc_q import QFuncMixed
from agents.nn_q import QModelWithNN
from rules.coffeeRule import CoffeeRule
from rules.ovenRule import OvenRule
from dataModel import DataModel

def main():
    actions = []
    rules = []
    actions.append(OvenAction(
        name = 'preheat',
        time_cost=300
    ))
    rules.append(OvenRule(
        100.,
        0.1,
        actions[0],
    ))
    model = DataModel("coffee_guy")
    nL = [model.get_num_locations()]
    nA = len(actions) * 2
    low, high = model.get_cont_low_high()
    q_f = QFuncMixed(low, high, nL, nA, 10, np.array([60]))
    nn_f = QModelWithNN(len(low) + len(nL))
    agent = nSarsaAgent(
        actions,
        nn_f,
        20,
        1.0,
        0,
    )

    environ = Env(actions, rules, agent, model)
    environ.run(100)
    
if __name__ == "__main__":
    main()