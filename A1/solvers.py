class SentenceCorrector(object):
    def prep_conf_matrix_transpose(self):
        self.conf_matrix_T = {}
        for key, values in self.conf_matrix.items():
            for val in values:
                if(val not in self.conf_matrix_T):
                    self.conf_matrix_T[val] = [val]
                self.conf_matrix_T[val].append(key)
    
    def replace_char(self, string, char, pos):
        stringList = list(string)
        stringList[pos] = char
        stringList = "".join(stringList)
        return stringList

    def permute_with_window(self, string, istart, size, iter):
        possible_corrections = self.get_value(self.conf_matrix_T, self.best_state[iter])
        for correction in possible_corrections:
            newString = string + correction
            if(iter == istart+size-1):
                neighbor = self.best_state[:istart] + newString + self.best_state[iter+1:]
                if(self.cost_fn(neighbor) < self.cost_fn(self.best_state)):
                    self.best_state = neighbor
            else:
                self.permute_with_window(newString, istart, size, iter+1)

    def greedy_search(self, window):
        for iter in range(0, len(self.best_state)-window+1):
            self.curCost = self.cost_fn(self.best_state)
            self.permute_with_window("",iter,window,iter)

    def get_value(self, matrix, char):
        possible_errors = [char]
        if(char in matrix):
            possible_errors = matrix[char]
        return possible_errors

    def __init__(self, cost_fn, conf_matrix):
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn

        # You should keep updating following variable with best string so far.
        self.best_state = None
        
        self.prep_conf_matrix_transpose() 
        
    def search(self, start_state):

        self.best_state = start_state
        self.greedy_search(3)
        # print("Final cost: {}".format(self.cost_fn(self.best_state)))