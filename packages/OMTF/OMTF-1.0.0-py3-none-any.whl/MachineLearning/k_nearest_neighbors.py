
import math
import pickle
import numpy as np
import pandas as pd

import utils

class KNN:
    
    # From: https://www.kaggle.com/code/fareselmenshawii/knn-from-scratch
    
    """
    K-Nearest Neighbors (KNN) classification algorithm

    Parameters:
    -----------
    n_neighbors : int, optional (default=5)
        Number of neighbors to use in the majority vote.

    Methods:
    --------
    fit(X_train, y_train):
        Stores the values of X_train and y_train.

    predict(X):
        Predicts the class labels for each example in X.

    """
    
    def __init__(self, n_neighbors:int=5) -> None:
        
        self.n_neighbors = n_neighbors

    def fit(self, X_train:np.ndarray, y_train:np.ndarray) -> None:
        
        """
        Stores the values of X_train and y_train.

        Parameters:
        -----------
        X_train : numpy.ndarray, shape (n_samples, n_features)
            The training dataset.

        y_train : numpy.ndarray, shape (n_samples,)
            The target labels.
        """
        
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X:np.ndarray) -> np.ndarray:
        
        """
        Predicts the class labels for each example in X.

        Parameters:
        -----------
        X : numpy.ndarray, shape (n_samples, n_features)
            The test dataset.

        Returns:
        --------
        predictions : numpy.ndarray, shape (n_samples,)
            The predicted class labels for each example in X.
        """
        
        # Create empty array to store the predictions
        predictions = []
        # Loop over X examples
        for x in X:
            # Get prediction using the prediction helper function
            prediction = self._predict(x)
            # Append the prediction to the predictions list
            predictions.append(prediction)
            
        return np.array(predictions)

    def _predict(self, x:np.ndarray) -> int:
        
        """
        Predicts the class label for a single example.

        Parameters:
        -----------
        x : numpy.ndarray, shape (n_features,)
            A data point in the test dataset.

        Returns:
        --------
        most_occuring_value : int
            The predicted class label for x.
        """
        
        # Create empty array to store distances
        distances = []
        # Loop over all training examples and compute the distance between x and all the training examples 
        for x_train in self.X_train:
            distance = utils.euclidean_distance(x, x_train)
            distances.append(distance)
        distances = np.array(distances)
        
        # Sort by ascendingly distance and return indices of the given n neighbours
        n_neighbors_idxs = np.argsort(distances)[: self.n_neighbors]
        
        # Get labels of n-neighbour indexes
        labels = self.y_train[n_neighbors_idxs]                  
        labels = list(labels)
        # Get the most frequent class in the array
        most_occuring_value = max(labels, key=labels.count)
        
        return most_occuring_value    
            
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
                marker=dict(color="#444"),
                line=dict(width=1),
                showlegend=True
            )
        ])
        fig.update_layout(
            xaxis_title='X',
            yaxis_title='Y',
            title='Prediction vs. target',
            hovermode="x"
        )
        fig.show()
    
    def getMetrics(self, y_real:np.ndarray, y_pred:np.ndarray, show:bool=True) -> dict:
        
        accuracy = utils.ClassificationMetrics.accuracy(y_real, y_pred)
        
        if show:
            print(f"Accuracy: {accuracy:.2%}")
            
        return {'accuracy':accuracy}
    
    
    
    
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
    
    model = KNN(7)
    model.fit(X_train, y_train)
    
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