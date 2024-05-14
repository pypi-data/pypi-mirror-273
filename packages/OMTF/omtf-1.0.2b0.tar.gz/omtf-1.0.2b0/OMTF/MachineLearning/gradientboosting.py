
import numpy as np
import pandas as pd

class Node:
    
    def __init__(self, feature:int=None, threshold:float=None, left=None, right=None, 
                 gain:float=None, value:float=None) -> None:

        """
        Initializes a new instance of the Node class.

        Args:
            feature: The feature used for splitting at this node. Defaults to None.
            threshold: The threshold used for splitting at this node. Defaults to None.
            left: The left child node. Defaults to None.
            right: The right child node. Defaults to None.
            gain: The gain of the split. Defaults to None.
            value: If this node is a leaf node, this attribute represents the predicted value
                for the target variable. Defaults to None.
        """

        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.gain = gain
        self.value = value
    
    def is_leaf_node(self) -> bool:
        return self.value is not None
    

class Tree:

    def __init__(self, min_samples:int=2, min_impurity:float=1.0, max_depth:int=2, 
                 n_feats:int=None) -> None:

        """
        Constructor for RegressionTree class.

        Parameters:
            min_samples (int): Minimum number of samples required to split an internal node.
            max_depth (int): Maximum depth of the decision tree.
        """

        self.min_samples = min_samples
        self.min_impurity = min_impurity
        self.max_depth = max_depth
        self.n_feats = n_feats
    


# Decision Tree Regressor Class
class RegressionTree:

    def __init__(self, min_samples:int=2, min_impurity:float=1.0, max_depth:int=2, 
                 n_feats:int=None) -> None:

        """
        Constructor for RegressionTree class.

        Parameters:
            min_samples (int): Minimum number of samples required to split an internal node.
            max_depth (int): Maximum depth of the decision tree.
        """

        self.min_samples = min_samples
        self.min_impurity = min_impurity
        self.max_depth = max_depth
        self.n_feats = n_feats
    
    def fit(self, X:np.ndarray, Y:np.ndarray) -> None:

        self.n_feats = X.shape[1] if self.n_feats == None else min(self.n_feats, X.shape[1])
        self.col = range(X.shape[1])
        self.root = self.growTree(X, Y)

    def growTree(self, X:np.ndarray, Y:np.ndarray, depth:int= 0) -> Node:
        
        df = pd.DataFrame(X)
        df['y'] = Y
        
        ymean = np.mean(Y)
        
        self.mse = self.get_mse(Y, ymean)
        
        n_samples, n_features = X.shape
        
        # stopping criteria
        if (depth >= self.max_depth or n_samples <= self.min_samples):
            leaf_value = np.mean(Y)
            return Node(value=leaf_value)

        best_feat, best_thresh = self.best_criteria(X, Y)

        left_df:pd.DataFrame = df[df[best_feat]<=best_thresh].copy()
        right_df:pd.DataFrame = df[df[best_feat]>best_thresh].copy()

        left = self.growTree(left_df.drop('y', axis=1), left_df['y'].values.tolist(), depth+1)
        right = self.growTree(right_df.drop('y', axis=1), right_df['y'].values.tolist(), depth+1)

        return Node(best_feat, best_thresh, left, right)
    
    # find out best criteria
    def best_criteria(self, X:np.ndarray, Y:np.ndarray) -> (int, float):
        
        df = pd.DataFrame(X)
        
        df['y'] = Y
        
        mse_base = self.mse
        
        best_feature = None
        best_thresh = None
        
        for feat in self.col:
            print(feat, '\n', df)
            xdf = df.sort_values(feat)
            
            x_mean = self.moving_average(xdf[feat], 2)

            for value in x_mean:
                left_y = xdf[xdf[feat] < value]['y'].values
                right_y = xdf[xdf[feat] >= value]['y'].values
                
                left_mean = 0
                right_mean = 0
                if len(left_y) > 0:
                    left_mean = np.mean(left_y)
                if len(right_y) > 0:
                    right_mean = np.mean(right_y)
                
                res_left = left_y - left_mean
                res_right = right_y - right_mean
                
                r = np.concatenate((res_left, res_right), axis=None)
                
                n = len(r)

                r = r ** 2
                r = np.sum(r)
                mse_split = r / n
                
                if mse_split < mse_base:
                    mse_base = mse_split
                    best_feature = feat
                    best_thresh = value
                    
        return (best_feature, best_thresh)
    
    def get_mse(self, y_true, y_hat):
        n = len(y_true)
        
        r = y_true - y_hat
        
        r = r ** 2
        
        r = np.sum(r)
        
        return r / n
    
    def moving_average(self, x:np.array, window : int):
        return np.convolve(x, np.ones(window), 'valid') / window 
    
    def predict(self, X):
        X = X.to_numpy().tolist()
        
        return np.array([self.traverse_tree(x, self.root) for x in X])

    def traverse_tree(self, x, node):
       
        if node.value is not None:
            return node.value
        
        fr = node.feature
        index = self.col.index(fr)

        if x[index] <= node.threshold:
            return self.traverse_tree(x, node.left)
        
        return self.traverse_tree(x, node.right)
    


class DecisionTree:

    """
    A decision tree classifier for binary classification problems.
    """

    def __init__(self, min_samples:int=2, min_impurity:float=1.0, max_depth:int=2, 
                 n_feats:int=None) -> None:

        """
        Constructor for RegressionTree class.

        Parameters:
            min_samples (int): Minimum number of samples required to split an internal node.
            max_depth (int): Maximum depth of the decision tree.
        """

        self.min_samples = min_samples
        self.min_impurity = min_impurity
        self.max_depth = max_depth
        self.n_feats = n_feats

    def split_data(self, dataset:np.ndarray, feature:int, threshold:float) -> (np.ndarray, np.ndarray):

        """
        Splits the given dataset into two datasets based on the given feature and threshold.

        Parameters:
            dataset (ndarray): Input dataset.
            feature (int): Index of the feature to be split on.
            threshold (float): Threshold value to split the feature on.

        Returns:
            left_dataset (ndarray): Subset of the dataset with values less than or equal to the threshold.
            right_dataset (ndarray): Subset of the dataset with values greater than the threshold.
        """

        # Create empty arrays to store the left and right datasets
        left_dataset = []
        right_dataset = []
        
        # Loop over each row in the dataset and split based on the given feature and threshold
        for row in dataset:
            if row[feature] <= threshold:
                left_dataset.append(row)
            else:
                right_dataset.append(row)

        # Convert the left and right datasets to numpy arrays and return
        left_dataset = np.array(left_dataset)
        right_dataset = np.array(right_dataset)

        return left_dataset, right_dataset

    def entropy(self, y:np.ndarray) -> float:

        """
        Computes the entropy of the given label values.

        Parameters:
            y (ndarray): Input label values.

        Returns:
            entropy (float): Entropy of the given label values.
        """

        entropy = 0

        # Find the unique label values in y and loop over each value
        labels = np.unique(y)
        for label in labels:
            # Find the examples in y that have the current label
            label_examples = y[y == label]
            # Calculate the ratio of the current label in y
            pl = len(label_examples) / len(y)
            # Calculate the entropy using the current label and ratio
            entropy += -pl * np.log2(pl)

        return entropy

    def information_gain(self, parent:np.ndarray, left:np.ndarray, right:np.ndarray) -> float:

        """
        Computes the information gain from splitting the parent dataset into two datasets.

        Parameters:
            parent (ndarray): Input parent dataset.
            left (ndarray): Subset of the parent dataset after split on a feature.
            right (ndarray): Subset of the parent dataset after split on a feature.

        Returns:
            information_gain (float): Information gain of the split.
        """

        # set initial information gain to 0
        information_gain = 0
        # compute entropy for parent
        parent_entropy = self.entropy(parent)
        # calculate weight for left and right nodes
        weight_left = len(left) / len(parent)
        weight_right= len(right) / len(parent)
        # compute entropy for left and right nodes
        entropy_left, entropy_right = self.entropy(left), self.entropy(right)
        # calculate weighted entropy 
        weighted_entropy = weight_left * entropy_left + weight_right * entropy_right
        # calculate information gain 
        information_gain = parent_entropy - weighted_entropy

        return information_gain

    def best_split(self, dataset:np.ndarray, num_samples:int, num_features:int):

        """
        Finds the best split for the given dataset.

        Args:
        dataset (ndarray): The dataset to split.
        num_samples (int): The number of samples in the dataset.
        num_features (int): The number of features in the dataset.

        Returns:
        dict: A dictionary with the best split feature index, threshold, gain, 
              left and right datasets.
        """

        # dictionary to store the best split values
        best_split = {'gain':- 1, 'feature': None, 'threshold': None}
        # loop over all the features
        for feature_index in range(num_features):
            #get the feature at the current feature_index
            feature_values = dataset[:, feature_index]
            #get unique values of that feature
            thresholds = np.unique(feature_values)
            # loop over all values of the feature
            for threshold in thresholds:
                # get left and right datasets
                left_dataset, right_dataset = self.split_data(dataset, feature_index, threshold)
                # check if either datasets is empty
                if len(left_dataset) and len(right_dataset):
                    # get y values of the parent and left, right nodes
                    y, left_y, right_y = dataset[:, -1], left_dataset[:, -1], right_dataset[:, -1]
                    # compute information gain based on the y values
                    information_gain = self.information_gain(y, left_y, right_y)
                    # update the best split if conditions are met
                    if information_gain > best_split["gain"]:
                        best_split["feature"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["left_dataset"] = left_dataset
                        best_split["right_dataset"] = right_dataset
                        best_split["gain"] = information_gain

        return best_split

    def calculate_leaf_value(self, y:list) -> float:

        """
        Calculates the most occurring value in the given list of y values.

        Args:
            y (list): The list of y values.

        Returns:
            The most occurring value in the list.
        """
        
        y = list(y)
        # get the highest present class in the array
        most_occuring_value = max(y, key=y.count)

        return most_occuring_value
    
    def build_tree(self, dataset:np.ndarray, current_depth:int=0) -> Node:

        """
        Recursively builds a decision tree from the given dataset.

        Args:
        dataset (ndarray): The dataset to build the tree from.
        current_depth (int): The current depth of the tree.

        Returns:
        Node: The root node of the built decision tree.
        """

        # split the dataset into X, y values
        X, y = dataset[:, :-1], dataset[:, -1]
        n_samples, n_features = X.shape
        # keeps spliting until stopping conditions are met
        if n_samples >= self.min_samples and current_depth <= self.max_depth:
            # Get the best split
            best_split = self.best_split(dataset, n_samples, n_features)
            # Check if gain isn't zero
            if best_split["gain"]:
                # continue splitting the left and the right child. Increment current depth
                left_node = self.build_tree(best_split["left_dataset"], current_depth + 1)
                right_node = self.build_tree(best_split["right_dataset"], current_depth + 1)
                # return decision node
                return Node(best_split["feature"], best_split["threshold"],
                            left_node, right_node, best_split["gain"])

        # compute leaf node value
        leaf_value = self.calculate_leaf_value(y)

        # return leaf node value
        return Node(value=leaf_value)
    
    def fit(self, X:np.ndarray, y:np.ndarray) -> None:

        """
        Builds and fits the decision tree to the given X and y values.

        Args:
        X (ndarray): The feature matrix.
        y (ndarray): The target values.
        """

        dataset = np.concatenate((X, y), axis=1)  
        self.root = self.build_tree(dataset)

    def predict(self, X:np.ndarray, array_format:bool=True) -> (list or np.ndarray):

        """
        Predicts the class labels for each instance in the feature matrix X.

        Args:
        X (ndarray): The feature matrix to make predictions for.

        Returns:
        list: A list of predicted class labels.
        """

        # Create an empty list to store the predictions
        predictions = []
        # For each instance in X, make a prediction by traversing the tree
        for x in X:
            prediction = self.make_prediction(x, self.root)
            # Append the prediction to the list of predictions
            predictions.append(prediction)

        return np.array(predictions) if array_format else predictions
    
    def make_prediction(self, x:np.ndarray, node:Node) -> float:

        """
        Traverses the decision tree to predict the target value for the given feature vector.

        Args:
        x (ndarray): The feature vector to predict the target value for.
        node (Node): The current node being evaluated.

        Returns:
        The predicted target value for the given feature vector.
        """

        # if the node has value i.e it's a leaf node extract it's value
        if node.value != None: 
            return node.value
        else:
            #if it's node a leaf node we'll get it's feature and traverse through the tree accordingly
            feature = x[node.feature]
            if feature <= node.threshold:
                return self.make_prediction(x, node.left)
            else:
                return self.make_prediction(x, node.right)
            
    
if __name__ == '__main__':

    from .utils import train_test_split
    
    x = data.drop('Life expectancy ', axis=1)
    y = data['Life expectancy ']
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    DRT = RegressionTree(max_depth = 15,min_samples = 20)

    DRT.fit(X_train, y_train)
    
    y_pred = DRT.predict(X_test)