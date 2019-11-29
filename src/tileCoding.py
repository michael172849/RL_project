import numpy as np
import math
class StateActionFeatureVectorWithTile():
    def __init__(self,
                 state_low:np.array,
                 state_high:np.array,
                 num_actions:int,
                 num_tilings:int,
                 tile_width:np.array):
        """
        state_low: possible minimum value for each dimension in state
        state_high: possible maimum value for each dimension in state
        num_actions: the number of possible actions
        num_tilings: # tilings
        tile_width: tile width for each dimension
        """
        # TODO: implement here
        self.dim = [num_tilings]
        self.tile_width = tile_width
        self.tiling_feat_start = []
        for idx, low in enumerate(state_low):
            self.dim.append(math.ceil((state_high[idx] - low) / tile_width[idx]) + 1)
            self.tiling_feat_start.append([low - float(i)/num_tilings * tile_width[idx] for i in range(num_tilings)])
        self.dim.append(num_actions)
        self.dim = tuple(self.dim)

    def feature_vector_len(self) -> int:
        """
        return dimension of feature_vector: d = num_actions * num_tilings * num_tiles
        """
        # TODO: implement this method
        return np.prod(self.dim)

    def __call__(self, s, done, a) -> np.array:
        """
        implement function x: S+ x A -> [0,1]^d
        if done is True, then return 0^d
        """
        feat_v = np.zeros(self.feature_vector_len())
        if done:
            return feat_v
        for i in range(self.dim[0]):
            tile_idx = [i]
            for idx, feat in enumerate(s):
                tile_idx.append(int((feat - self.tiling_feat_start[idx][i]) // self.tile_width[idx]))
            tile_idx.append(a)
            feat_v[np.ravel_multi_index(tuple(tile_idx), self.dim)] = 1.
        return feat_v
