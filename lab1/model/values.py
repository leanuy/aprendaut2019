# Combinacion lineal de los atributos y minimos cuadrados
# N-upla(termino independiente w0,
#        lineas 2 libres, lineas 2 amenazadas, lineas 2 inutiles,
#        lineas 3 libres, lineas 3 amenazadas, lineas 3 inutiles,
#        lineas 4 libres, lineas 4 amenazadas, lineas 4 inutiles
#        lineas 5)

# MAIN --------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------------------------

class Values():

    # CONSTRUCTOR ---------------------------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------------------------------------------
    
    def __init__(self):
        self.est_function = ([0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1], [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])
        self.learn_rate = 0.5

    # GETTERS & SETTERS ---------------------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------------------------------------------
    
    def get_est_function(self):
        return self.est_function

    def set_est_function(self, function):
        self.est_function = function

    def get_learn_rate(self):
        return self.learn_rate

    def set_learn_rate(self, rate):
        self.learn_rate = rate

    # METHODS -------------------------------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Using the current function, estimate board value
    def estimate_value(self, move):
        (b_est_function, w_est_function) = self.est_function
        tot = sum(i[0]*i[1] for i in zip(b_est_function, move[0])) + sum(i[0]*i[1] for i in zip(w_est_function, move[1]))
        return tot
    
    # Generate pair (board, Vtrain(board)) from a given board list
    def assign_train_value(self, boards):
        train_values = []

        for i in range (0, len(boards)-1):
            vtrain = self.estimate_value(boards[i+1])
            train_values.append((boards[i], vtrain))

        (b_last, w_last) = boards[-1]
        if b_last[10] > 0:
            train_values.append((boards[-1], 1))
        elif w_last[10] > 0:
            train_values.append((boards[-1], -1))
        else:
            train_values.append((boards[-1], 0))

        return train_values

    # Adjust Vop weights based in LMS using the difference between Vop(board) and Vtrain(board)
    def update_est_function (self, train_values):

        (b_est_function, w_est_function) = self.est_function
        
        for ((b_board, w_board), v_train) in train_values:
            for i in range (0, len(b_board)):
                b_est_function[i] = b_est_function[i] + self.learn_rate*(v_train - self.estimate_value((b_board, w_board)))*b_board[i]
                w_est_function[i] = w_est_function[i] + self.learn_rate*(v_train - self.estimate_value((b_board, w_board)))*w_board[i]

        self.est_function = (b_est_function, w_est_function)
