import numpy as np

def build_tree(data_x, data_y, leaf_size):
    #Edge case if number of rows is less than or equal to leaf_size
    if data_x.shape[0] <= leaf_size or data_x.shape[0] == 1:
        return np.asarray([["leaf", np.mean(data_y), None, None]])
    #if all y values are same
    elif np.all(data_y == data_y[0]):
        return np.asarray([["leaf", data_y[0], None, None]], dtype=object)
    else:
        #Find best feature
        best_feature = np.random.randint(0, data_x.shape[1])
        #best value to split
        split_val = np.median(data_x[:, best_feature])
        #when data cannot be split with median
        if data_x[data_x[:, best_feature] > split_val].shape[0] == 0:
            split_val = np.mean(data_x[:, best_feature])
        #when right subtree is empty
        if split_val == max(data_x[:, best_feature]):
            return np.array([['leaf', np.mean(data_y), None, None]])
        #when left subtree is empty
        if split_val == min(data_x[:, best_feature]):
            return np.array([['leaf', np.mean(data_y), None, None]])
        #left tree
        left_tree = build_tree(data_x[data_x[:, best_feature] <= split_val],data_y[data_x[:, best_feature] <= split_val], leaf_size)
        #right tree
        right_tree = build_tree(data_x[data_x[:, best_feature] > split_val],data_y[data_x[:, best_feature] > split_val], leaf_size)
        #root
        root = np.asarray([[best_feature, split_val, 1, left_tree.shape[0] + 1]])
        #return final array
        return np.vstack((np.vstack((root, left_tree)), right_tree))

class RTLearner(object):
    def __init__(self, leaf_size, verbose=False, tree=None):
        #constructor
        self.tree = tree
        self.leaf_size = leaf_size
        self.verbose = verbose
        pass
    def author(self):
        #gatech username
        return "ssubedi33"
    def study_group(self):
        #No study group
        return "ssubedi33"
    def add_evidence(self, data_x, data_y):
        #build tree
        self.tree = build_tree(data_x, data_y, self.leaf_size)
    def query(self, points):
        # array to put predicted values
        output = np.zeros(points.shape[0])
        # loop for each test cases
        for i in range(points.shape[0]):
            j = 0
            #loop until end of tree is reached
            while j < self.tree.shape[0]:
                #if end of tree
                if self.tree[j][0] == "leaf":
                    output[i] = self.tree[j][1]
                    break
                # if not end of tree
                else:
                    #search left side
                    if points[i, int(self.tree[j][0])] <= self.tree[j][1]:
                        next_idx = self.tree[j][2]
                    #search right side
                    else:
                        next_idx = self.tree[j][3]
                j += int(next_idx)
        return output