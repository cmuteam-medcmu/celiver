import os
import sys

import numpy as np
import pandas as pd

class Extract2DFeatures:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @classmethod
    def from_raw(cls, data: pd.DataFrame):
        data.insert(3, 'Sex_F', np.where(data['Sex'] == 'F', 1, 0))
        data.insert(4, 'Sex_M', np.where(data['Sex_F'] == 1, 0, 1))
        data = data.drop('Sex', axis=1)
        data['AFP'] = np.log1p(data['AFP'])
        return cls(data)

    @staticmethod
    def sliding_window_features(series: pd.Series) -> pd.DataFrame:
        a = [j for j in range(series.shape[0])]
        length = 0
        label, data = [], []
        while length < len(a) - 1:
            n_start, n_end = int(length + 1), int(len(a))
            top, bot = sum(a[0:n_start]), sum(a[n_start:n_end])
            divide = 0 if bot == 0 else top / bot
            length += 1
            label.append(f"SW_{int(length)}_{int(20-length)}")
            data.append(divide)
        return label, data
    
    @staticmethod
    def probability_features(series: pd.Series) -> pd.DataFrame:
        a = [j for j in range(series.shape[0])]
        length = 10
        label, data = [], []

        def Prob_Irregular(l: int, cycle: int = 0):
            while cycle <= 20 - (2 * l):
                n_start, n_mid, n_end = int(cycle), int(cycle + l), int(cycle + 2 * l)
                top, bot = sum(a[n_start:n_mid]), sum(a[n_mid:n_end])
                divide = 0 if bot == 0 else top / bot
                cycle += 1
                label.append(f"PI{int(l)}_F{int(cycle)}")
                data.append(divide)

        def Prob_Regular(l: int, Block: int):
            n, locate = 1, []
            while n <= Block:
                start = 0 if n == 1 else end
                end = l * n
                locate.append([n, start, end])
                n += 1
            from itertools import combinations

            for i in combinations(locate, 2):
                block1, block2 = i[0][0], i[1][0]
                top = sum(a[i[0][1] : i[0][2]])
                bot = sum(a[i[1][1] : i[1][2]])
                divide = 0 if bot == 0 else top / bot
                label.append(f"PR{int(l)}_{int(block1)}_{int(block2)}")
                data.append(divide)

        while length > 0:
            if 20 % length == 0:
                block = 20 / length
                Prob_Regular(length, int(block))
            else:
                Prob_Irregular(length)
            length -= 1

        return label, data

    def extract_features(self) -> pd.DataFrame:

        for idx, case in self.data.iterrows():
            s_label, s_feature = self.sliding_window_features(case[7:])
            p_label, p_feature = self.probability_features(case[7:])

            if idx == 0:
                feature_engineer_df = pd.DataFrame(data=[s_feature + p_feature], columns=list(s_label + p_label))
            
            else:
                feature_engineer_df.loc[idx] = s_feature + p_feature

        new_df = pd.concat([self.data.copy(), feature_engineer_df], axis=1)

        return new_df
