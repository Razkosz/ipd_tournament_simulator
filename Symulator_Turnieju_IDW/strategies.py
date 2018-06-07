import numpy as np
from numpy.random import randint as los
from numpy.random import rand
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier



class Strategy:
    def __init__(self, badly=False):
        self.bad = badly
    def decision(self, loyd, lood):
        if 1:
            return 1
        else:
            return 0

# Always cooperates
class Good(Strategy):
    def decision(self, loyd, lood):
        return 0


# Always defects
class Bad(Strategy):
    def decision(self, loyd, lood):
        return 1


# Makes same decision as its opponent previous decision*
class TitForTat:
    def __init__(self, badly=False, generous=0, tats=1):
        self.bad = badly
        self.tats = tats
        if tats > 1 and generous > 1:
            self.generous = 1/float(generous)
        else:
            self.generous = float(generous)

    def decision(self, loyd, lood):
        if len(lood) == 0:
            if self.bad is True:
                return 1
            else:
                return 0
        if sum(lood[-self.tats:]) == self.tats:
            if self.generous > 2:
                if lood.count(1) % self.generous == 0:
                    return 0
                else:
                    return 1
            elif 0.0 < self.generous < 1.0:
                dont_forgive = rand()
                if dont_forgive > self.generous:
                    return 1
                else:
                    return 0
            else:
                return 1
        else:
            return 0


# Makes another decision than in previous decision
class Undecided:
    def __init__(self, badly=False):
        self.bad = badly

    def decision(self, loyd, lood):
        if len(loyd) == 0:
            if self.bad is True:
                return 1
            else:
                return 0
        if loyd[-1] == 1:
            return 0
        else:
            return 1


# Cooperates as long as opponent, then defects unforgivably
class Grudger:
    def __init__(self, calm=0):
        self.calm = calm
        self.trigger = False

    def decision(self, loyd, lood):
        if len(loyd) == 0:
            self.trigger = False
            return 0
        if sum(lood) <= self.calm:
            return 0
        else:
            self.trigger = True
            return 1


class SoftGrudger:
    def __init__(self):
        self.grudge = []

    def decision(self, loyd, lood):
        if len(loyd) == 0:
            self.grudge = []
            return 0
        if self.grudge:
            return self.grudge.pop()
        if 1 in lood:
            self.grudge = [0,0,1,1,1,1]
            return self.grudge.pop()
        else:
            return 0


# Repeat last decision if it was Reward or Temptation and change decision if it was Sucker or Punishment
class Pavlov:
    def __init__(self, badly=False, generous=0):
        self.bad = badly
        self.generous = generous

    def decision(self, loyd, lood):
        if len(loyd) == 0:
            if self.bad is True:
                return 1
            else:
                return 0
        if lood[-1] == 1:
            if (loyd[-1]-1)*(-1) == 1:
                forgive = np.random.choice([0,1], p=[self.generous,1-self.generous])
                return forgive
            return (loyd[-1]-1)*(-1)
        return loyd[-1]


# Make N cooperates, then N defects, then make decision which gives better average score
class Adaptive:
    def __init__(self, matrix, len_adapt=5):
        self.avg_c = 0
        self.avg_d = 0
        self.matrix = [matrix[0][0],matrix[1][0][0],matrix[1][1][0],matrix[2][0]]
        self.len_adapt = len_adapt

    def decision(self, loyd, lood):
        if len(loyd) <= self.len_adapt:
            self.avg_c = 0
            self.avg_d = 0
            return 0
        elif len(loyd) <= 2* self.len_adapt:
            return 1
        else:
            self.get_averages(loyd, lood)
            if self.avg_c > self.avg_d:
                return 0
            elif self.avg_c == self.avg_d:
                return (loyd[-1]-1)*(-1)
            else:
                return 1

    def get_averages(self, loyd, lood):
        raw_c = []
        raw_d = []
        for i in range(len(loyd)):
            if loyd[i] == 0:
                if lood[i] == 0:
                    raw_c.append(self.matrix[0])
                elif lood[i] == 1:
                    raw_c.append(self.matrix[2])
            if loyd[i] == 1:
                if lood[i] == 0:
                    raw_d.append(self.matrix[1])
                elif lood[i] == 1:
                    raw_d.append(self.matrix[3])
        if not raw_d:
            self.avg_d = 0
        else:
            self.avg_d = sum(raw_d) / len(raw_d)
        if not raw_c:
            self.raw_c = 0
        else:
            self.avg_c = sum(raw_c) / len(raw_c)


class Random:
    def __init__(self, defect_with=0.5):
        self.defect_with = defect_with

    def decision(self, loyd, lood):
        decision = np.random.choice([1, 0], p=[self.defect_with, 1-self.defect_with])
        return decision


class Detective:
    def decision(self, loyd, lood):
        if len(loyd) in (0, 2, 3):
            return 0
        if len(loyd) == 1:
            return 1
        if 1 in lood:
            return lood[-1]
        else:
            return 1


class TwoTitsForTat:
    def __init__(self):
        self.trigger = False

    def decision(self, loyd, lood):
        if self.trigger is True:
            self.trigger = False
            return 1
        if len(loyd) == 0:
            self.trigger = False
            return 0
        else:
            if lood[-1] == 1:
                self.trigger = True
                return 1
            return 0


####### My strategies

class UndecidedTitForTat(Strategy):
    def decision(self, loyd, lood):
        if len(loyd) == 0:
            if self.bad is True:
                return 1
            else:
                return 0
        else:
            if lood[-1] == 1:
                return np.random.choice([0, 1], p=[0.25, 0.75])
            else:
                return np.random.choice([0, 1], p=[0.75, 0.25])


class Mistrustful(Strategy):
    def decision(self, loyd, lood):
        if len(loyd) == 0:
            return 0
        if sum(loyd[-2:]) == 2:
            return 0
        elif sum(lood[-3:]) == 0:
            return 1
        elif loyd[-1] == 1:
            return 1
        else:
            return 0


class Bandit(Strategy):
    def decision(self, loyd, lood):
        if len(loyd) == 0:
            return 0
        elif 0 < len(loyd) < 6:
            return 1
        else:
            stay_blended = rand()
            if loyd[-1] == 0 and stay_blended >= 0.75:
                return 0
            blend_in = np.random.choice([2,3,4,5],p=[0.2,0.4,0.25,0.15])
            if sum(loyd[-blend_in:]) == blend_in:
                return 0
            else:
                return 1


class SimplyThinker:
    def __init__(self, source_path="logic_strategy_5.csv"):
        training_set = pd.DataFrame.from_csv(source_path, index_col=None)
        t_x = training_set.iloc[:, 1:]
        t_y = training_set.iloc[:, 0]
        self.k_nearest = KNeighborsClassifier(n_neighbors=5)
        self.k_nearest.fit(t_x, t_y)
        self.recognise_opp = ""

    def test_algorithm(self, test_set_path="test_set_5.csv"):
        test_set = pd.DataFrame.from_csv(test_set_path, index_col=None)
        tt_x = test_set.iloc[:, 1:]
        tt_y = test_set.iloc[:, 0]
        print self.k_nearest.score(tt_x, tt_y)

    def decision(self,loyd,lood):
        if len(loyd) in [0,3,4]:
            return 0
        elif len(loyd) in [1,2]:
            return 1
        if len(loyd) == 5:
            self.recognise_opp = self.k_nearest.predict(np.array(lood).reshape(1, -1))
        if self.recognise_opp == "titfortat":
            return 0
        if self.recognise_opp == "grudge":
            return 1
        if self.recognise_opp == "good":
            return 1
        if self.recognise_opp == "bad":
            return 1
        if self.recognise_opp == "titfortwotat":
            if loyd[-1] == 0:
                return 1
            else:
                return 0
        if self.recognise_opp == "pavlov":
            return 0
        if self.recognise_opp == "undecided":
            return 1


class HardlyThinker:
    def __init__(self, source_path = "logic_strategy_9.csv"):
        training_set = pd.DataFrame.from_csv(source_path, index_col=None)
        t_x = training_set.iloc[:, 1:]
        t_y = training_set.iloc[:, 0]
        self.k_nearest = KNeighborsClassifier(n_neighbors=5)
        self.k_nearest.fit(t_x, t_y)
        self.recognise_opp = ""

    def test_algorithm(self, test_set_path="test_set_9.csv"):
        test_set = pd.DataFrame.from_csv(test_set_path, index_col=None)
        tt_x = test_set.iloc[:, 1:]
        tt_y = test_set.iloc[:, 0]
        print self.k_nearest.score(tt_x, tt_y)

    def decision(self,loyd,lood):
        if len(loyd) in [0,3,4,6,8]:
            return 0
        elif len(loyd) in [1,2,5,7]:
            return 1
        if len(loyd) == 9:
            self.recognise_opp = self.k_nearest.predict(np.array(lood).reshape(1, -1))
        if self.recognise_opp == "titfortat":
            return 0
        if self.recognise_opp == "grudger":
            return 1
        if self.recognise_opp == "good":
            return 1
        if self.recognise_opp == "bad":
            return 1
        if self.recognise_opp == "titfortwotat":
            if loyd[-1] == 0:
                return 1
            else:
                return 0
        if self.recognise_opp == "pavlov":
            return 0
        if self.recognise_opp == "undecided":
            return 1
        if self.recognise_opp == "detective":
            return 0


class EasyGoingSimplyThinker:
    def __init__(self, source_path="logic_strategy_5.csv"):
        training_set = pd.DataFrame.from_csv(source_path, index_col=None)
        t_x = training_set.iloc[:, 1:]
        t_y = training_set.iloc[:, 0]
        self.k_nearest = KNeighborsClassifier(n_neighbors=5)
        self.k_nearest.fit(t_x, t_y)
        self.recognise_opp = ""
        self.start_mla = False

    def test_algorithm(self, test_set_path="test_set_5.csv"):
        test_set = pd.DataFrame.from_csv(test_set_path, index_col=None)
        tt_x = test_set.iloc[:, 1:]
        tt_y = test_set.iloc[:, 0]
        print self.k_nearest.score(tt_x, tt_y)

    def decision(self,loyd,lood):
        if len(loyd) < 3:
            self.start_mla = False
            return 0
        if 1 in lood:
            if self.start_mla is False:
                st_mla = []
                st_mla.append(lood.index(1)+1)
                if len(loyd) in [st_mla[0], st_mla[0]+3, st_mla[0]+4]:
                    return 0
                elif len(loyd) in [st_mla[0]+1, st_mla[0]+2]:
                    return 1
                if len(loyd) == st_mla[0]+5:
                    self.recognise_opp = self.k_nearest.predict(np.array(lood[-5:]).reshape(1, -1))
                    self.start_mla = True
            if self.recognise_opp == "titfortat":
                return 0
            if self.recognise_opp == "grudge":
                return 1
            if self.recognise_opp == "good":
                return 1
            if self.recognise_opp == "bad":
                return 1
            if self.recognise_opp == "titfortwotat":
                if loyd[-1] == 0:
                    return 1
                else:
                    return 0
            if self.recognise_opp == "pavlov":
                return 0
            if self.recognise_opp == "undecided":
                return 1
        else:
            return 0


class EasyGoingTftSimplyThinker:
    def __init__(self, source_path="logic_strategy_5.csv"):
        training_set = pd.DataFrame.from_csv(source_path, index_col=None)
        t_x = training_set.iloc[:, 1:]
        t_y = training_set.iloc[:, 0]
        self.k_nearest = KNeighborsClassifier(n_neighbors=5)
        self.k_nearest.fit(t_x, t_y)
        self.recognise_opp = ""

    def test_algorithm(self, test_set_path="test_set_5.csv"):
        test_set = pd.DataFrame.from_csv(test_set_path, index_col=None)
        tt_x = test_set.iloc[:, 1:]
        tt_y = test_set.iloc[:, 0]
        print self.k_nearest.score(tt_x, tt_y)

    def decision(self,loyd,lood):
        if len(loyd) < 3:
            return 0
        if 1 in lood[0:3]:
            if len(loyd) in [3,6,7]:
                return 0
            elif len(loyd) in [4,5]:
                return 1
            if len(loyd) == 8:
                self.recognise_opp = self.k_nearest.predict(np.array(lood[-5:]).reshape(1, -1))
            if self.recognise_opp == "titfortat":
                return 0
            if self.recognise_opp == "grudge":
                return 1
            if self.recognise_opp == "good":
                return 1
            if self.recognise_opp == "bad":
                return 1
            if self.recognise_opp == "titfortwotat":
                if loyd[-1] == 0:
                    return 1
                else:
                    return 0
            if self.recognise_opp == "pavlov":
                return 0
            if self.recognise_opp == "undecided":
                return 1
        else:
            return lood[-1]


class TitTatTitForTat:
    def __init__(self):
        self.trigger = 0

    def decision(self, loyd, lood):
        if len(loyd) == 0:
            self.trigger = 0
            return 0
        if self.trigger > 0:
            self.trigger -= 1
            return self.trigger % 2
        if lood[-1] == 1:
            self.trigger = 3
            return 1
        else:
            return 0


class LetsMakeCeaseFire:
    def __init__(self, war=3, peace=3, intensity=0.75 ):
        self.war = -1
        self.peace = 0
        self.intensity = intensity
        self.restart = [war, peace, intensity]

    def decision(self, loyd, lood):
        if len(loyd) == 0:
            self.war, self.peace, self.intensity = -1, 0, self.intensity
            return 0
        if self.war > 0:
            self.war -= 1
            return 1
        if self.war == 0:
            choice = np.random.choice([0,1], p=[1-self.intensity, self.intensity])
            if self.intensity >= 0.1:
                self.intensity -= 0.1
            if choice == 0:
                self.war = -1
                self.peace = self.restart[1]
                self.intensity = self.restart[2]
            return choice
        if self.peace > 0:
            self.peace -= 1
            return 0
        if lood[-1] == 0:
            return 0
        if lood[-1] == 1:
            self.war = self.restart[0]
            return 1


class TitForTatWithoutLooping:
    def decision(self, loyd, lood):
        if len(loyd) == 0:
            return 0
        else:
            if loyd[-4:] == [1,0,1,0] and lood[-4:] == [0,1,0,1]:
                return 0
            else:
                return lood[-1]


class AveragedTitForTat:
    def __init__(self, matrix):
        self.avg_c = 0
        self.avg_d = 0
        self.matrix = [matrix[0][0],matrix[1][0][0],matrix[1][1][0],matrix[2][0]]
        self.R = matrix[0][0]
        self.T = matrix[1][0][0]
        self.S = matrix[1][1][0]
        self.P = matrix[2][0]

    def decision(self, loyd, lood):
        if len(loyd) == 0:
            return 0
        if len(loyd) <= 10:
            return lood[-1]
        # if len(loyd) % 30 == 0:
        #     return 1
        self.get_averages(loyd, lood)
        if lood[-1] == 0:
            cop = (self.avg_c-self.S)/(self.R-self.S)
            return np.random.choice([0, 1], p=[cop, 1-cop])
        else:
            defc = (self.avg_d-self.P)/(self.T-self.P)
            return np.random.choice([0, 1], p=[1-defc, defc])
        # if self.avg_c > self.avg_d:
        #     return 0
        # else:
        #     return 1

    def get_averages(self, loyd, lood):
        raw_c = []
        raw_d = []
        for i in range(len(loyd)):
            if loyd[i] == 0:
                if lood[i] == 0:
                    raw_c.append(self.matrix[0])
                elif lood[i] == 1:
                    raw_c.append(self.matrix[2])
            if loyd[i] == 1:
                if lood[i] == 0:
                    raw_d.append(self.matrix[1])
                elif lood[i] == 1:
                    raw_d.append(self.matrix[3])
        if not raw_d:
            self.avg_d = self.P
        else:
            self.avg_d = sum(raw_d) / len(raw_d)
        if not raw_c:
            self.raw_c = self.S
        else:
            self.avg_c = sum(raw_c) / len(raw_c)
