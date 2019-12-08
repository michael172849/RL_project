import numpy as np
from deviceAction.ovenAction import OvenAction
from env import Env
from baselineEnv import BaselineEnv
from agents.agent import Agent
from agents.n_sarsa_agent import nSarsaAgent
from agents.e_trace_agent import ETraceAgent
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
        200.,
        0.5,
        actions[0],
    ))
    model = DataModel("coffee_guy")
    nL = [model.get_num_locations(), model.get_num_locations()]
    nL.extend([2]*len(rules))
    nA = len(actions) * 2
    low, high = model.get_cont_low_high()
    q_f = QFuncMixed(low, high, nL, nA, 5, np.array([4800]))
    nn_f = QModelWithNN(low, high, nL, nA, 0.001)
    agent = nSarsaAgent(
        actions,
        q_f,
        20,
        1.0,
        0.1,
    )
    # agent = ETraceAgent(
    #     actions,
    #     q_f,
    #     1.0,
    #     0.,
    #     0.1,
    # )

    environ = Env(actions, rules, agent, model)
    environ.run(500)
    
def baseline():
    actions = []
    rules = []
    actions.append(OvenAction(
        name = 'preheat',
        time_cost=300
    ))
    rules.append(OvenRule(
        200.,
        0.5,
        actions[0],
    ))
    model = DataModel("coffee_guy")
    env = BaselineEnv(actions, rules, model)
    env.run(500)
if __name__ == "__main__":
    # main()
    baseline()