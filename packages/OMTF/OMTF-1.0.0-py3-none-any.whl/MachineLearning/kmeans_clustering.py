
import math
import pickle
import numpy as np
import pandas as pd

import utils

class Kmeans:

    # From: https://www.kaggle.com/code/fareselmenshawii/kmeans-from-scratch

    """
    K-Means clustering algorithm implementation.
    K-means clustering is a method used to group data points into clusters.

    Parameters:
        K (int): Number of clusters

    Attributes:
        K (int): Number of clusters
        centroids (numpy.ndarray): Array containing the centroids of each cluster

    Methods:
        __init__(self, K): Initializes the Kmeans instance with the specified number of clusters.
        initialize_centroids(self, X): Initializes the centroids for each cluster by selecting K random points from the dataset.
        assign_points_centroids(self, X): Assigns each point in the dataset to the nearest centroid.
        compute_mean(self, X, points): Computes the mean of the points assigned to each centroid.
        fit(self, X, iterations=10): Clusters the dataset using the K-Means algorithm.
    """
    
    def __init__(self, K:int) -> None:

        assert K > 0, "K should be a positive integer."
        self.K = K
        
    def initialize_centroids(self, X:int) -> None:

        assert X.shape[0] >= self.K, "Number of data points should be greater than or equal to K."
        
        randomized_X = np.random.permutation(X.shape[0]) 
        centroid_idx = randomized_X[:self.K] # get the indices for the centroids
        self.centroids = X[centroid_idx] # assign the centroids to the selected points
        
    def assign_points_centroids(self, X:np.ndarray) -> np.ndarray:

        """
        Assign each point in the dataset to the nearest centroid.
        
        Parameters:
        X (numpy.ndarray): dataset to cluster
        
        Returns:
        numpy.ndarray: array containing the index of the centroid for each point
        """

        X = np.expand_dims(X, axis=1) # expand dimensions to match shape of centroids
        distance = np.linalg.norm((X - self.centroids), axis=-1) # calculate Euclidean distance between each point and each centroid
        points = np.argmin(distance, axis=1) # assign each point to the closest centroid

        assert len(points) == X.shape[0], "Number of assigned points should equal the number of data points."

        return points
    
    def compute_mean(self, X:np.ndarray, points:np.ndarray) -> np.ndarray:

        """
        Compute the mean of the points assigned to each centroid.
        
        Parameters:
        X (numpy.ndarray): dataset to cluster
        points (numpy.ndarray): array containing the index of the centroid for each point
        
        Returns:
        numpy.ndarray: array containing the new centroids for each cluster
        """

        centroids = np.zeros((self.K, X.shape[1])) # initialize array to store centroids
        for i in range(self.K):
            centroid_mean = X[points == i].mean(axis=0) # calculate mean of the points assigned to the current centroid
            centroids[i] = centroid_mean # assign the new centroid to the mean of its points

        return centroids
    
    def fit(self, X:np.ndarray, iterations:int=10) -> (np.ndarray, np.ndarray):

        """
        Cluster the dataset using the K-Means algorithm.
        
        Parameters:
        X (numpy.ndarray): dataset to cluster
        iterations (int): number of iterations to perform (default=10)
        
        Returns:
        numpy.ndarray: array containing the final centroids for each cluster
        numpy.ndarray: array containing the index of the centroid for each point
        """

        self.initialize_centroids(X) # initialize the centroids

        for i in range(iterations):

            points = self.assign_points_centroids(X) # assign each point to the nearest centroid
            self.centroids = self.compute_mean(X, points) # compute the new centroids based on the mean of their points
            
            # Assertions for debugging and validation
            assert len(self.centroids) == self.K, "Number of centroids should equal K."
            assert X.shape[1] == self.centroids.shape[1], "Dimensionality of centroids should match input data."
            assert max(points) < self.K, "Cluster index should be less than K."
            assert min(points) >= 0, "Cluster index should be non-negative."
            
        return self.centroids, points
    


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