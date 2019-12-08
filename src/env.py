# Time, Location(Room Label), Posture
# 
import numpy as np
from typing import Iterable
from agents.agent import Agent
from deviceAction.action import Action
from rules.rule import Rule
from model import Model
from util import sec_to_str
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
        self.done = False

    def reset(self):
        self.model.reset()
        for action in self.actions:
            action.reset()
        self.rules_set = np.zeros(len(self.rules))
        self.prevLoc = "###"
        self.state, self.done = self.model.step(0)

    def step(self, a):
        if self.done:
            return self.state, 0, self.done
        a['act'](self.state['time'])
        r = 0
        for action in self.actions:
            r += action.stepReward(self.state['time'])
        for i,rule in enumerate(self.rules):
            rr = rule.check(self.state)
            if rr > 0:
                self.rules_set[i] = 1
            r += rr
        s, done = self.model.step(30)
        return s, r, done

    def get_feat_from_state(self, state, moreFeature=False):
        if moreFeature:
            feat = self.model.get_cont_cate(state)
            if self.prevLoc =="###":
                self.prevLoc = self.model.get_loc_index(state['loc_cate'])
            extra = [self.prevLoc]              #previous Location
            extra.extend(self.rules_set)        #Is rule met
            feat = feat[0], np.append(feat[1], extra)
            return feat
        else:
            return self.model.get_cont_cate(self.state)
    def run(self, days, moreFeature=False):
        self.moreFeature = True
        for i in range(days):
            self.reset()
            r_s = 0
            print("======Day {}====================================================================".format(i))
            self.feat = self.get_feat_from_state(self.state, moreFeature)
            a = self.agent.getAction(self.feat)
            actions = [a['id']]
            self.rules_set = np.zeros(len(self.rules))
            while not self.done:
                s_p, r, self.done = self.step(a)
                if s_p['loc_cate'] != self.state['loc_cate']:
                    self.prevLoc = self.model.get_loc_index(self.state['loc_cate'])
                # sp_feat = self.model.get_cont_cate(self.state)
                # extra = [prev]
                # extra.extend(self.rules_set)
                sp_feat = self.get_feat_from_state(s_p, moreFeature)
                r_s += r
                # if s_p['act_truth'] in ['Breakfast', 'Wake up', 'PersonalGrooming']:
                # if a['id'] == 1 and i>80:
                #     print (a['id'], s_p['act_truth'], sec_to_str(s_p['time']), s_p['loc_cate'])

                # if a['id'] == 0 and i > 50 and s_p['time']>43200 and r<0:
                #     print (a['id'], self.state, r)
                a = self.agent.update(self.feat, r,a, sp_feat)
                # print(s_p['loc_cate'], self.model.get_cont_cate(s_p)[1])
                actions.append(a['id'])
                self.state =s_p
                self.feat = sp_feat
            print ("Return:{}!!!".format(r_s))
            self.agent.finishEpisode(self.feat)
        
    