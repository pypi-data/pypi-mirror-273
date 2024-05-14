
import math
import pickle
import numpy as np
import pandas as pd

import utils

class PCA:
    
    # From: https://www.kaggle.com/code/fareselmenshawii/pca-from-scratch/notebook?scriptVersionId=121402593
    
    '''
    Principal Component Analysis (PCA) class for dimensionality reduction.
    
    This model takes n features and calculates a given number of components based
    on the features to try to represent the most information posible. This new components 
    would substitute the inputed features.
    '''
    
    def __init__(self, n_components:int, standardize:bool=True) -> None:
        
        '''
        Constructor method that initializes the PCA object with the number of components to retain.

        Parameters
        ----------
        n_components : int
            Number of principal components to obtain.
        standardize: bool
            True to standardize the data.
        '''
        
        self.n_components = math.ceil(n_components) if not isinstance(n_components, int) \
                            else n_components
        self.standardize = standardize

    def __checkStandarization(self, arr:np.ndarray) -> np.ndarray:
        
        '''
        Checks if an array is standardized.
        
        Parameters
        ----------
        arr : np.ndarray
            Input data.
        
        Returns
        -------
        arr: np.ndarray
            Standardized data if it wasn't standardized already, else the original data.
        '''

        return arr if round(np.mean(arr)) == 0 and round(np.std(arr)) == 1 else utils.scale(arr)
        
    def fit(self, X:np.ndarray) -> None:
        
        '''
        Fits the PCA model to the input data and computes the principal components.

        Parameters
        ----------
        X : np.ndarray
            Input data matrix with shape (n_samples, n_features).
        '''

        if self.standardize:
            X = self.__checkStandarization(X)
        
        # Compute the mean of the input data along each feature dimension.
        mean = np.mean(X, axis=0)
        
        # Subtract the mean from the input data to center it around zero.
        X = X - mean
        
        # Compute the covariance matrix of the centered input data.
        cov = np.cov(X.T)
        
        # Compute the eigenvectors and eigenvalues of the covariance matrix.
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        # Reverse the order of the eigenvalues and eigenvectors.
        eigenvalues = eigenvalues[::-1]
        eigenvectors = eigenvectors[:,::-1]
        
        # Keep only the first n_components eigenvectors as the principal components.
        self.components = eigenvectors[:,:self.n_components]
        
        # Compute the explained variance ratio for each principal component.
        # Compute the total variance of the input data
        total_variance = np.sum(np.var(X, axis=0))

        # Compute the variance explained by each principal component
        self.explained_variances = eigenvalues[:self.n_components]

        # Compute the explained variance ratio for each principal component
        self.explained_variance_ratio = self.explained_variances / total_variance
        
    def transform(self, X:np.ndarray) -> np.ndarray:
        
        '''
        Transforms the input data by projecting it onto the principal components.
        
        Parameters
        ----------
        X : np.ndarray
            Input data matrix with shape (n_samples, n_features).
        
        Returns
        -------
        transformed_data: np.ndarray
            Transformed data matrix with shape (n_samples, n_components).
        '''
        
        if self.standardize:
            X = self.__checkStandarization(X)

        # Center the input data around zero using the mean computed during the fit step.
        X = X - np.mean(X, axis=0)
        
        # Project the centered input data onto the principal components.
        transformed_data = np.dot(X, self.components)
        
        return transformed_data
    
    def fit_transform(self, X:np.ndarray) -> np.ndarray:
        
        '''
        Fits the PCA model to the input data and computes the principal components then
        transforms the input data by projecting it onto the principal components.
        
        Parameters
        ----------
        X : np.ndarray
            Input data matrix with shape (n_samples, n_features).
        '''
        
        if self.standardize:
            X = self.__checkStandarization(X)

        self.fit(X)
        
        return self.transform(X)
    
    @property
    def cumulative_variance_ratio(self) -> float:
        
        '''
        Returns the sum of the explained variance of all the principal components.
        
        Returns
        -------
        sum: float
            Explained variance of all the principal components.
        '''
        
        return np.sum(self.explained_variance_ratio)
    
    def plotComponents(self, X:np.ndarray, features:list=None) -> None:
        
        '''
        Plots a chart with a subplot for each principal component from the X matrix.
        
        Parameters
        ----------
        X : np.ndarray
            Input data matrix with shape (n_samples, n_features).
        features: list
            List with names for each principal component.
        '''
        
        from plotly.subplots import make_subplots
        import plotly.graph_objs as go
        
        size = math.ceil(X.shape[-1]**(1/2))
        if features == None:
            features = [f'PC{i}' for i in range(X.shape[-1])]
        
        fig = make_subplots(rows=size, cols=size)
        f = 0
        for r, c in [[i+1, j+1] for i in range(size) for j in range(size)]:
            fig.add_trace(go.Scatter(y=[line[f] for line in X], 
                                     name=features[f] if features != None else None), 
                          row=r, col=c)
            f += 1
            if f >= X.shape[-1]:
                break
        
        fig.update_layout(
            title='Regression of scatter data',
            hovermode="x"
        )
        fig.show()
    
    
    
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
    
    features = ['range_pu', 'open_to_close_pu', 'gap_pu', 'outlier_pu', 'day', 
                'month', 'year', 'week_day', 'is_quarter_end']

    X_train, X_test, y_train, y_test = utils.train_test_split(data[features], data['target'], 
                                                              random_state=41, test_size=0.2)
    #X_train_stand, X_test_stand = utils.standardize_data(X_train, X_test)
    
    pca = PCA(math.ceil(len(features)/2))
    pca.fit(X_train)
    X_train_scaled_pca = pca.transform(X_train)
    X_test_scaled_pca = pca.transform(X_test)
    print('Explained Variance Ratio: ', pca.explained_variance_ratio)
    print('Total Variance Ratio: ', pca.cumulative_variance_ratio)
    pca.plotComponents(X_test_scaled_pca)
    
    import plotly.express as px
    
    fig = px.scatter(x=X_test_scaled_pca[:,0], y=X_test_scaled_pca[:,1])
    fig.update_layout(
        title="PCA transformed data",
        xaxis_title="PC1",
        yaxis_title="PC2"
    )
    fig.show()