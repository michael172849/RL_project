from typing import Iterable
import numpy as np
import math

class QFuncMixed():
    def __init__(self,
                 state_low:np.array,
                 state_high:np.array,
                 num_category:Iterable[int],
                 num_actions:int,
                 num_tilings:int,
                 tile_width:np.array):
        """
        state_low: possible minimum value for each dimension of the continuous state
        state_high: possible maximum value for each dimension of the continuous state
        num_category: possible values for categorical state
        num_actions: the number of possible actions
        num_tilings: # tilings
        tile_width: tile width for each dimension
        """
        self.dim = [num_tilings]
        self.tile_width = tile_width
        self.tiling_feat_start = []
        for idx, low in enumerate(state_low):
            self.dim.append(math.ceil((state_high[idx] - low) / tile_width[idx]) + 1)
            self.tiling_feat_start.append([low - float(i)/num_tilings * tile_width[idx] for i in range(num_tilings)])
        self.dim.extend(num_category)
        self.dim.append(num_actions)
        self.dim = tuple(self.dim)
        self.w = np.zeros((self.feature_vector_len()))

    def num_tilings(self):
        """
        return the number of tilings
        """
        return self.dim[0]

    def feature_vector_len(self) -> int:
        """
        return dimension of feature_vector: d = num_actions * num_tilings * num_tiles
        """
        return np.prod(self.dim)

    def idx(self, tile, s_cont, s_cate, a) -> np.array:
        """
        return the index of the state in this tile
        """
        tile_idx = [tile]
        for idx, feat in enumerate(s_cont):
            tile_idx.append(int((feat - self.tiling_feat_start[idx][tile]) // self.tile_width[idx]))
        tile_idx.append(s_cate)
        tile_idx.append(a)
        return np.ravel_multi_index(tuple(tile_idx), self.dim)

    def __call__(self, s_cont, s_cate, a) -> np.array:
        """
        return the feature vector
        """
        feat_v = np.zeros(self.feature_vector_len())
        for i in range(self.dim[0]):
            feat_v[self.idx(i, s_cont, s_cate, a)] = 1.
        return feat_v

    def update(self, s_cont, s_cate, a, delta):
        """
        update the Q value
        """
        delta = delta / self.num_tilings()
        for i in range(self.dim[0]):
            weight_idx = self.idx(i, s_cont, s_cate, a)
            self.w[weight_idx] += delta

    def compute_value(self, s_cont, s_cate, a):
        """
        return the Q value
        """
        return np.dot(self.w, self.__call__(s_cont, s_cate, a))
