
import math
import pickle
import numpy as np
import pandas as pd

import utils

class NaiveBayes:
    
    '''
    Naive Bayes classifier implementation using Gaussian distribution assumption.
    
    Tries to maximize the probability of something happening assuming something has 
    already happened. It assumes that all features are independent and the underlying 
    distribution is Gaussian.
    '''

    def fit(self, X:np.ndarray, y:np.ndarray) -> None:
        
        '''
        Fit the Naive Bayes classifier to the training data.

        Parameters
        ----------
        X: np.ndarray 
            Training feature data of shape (n_samples, n_features).
        y: np.ndarray
            Target labels of shape (n_samples,).
        '''
        
        # Get the number of samples, number of features respectively
        X = X if round(np.mean(X)) == 0 and round(np.std(X)) == 1 else utils.scale(X)
        self.m, self.n = X.shape
        
        # Get the unique elements in y (class labels)
        self.unique_classes = np.unique(y)
        # Get the number of unique classes
        self.n_unique = len(self.unique_classes)
        
        # Create empty arrays to store mean, variance, and priors
        self.mean = np.zeros((self.n_unique, self.n))
        self.variance = np.zeros((self.n_unique, self.n))
        self.priors = np.zeros(self.n_unique)
        
        for i, c in enumerate(self.unique_classes):
            # Get the portion of the data where y is equal to a certain class
            X_c = X[y == c]
            # Calculate the mean for each class and all features
            self.mean[i, :] = np.mean(X_c, axis=0)
            # Calculate the variance for each class and all features
            self.variance[i, :] = np.var(X_c, axis=0)
            # Calculate the priors
            self.priors[i] = X_c.shape[0] / self.m

    def gaussian_density(self, x:np.ndarray, c:int) -> np.ndarray:
        
        '''
        Calculate the Gaussian density function for a given feature vector and class.

        Parameters
        ----------
        x: np.ndarray
            Feature vector of shape (n_features,).
        c: int
            Index of the class.

        Returns
        -------
        return: np.ndarray
            Gaussian density values for each feature.
        '''
        
        # Get the mean and the variance for the specified class
        mean = self.mean[c]
        variance = self.variance[c]
        
        # Calculate the Gaussian density function
        const = 1 / np.sqrt(variance * 2 * np.pi)
        proba = np.exp(-0.5 * ((x - mean) ** 2 / variance))
        
        return const * proba

    def get_probability(self, x:np.ndarray) -> int:
        
        '''
        Calculate the probability of each class given a feature vector.

        Parameters
        ----------
        x: np.ndarray
            Feature vector of shape (n_features,).

        Returns
        -------
        return: int
            Predicted class label.
        '''
        
        # Create an empty list to store the posteriors
        posteriors = []
        
        for i, c in enumerate(self.unique_classes):
            # Calculate the log of the prior
            prior = np.log(self.priors[i])
            # Calculate the new posterior and append it to the list
            posterior = np.sum(np.log(self.gaussian_density(x, i)))
            posterior = posterior + prior
            posteriors.append(posterior)
            
        # Return the class with the highest class probability
        return self.unique_classes[np.argmax(posteriors)]

    def predict(self, X:np.ndarray) -> np.ndarray:
        
        '''
        Predict the class labels for the input feature data.

        Parameters
        ----------
        X: np.ndarray
            Feature data of shape (n_samples, n_features).

        Returns
        -------
        return: np.ndarray
            Predicted class labels of shape (n_samples,).
        '''
        
        # Create an empty array to store the predictions
        predictions = []
        
        # Loop over each sample in X
        X = X if round(np.mean(X)) == 0 and round(np.std(X)) == 1 else utils.scale(X)
        for x in X:
            # Get the prediction for this sample
            pred = self.get_probability(x)
            # Append the prediction to the predictions list
            predictions.append(pred)
        
        return np.array(predictions)
    
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
            Dictionary containing 'accuracy' for the model.
        '''
        
        accuracy = utils.ClassificationMetrics.accuracy(y_real, y_pred)
        
        if show:
            print(f"Accuracy: {accuracy:.2%}")
            
        return {'accuracy':accuracy}
        
    
if __name__ == '__main__':
    
    import yfinance as yf
    from principal_component import PCA
    
    pca_apply = False
    just_side = False

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
    
    features = ['range_pu', 'open_to_close_pu', 'gap_pu', 'outlier_pu', 'day', 'month', 'week_day', 'is_quarter_end']

    X_train, X_test, y_train_raw, y_test_raw = utils.train_test_split(data[features], data['target'], 
                                                              random_state=41, test_size=0.2)
    X_train_stand, X_test_stand = utils.standardize_data(X_train, X_test)
    
    if pca_apply:
        pca = PCA(len(features)/2)
        pca.fit(X_train_stand)
        X_train_stand = pca.transform(X_train_stand)
        X_test_stand = pca.transform(X_test_stand)
        pca.plotComponents(X_train_stand)
        pca.cumulative_variance_ratio
        
        features = [f'PC{i}' for i in range(X_train_stand.shape[-1])]

    model = NaiveBayes()
    model.fit(X_train_stand, y_train_raw)
    
    y_train_pred = model.predict(X_train_stand)
    y_test_pred = model.predict(X_test_stand)
    
    # Show metrics
    tests = {'train': [y_train_raw, y_train_pred], 'test':[y_test_raw, y_test_pred]}
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