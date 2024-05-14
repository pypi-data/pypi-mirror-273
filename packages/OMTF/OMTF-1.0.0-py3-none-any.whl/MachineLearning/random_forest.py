
import math
import pickle
import numpy as np
import pandas as pd

import utils
import decision_trees

class RandomForest:
    
    # From: https://www.kaggle.com/code/fareselmenshawii/random-forest-from-scratch?scriptVersionId=138025147
    
    '''
    A random forest classifier.

    Parameters
    ----------
    n_trees: int
        The number of trees in the random forest.
    max_depth: int
        The maximum depth of each decision tree in the random forest.
    min_samples: int
        The minimum number of samples required to split an internal node
        of each decision tree in the random forest.

    Attributes
    ----------
    n_trees : int
        The number of trees in the random forest.
    max_depth : int
        The maximum depth of each decision tree in the random forest.
    min_samples : int
        The minimum number of samples required to split an internal node
        of each decision tree in the random forest.
    trees : list of DecisionTreeClassifier
        The decision trees in the random forest.
    '''

    def __init__(self, n_trees:int=7, max_depth:int=7, min_samples:int=2) -> None:
        
        '''
        Initialize the random forest classifier.

        Parameters
        ----------
        n_trees: int
            The number of trees in the random forest.
        max_depth: int
            The maximum depth of each decision tree in the random forest.
        min_samples: int
            The minimum number of samples required to split an internal node
            of each decision tree in the random forest.
        '''
        
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.trees = []

    def fit(self, X:np.ndarray, y:np.ndarray):
        
        '''
        Build a random forest classifier from the training set (X, y).

        Parameters
        ----------
        X: np.ndarray
            The training input samples with shape (n_samples, n_features).
        y: np.ndarray
            The target values with shape (n_samples,).
        '''
        
        # Create an empty list to store the trees.
        self.trees = []
        # Concatenate X and y into a single dataset.
        dataset = np.concatenate((X, y.reshape(-1, 1)), axis=1)
        # Loop over the number of trees.
        for _ in range(self.n_trees):
            # Create a decision tree instance.
            tree = decision_trees.DecisionTreeClassifier(min_samples=self.min_samples, max_depth=self.max_depth)
            # Sample from the dataset with replacement (bootstrapping).
            dataset_sample = self.bootstrap_samples(dataset)
            # Get the X and y samples from the dataset sample.
            X_sample, y_sample = dataset_sample[:, :-1], dataset_sample[:, -1]
            # Fit the tree to the X and y samples.
            tree.fit(X_sample, y_sample)
            # Store the tree in the list of trees.
            self.trees.append(tree)

    def bootstrap_samples(self, dataset:np.ndarray) -> np.ndarray:
        
        '''
        Bootstrap the dataset by sampling from it with replacement.

        Parameters
        ----------
        dataset: np.ndarray
            The dataset to bootstrap with shape (n_samples, n_features + 1).

        Returns
        -------
        dataset_sample : np.ndarray
            The bootstrapped dataset sample with shape (n_samples, n_features + 1).
        '''
        
        # Get the number of samples in the dataset.
        n_samples = dataset.shape[0]
        # Generate random indices to index into the dataset with replacement.
        np.random.seed(1)
        indices = np.random.choice(n_samples, n_samples, replace=True)
        # Return the bootstrapped dataset sample using the generated indices.
        dataset_sample = dataset[indices]
        
        return dataset_sample

    def most_common_label(self, y:list) -> (int or float):
        
        '''
        Return the most common label in an array of labels.

        Parameters
        ----------
        y: np.ndarray
            The array of labels with shape (n_samples,).

        Returns
        -------
        most_occuring_value : int or float
            The most common label in the array.
        '''
        
        y = list(y)
        # get the highest present class in the array
        most_occuring_value = max(y, key=y.count)
        
        return most_occuring_value

    def predict(self, X:np.ndarray) -> np.ndarray:
        
        '''
        Predict class for X.

        Parameters
        ----------
        X: np.ndarray
            The input samples with shape (n_samples, n_features).

        Returns
        -------
        majority_predictions: np.ndarray
            The predicted classes with shape (n_samples,).
        '''
        
        #get prediction from each tree in the tree list on the test data
        predictions = np.array([tree.predict(X) for tree in self.trees])
        # get prediction for the same sample from all trees for each sample in the test data
        preds = np.swapaxes(predictions, 0, 1)
        #get the most voted value by the trees and store it in the final predictions array
        majority_predictions = np.array([self.most_common_label(pred) for pred in preds])
        
        return majority_predictions
    
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
            Dictionary containing 'accuracy', 'precision', 'recall' and 
            'f1_score' for the model.
        '''
        
        accuracy = utils.ClassificationMetrics.accuracy(y_real, y_pred)
        precision = utils.ClassificationMetrics.precision(y_real, y_pred)
        recall = utils.ClassificationMetrics.recall(y_real, y_pred)
        f1_score = utils.ClassificationMetrics.f1_score(y_real, y_pred)
        
        if show:
            print(f"Accuracy: {accuracy:.2%}")
            print(f"Precision: {precision:.2%}")
            print(f"Recall: {recall:.2%}")
            print(f"F1-Score: {f1_score:.2%}")
            
        return {'accuracy':accuracy, 'precision':precision, 
                'recall':recall, 'f1_score':f1_score}
        
    
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
    # X_train_stand, X_test_stand = utils.standardize_data(X_train, X_test)

    model = RandomForest(n_trees=10, max_depth=10, min_samples=2)
    model.fit(X_train, y_train)
    
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
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
    model.plotPrediction(X=X_test, y=y_test)
    
    
    