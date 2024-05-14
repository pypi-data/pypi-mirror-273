
import math
import pickle
import numpy as np
import pandas as pd

import utils


class Node():
    
    #From: https://www.kaggle.com/code/fareselmenshawii/decision-tree-from-scratch?scriptVersionId=130941860
    
    '''
    A class representing a node in a decision tree.
    '''

    def __init__(self, feature:int=None, threshold=None, left=None, right=None, 
                 gain=None, value=None) -> None:
        
        '''
        Initializes a new instance of the Node class.

        Parameters
        ----------
        feature: int
            The feature used for splitting at this node. Defaults to None.
        threshold: 
            The threshold used for splitting at this node. Defaults to None.
        left: 
            The left child node. Defaults to None.
        right: 
            The right child node. Defaults to None.
        gain: 
            The gain of the split. Defaults to None.
        value: 
            If this node is a leaf node, this attribute represents the predicted value
            for the target variable. Defaults to None.
        '''
        
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.gain = gain
        self.value = value
        
        
        
class DecisionTreeClassifier():
    
    #From: https://www.kaggle.com/code/fareselmenshawii/decision-tree-from-scratch?scriptVersionId=130941860
    
    '''
    A decision tree classifier for binary classification problems.
    '''

    def __init__(self, min_samples:int=2, max_depth:int=2) -> None:
        
        '''
        Constructor for DecisionTree class.

        Parameters
        ----------
        min_samples: int
            Minimum number of samples required to split an internal node.
        max_depth: int
            Maximum depth of the decision tree.
        '''
        
        self.min_samples = min_samples
        self.max_depth = max_depth

    def split_data(self, dataset:np.ndarray, feature:int, threshold:float) -> (np.ndarray, np.ndarray):
        
        '''
        Splits the given dataset into two datasets based on the given feature and threshold.

        Parameters
        ----------
        dataset: np.ndarray
            Input dataset.
        feature: int 
            Index of the feature to be split on.
        threshold: float 
            Threshold value to split the feature on.

        Returns
        -------
        left_dataset: np.ndarray
            Subset of the dataset with values less than or equal to the threshold.
        right_dataset: np.ndarray
            Subset of the dataset with values greater than the threshold.
        '''
        
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
        
        '''
        Computes the entropy of the given label values.

        Parameters
        ----------
        y: np.ndarray
            Input label values.

        Returns
        -------
        entropy: float
            Entropy of the given label values.
        '''
        
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

        # Return the final entropy value
        return entropy

    def information_gain(self, parent:np.ndarray, left:np.ndarray, right:np.ndarray) -> float:
        
        '''
        Computes the information gain from splitting the parent dataset into two datasets.

        Parameters
        ----------
        parent: np.ndarray
            Input parent dataset.
        left: np.ndarray
            Subset of the parent dataset after split on a feature.
        right: np.ndarray
            Subset of the parent dataset after split on a feature.

        Returns
        -------
        information_gain: float
            Information gain of the split.
        '''
        
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

    def best_split(self, dataset:np.ndarray, num_samples:int, num_features:int) -> dict:
        
        '''
        Finds the best split for the given dataset.

        Parameters
        ----------
        dataset: np.ndarray
            The dataset to split.
        num_samples: int
            The number of samples in the dataset.
        num_features: int
            The number of features in the dataset.

        Returns
        -------
        best_split: dict 
            A dictionary with the best split feature index, threshold, gain, 
            left and right datasets.
        '''
        
        # dictionary to store the best split values
        best_split = {'gain':- 1, 'feature': None, 'threshold': None}#, 'left_dataset':None, 'right_dataset':None}
        # loop over all the features
        for feature_index in range(num_features):
            # get the feature at the current feature_index
            feature_values = dataset[:, feature_index]
            # get unique values of that feature
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
                    if information_gain > best_split['gain']:
                        best_split['feature'] = feature_index
                        best_split['threshold'] = threshold
                        best_split['left_dataset'] = left_dataset
                        best_split['right_dataset'] = right_dataset
                        best_split['gain'] = information_gain
                        
        return best_split

    def calculate_leaf_value(self, y:list) -> float:
        
        '''
        Calculates the most frequent value in the given list of y values.

        Parameters
        ----------
        y: list
            The list of y values.

        Returns
        -------
        most_ocurring_value: float
            The most frequent value in the list.
        '''
        
        y = list(y)
        #get the highest present class in the array
        most_occuring_value = max(y, key=y.count)
        
        return most_occuring_value
    
    def build_tree(self, dataset:np.ndarray, current_depth:int=0) -> Node:
        
        '''
        Recursively builds a decision tree from the given dataset.

        Parameters
        ----------
        dataset: np.ndarray
            The dataset to build the tree from.
        current_depth: int
            The current depth of the tree.

        Returns
        -------
        return: Node
            The root node of the built decision tree.
        '''
        
        # split the dataset into X, y values
        X, y = dataset[:, :-1], dataset[:, -1]
        n_samples, n_features = X.shape
        # keeps spliting until stopping conditions are met
        if n_samples >= self.min_samples and current_depth <= self.max_depth:
            # Get the best split
            best_split = self.best_split(dataset, n_samples, n_features)
            # Check if gain greater than zero
            if best_split['gain'] > 0:
                # continue splitting the left and the right child. Increment current depth
                left_node = self.build_tree(best_split['left_dataset'], current_depth + 1)
                right_node = self.build_tree(best_split['right_dataset'], current_depth + 1)
                # return decision node
                return Node(best_split['feature'], best_split['threshold'],
                            left_node, right_node, best_split['gain'])

        # compute leaf node value
        leaf_value = self.calculate_leaf_value(y)
        
        # return leaf node value
        return Node(value=leaf_value)
    
    def fit(self, X:np.ndarray, y:np.ndarray) -> None:
        
        '''
        Builds and fits the decision tree to the given X and y values.

        Parameters
        ----------
        X: np.ndarray 
            The feature matrix.
        y: np.ndarray
            The target values.
        '''
        
        # Make the two arrays have same dimensions
        X = X if round(np.mean(X)) == 0 and round(np.std(X)) == 1 else utils.scale(X)
        if len(X.shape) == 2 and len(y.shape) == 1:
            y = y.reshape(-1,1)
            
        dataset = np.concatenate((X, y), axis=1)  
        self.root = self.build_tree(dataset)

    def predict(self, X:np.ndarray) -> list:
        
        '''
        Predicts the class labels for each instance in the feature matrix X.

        Parameters
        ----------
        X: np.ndarray
            The feature matrix to make predictions for.

        Returns
        -------
        predictions: list
            A list of predicted class labels.
        '''
        
        # Create an empty list to store the predictions
        predictions = []
        # For each instance in X, make a prediction by traversing the tree
        X = X if round(np.mean(X)) == 0 and round(np.std(X)) == 1 else utils.scale(X)
        for x in X:
            prediction = self.make_prediction(x, self.root)
            # Append the prediction to the list of predictions
            predictions.append(prediction)
        
        return predictions
    
    def make_prediction(self, x:np.ndarray, node:Node):
        
        '''
        Traverses the decision tree to predict the target value for the given feature vector.

        Parameters
        ----------
        x: np.ndarray
            The feature vector to predict the target value for.
        node: Node
            The current node being evaluated.

        Returns
        -------
        The predicted target value for the given feature vector.
        '''
        
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
            
    def plotPrediction(self, X:np.ndarray=None, y:np.ndarray=None) -> None:
        
        '''
        Plotly chart containing the real data and the prediction.

        Parameters
        ----------
        X: np.ndarray
            Input data of shape (m, n_features).
        y: np.ndarray
            Data to predict of shape (m, ).

        Plots
        -----
        Plotly chart containing the real data and the prediction.
        '''

        X = self.X if not isinstance(X, np.ndarray) else X
        y = self.y if not isinstance(y, np.ndarray) else y
        
        import plotly.graph_objs as go
        fig = go.Figure([
            go.Scatter(
                name='Data',
                y=y,
                mode='markers',
                marker=dict(color='red', size=2),
                showlegend=True
            ),
            go.Scatter(
                name='Prediction',
                y=self.predict(X),
                mode='lines',
                marker=dict(color='#444'),
                line=dict(width=1),
                showlegend=True
            )
        ])
        fig.update_layout(
            xaxis_title='X',
            yaxis_title='Y',
            title='Prediction vs. target',
            hovermode='x'
        )
        fig.show()
            
    def getMetrics(self, y_real:np.ndarray, y_pred:np.ndarray, show:bool=True) -> dict:

        '''
        Get model metrics.

        Parameters
        ----------
        y_real: np.ndarray
            Array containig the real data to be predicted.
        y_pred: np.ndarray
            Array containig the predicted data.
        show: bool
            True to print the metrics.

        Returns
        -------
        return: dict
            Dictionary containing 'accuracy' and 'balance_accuracy' for the model.
        '''
        
        accuracy = utils.ClassificationMetrics.accuracy(y_real, y_pred)
        balanced_accuracy = utils.ClassificationMetrics.balanced_accuracy(y_real, y_pred)
        
        if show:
            print(f"Accuracy: {accuracy:.2%}")
            print(f"Balanced Accuracy: {balanced_accuracy:.2%}")
            
        return {'accuracy':accuracy, 'balance_accuracy':balanced_accuracy}
    
        
        

if __name__ == '__main__':

    import yfinance as yf

    data = yf.Ticker('TSLA').history(period='5y', interval='1d')
    data.columns = [c.lower() for c in data.columns]
    data['date'] = data.index
    data['prev_close'] = data['close'].shift(1)
    data['outlier_pu'] = data['open']/data['open'].rolling(50).mean() - 1
    data['range'] = (data['high'] - data['low']).shift(1)
    data['range_pu'] = data['range']/data['open']
    data['open_to_close'] = (data['close'] - data['open']).shift(1)
    data['open_to_close_pu'] = data['range']/data['open']
    data['gap'] = data['open'] - data['close'].shift(1)
    data['gap_pu'] = data['gap'] / data['close'].shift(1)
    
    data['day'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.day
    data['week_day'] = data['date'].dt.dayofweek
    data['is_quarter_end'] = np.where(data['month']%3 == 0, 1, 0)
        
    data['target'] = np.where(data['open'] < data['close'], 1, 0)
    data.dropna(inplace=True)
    
    features = ['range_pu', 'open_to_close_pu', 'gap_pu', 'outlier_pu']

    X_train, X_test, y_train, y_test = utils.train_test_split(data[features], data['target'], 
                                                              random_state=41, test_size=0.2)
    X_train_stand, X_test_stand = utils.standardize_data(X_train, X_test)

    model = DecisionTreeClassifier(min_samples=2, max_depth=10) # max_depth is the iterations
    model.fit(X_train_stand, y_train)
    
    y_train_pred = model.predict(X_train_stand)
    y_test_pred = model.predict(X_test_stand)
    
    # Show metrics
    tests = {'train': [y_train, y_train_pred], 'test':[y_test, y_test_pred]}
    for k in tests:
        y_test, y_pred = tests[k]
        
        print(f'\nMETRICS FOR THE {k.upper()} ----------------')
        model.getMetrics(y_test, y_pred, show=True)
        
        y_df = pd.DataFrame({'Open':data['open'].iloc[-len(y_test):], 
                            'Close':data['close'].iloc[-len(y_test):],
                            'Orig': y_test, 'Pred': y_pred})
        y_df['Range'] = y_df['Close'] - y_df['Open']
        success = y_df[y_df['Pred'] == y_df['Orig']]
        error = y_df[y_df['Pred'] != y_df['Orig']]
        
        wr = len(success)/len(y_df)
        rr = (success['Range'].abs().mean())/(error['Range'].abs().mean())
        print(f'Side Success: {wr:.2%}')
        print(f'Risk Reward: {rr:.2} R')
        print(f"Spectancy: {(wr * success['Range'].abs().mean() - (1-wr) * error['Range'].abs().mean()):.2%}")

    # Plot prediction
    model.plotPrediction(X=X_test_stand, y=y_test)