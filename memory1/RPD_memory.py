# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 18:02:33 2020

@author: azumi
"""

import random
import matplotlib.pyplot as plt
import subprocess


class Player:
    def __init__(self, strategy):
        self.point = 0
        self.strategy = strategy
    
    def decide_action_mem1(self, state):
        # p_0, p_CC, p_CD, p_DC, p_DD
        rnd = random.random()
        
        if state == '0':# 初回のゲーム
            if rnd <= self.strategy['p_0']: return 'C'
            else: return 'D'
        if state == 'CC':
            if rnd <= self.strategy['p_CC']: return 'C'
            else: return 'D'
        if state == 'CD':
            if rnd <= self.strategy['p_CD']: return 'C'
            else: return 'D'
        if state == 'DC':
            if rnd <= self.strategy['p_DC']: return 'C'
            else: return 'D'
        if state == 'DD':
            if rnd <= self.strategy['p_DD']: return 'C'
            else: return 'D'
    
    def get_point(self, point):
        self.point += point

class SimulateGame:
    def __init__(self, max_t):
        self.max_t = max_t
        self.payoff= {'T':1.5,
                      'R':1,
                      'P':0,
                      'S':-0.5}
        
        self.player_x = None
        self.player_y = None
        
    def __stage_game(self, state):
        action_x = self.player_x.decide_action_mem1(state)
        action_y = self.player_y.decide_action_mem1(state)
        
        if action_x == 'C' and action_y == 'C':
            self.player_x.get_point(self.payoff['R'])
            self.player_y.get_point(self.payoff['R'])
            return 'CC'
        
        if action_x == 'C' and action_y == 'D':
            self.player_x.get_point(self.payoff['S'])
            self.player_y.get_point(self.payoff['T'])
            return 'CD'
        
        if action_x == 'D' and action_y == 'C':
            self.player_x.get_point(self.payoff['T'])
            self.player_y.get_point(self.payoff['S'])
            return 'DC'
        
        if action_x == 'D' and action_y == 'D':
            self.player_x.get_point(self.payoff['P'])
            self.player_y.get_point(self.payoff['P'])
            return 'DD'
        
    def __iterated_game(self):
        state = '0'
        for t in range(self.max_t):
            state = self.__stage_game(state)
        
        average_payoff_x = self.player_x.point / self.max_t
        average_payoff_y = self.player_y.point / self.max_t
        
        return average_payoff_x, average_payoff_y
    
    def __plot_result(self, x_list, y_list):
        plt.figure(figsize = (6, 6))
        plt.xlabel('Payoff of Player Y')
        plt.ylabel('Payoff of Player X')
        plt.ylim(-1, 2)
        plt.xlim(-1, 2)
        plt.plot([self.payoff['R'],
                  self.payoff['T'],
                  self.payoff['P'],
                  self.payoff['S'],
                  self.payoff['R']],
        
                 [self.payoff['R'],
                  self.payoff['S'],
                  self.payoff['P'],
                  self.payoff['T'],
                  self.payoff['R']],
                  
                  color = "k")
        plt.rcParams["font.size"] = 18
        plt.grid()
        
        plt.plot(y_list, x_list, "o", color = "g")
        
    def run_python(self):
        x_list, y_list = [], []
        
        for i in range(1000):
            self.player_x = Player({'p_0' :0,
                                    'p_CC':0.86,
                                    'p_CD':0.77,
                                    'p_DC':0.09,
                                    'p_DD':0
                                    })
            
            self.player_y = Player({'p_0' :random.random(),
                                    'p_CC':random.random(),
                                    'p_CD':random.random(),
                                    'p_DC':random.random(),
                                    'p_DD':random.random()
                                    })
            
            payoff_x, payoff_y = self.__iterated_game()
            x_list.append(payoff_x)
            y_list.append(payoff_y)
        
        self.__plot_result(x_list, y_list)
    
    def run_c(self):
        p = (0, 0.86, 0.77, 0.09, 0)
        
        cmd = ["a.exe"] + \
            [str(p[0]),str(p[1]),str(p[2]),str(p[3]),str(p[4])]
        
        proc = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        
        x_list=[]; y_list=[]
        for l in proc.stdout.decode("utf8").split('\n')[:-1]:
            tmp = l.split(',')
            x_list.append(float(tmp[0]))
            y_list.append(float(tmp[1]))
        
        self.__plot_result(x_list, y_list)
        
if __name__ == '__main__':
    max_t = 10000
    # 100000回　シミュレーションでZDが直線に近くなる
    
    game = SimulateGame(max_t)
    game.run_c()
