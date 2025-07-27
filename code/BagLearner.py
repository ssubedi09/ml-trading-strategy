import numpy as np
from scipy import stats

def get_mode(y):
    if len(y) == 0:
        return 0
    values, counts = np.unique(y, return_counts=True)
    return values[np.argmax(counts)]

#generate random bags
def generate_random_bags(M):
    return [np.random.randint(0, M) for i in range(M)]

class BagLearner(object):
    def __init__(self, learner, kwargs = {}, bags = 20, boost = False, verbose = False):
        #constructor
        self.learner = learner
        self.bags = bags
        self.boost = boost
        self.verbose = verbose

        #Initialize learners
        learners = []
        for i in range(self.bags):
            learners.append(self.learner(**kwargs))
        self.learners = learners
        pass

    def author(self):
        #gatech username
        return "ssubedi33"

    def study_group(self):
        #No study group
        return "ssubedi33"

    def add_evidence(self, data_x, data_y):
        # Run each model for different set of datas
        for model in self.learners:
            #random selection with replacement
            random_index = generate_random_bags(data_x.shape[0])
            data_x_upd = data_x[random_index, :]
            data_y_upd = data_y[random_index]
            #train
            model.add_evidence(data_x_upd, data_y_upd)
        pass

    def query(self, points):
        output = []# Query in each model
        for model in self.learners:
            output.append(model.query(points))
        output = np.array(output)
        #calculate mode
        result = []

        #mod of each bag
        for i in range(output.shape[1]):
            mod = []
            for j in range(output.shape[0]):
                mod.append(output[j, i])
            result.append(get_mode(mod))
        return result