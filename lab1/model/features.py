# DEPENDENCIES ------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------
import numpy as np

# MAIN --------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------

class Features():

    # METHODS -------------------------------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------------------------------------------

    # Given a board's matrix, returns corresponding features normalized by euclidean norm
    def get_features(self, matrix):

        diags = [matrix[::-1,:].diagonal(i) for i in range(-matrix.shape[0]+1,matrix.shape[1])]
        diags.extend(matrix.diagonal(i) for i in range(matrix.shape[1]-1,-matrix.shape[0],-1))
        (ret_row_b, ret_row_w) = self.count_lines(matrix)
        (ret_col_b, ret_col_w) = self.count_lines(matrix.transpose())
        (ret_diag_b, ret_diag_w) = self.count_lines(diags)
        ret_b = [x + y + z for (x, y), z in zip(zip(ret_row_b, ret_col_b), ret_diag_b)]
        ret_w = [x + y + z for (x, y), z in zip(zip(ret_row_w, ret_col_w), ret_diag_w)]
        
        # To multiply by w0
        ret_b[0] = 1
        ret_w[0] = 1

        # Concatenate vectors to get its euclidean norm
        ret = np.concatenate([ret_b, ret_w])
        norm = np.linalg.norm(ret)
        
        # Normalize features
        for i in range(0, 11):
            if norm != 0:
                ret_b[i] = ret_b[i] / norm
                ret_w[i] = ret_w[i] / norm

        return (ret_b, ret_w)

    # Auxiliar method
    def count_lines(self, rows):
        ret_b = [0,0,0,0,0,0,0,0,0,0,0]
        ret_w = [0,0,0,0,0,0,0,0,0,0,0]
        cur_b = 0
        cur_w = 0
        for row in rows:
            threat_lvl_b = 1
            threat_lvl_w = 1
            for value in row:
                if value == 1:
                    ret_b[0] = ret_b[0] + 1
                    cur_b = cur_b + 1
                    if cur_w > 1:
                        i = self.select_index(cur_w, threat_lvl_w + 1)
                        ret_w[i] = ret_w[i] + 1
                    cur_w = 0
                    threat_lvl_w = 1
                elif value == 2:
                    ret_w[0] = ret_w[0] + 1
                    cur_w = cur_w + 1
                    if cur_b > 1:
                        i = self.select_index(cur_b, threat_lvl_b + 1)
                        ret_b[i] = ret_b[i] + 1
                    cur_b = 0
                    threat_lvl_b = 1
                else:
                    if cur_w > 1:
                        i = self.select_index(cur_w, threat_lvl_w)
                        ret_w[i] = ret_w[i] + 1
                    if cur_b > 1:
                        i = self.select_index(cur_b, threat_lvl_b)
                        ret_b[i] = ret_b[i] + 1
                    cur_w = 0
                    cur_b = 0
                    threat_lvl_b = 0
                    threat_lvl_w = 0
            if cur_w > 1:
                i = self.select_index(cur_w, threat_lvl_w + 1)
                ret_w[i] = ret_w[i] + 1
            if cur_b > 1:
                i = self.select_index(cur_b, threat_lvl_b + 1)
                ret_b[i] = ret_b[i] + 1
            cur_w = 0
            cur_b = 0
            threat_lvl_b = 0
            threat_lvl_w = 0
        return (ret_b, ret_w)

    # Auxiliar method
    def select_index(self, cur, threat_lvl):
        if cur > 4:
            return 10
        else:
            return 3*(cur-2) + threat_lvl + 1
