
import math
import pickle
import numpy as np
import pandas as pd
import plotly.express as px

import utils


class LinearRegression:
    
    # From: https://www.kaggle.com/code/fareselmenshawii/linear-regression-from-scratch

    '''
    Linear Regression Model with Gradient Descent

    Linear regression is a supervised machine learning algorithm used for modeling the relationship
    between a dependent variable (target) and one or more independent variables (features) by fitting
    a linear equation to the observed data.

    This class implements a linear regression model using gradient descent optimization for training.
    It provides methods for model initialization, training, prediction, and model persistence.

    Parameters:
        learning_rate (float): The learning rate used in gradient descent.
        convergence_tol (float, optional): The tolerance for convergence (stopping criterion). Defaults to 1e-6.

    Attributes:
        W (numpy.ndarray): Coefficients (weights) for the linear regression model.
        b (float): Intercept (bias) for the linear regression model.

    Methods:
        initialize_parameters(n_features): Initialize model parameters.
        forward(X): Compute the forward pass of the linear regression model.
        compute_cost(predictions): Compute the mean squared error cost.
        backward(predictions): Compute gradients for model parameters.
        fit(X, y, iterations, plot_cost=True): Fit the linear regression model to training data.
        predict(X): Predict target values for new input data.
        save_model(filename=None): Save the trained model to a file using pickle.
        load_model(filename): Load a trained model from a file using pickle.

    Examples:
        >>> from linear_regression import LinearRegression
        >>> model = LinearRegression(learning_rate=0.01)
        >>> model.fit(X_train, y_train, iterations=1000)
        >>> predictions = model.predict(X_test)
    '''

    def __init__(self, learning_rate:float=0.01, convergence_tol:float=0.000001) -> None:
        
        '''
        Constructor method that initializes the LinearRegression object.

        Parameters
        ----------
        learning_rate : float
            The learning rate used in gradient descent. Defults to 0.01.
        convergence_tol: float
            The tolerance for convergence (stopping criterion). Defaults to 0.000001.
        '''

        self.learning_rate = learning_rate
        self.convergence_tol = convergence_tol
        self.W = None
        self.b = None

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
    
    def initialize_parameters(self, n_features:int) -> None:

        '''
        Initialize model parameters.

        Parameters
        ----------
        n_features: int
            The number of features in the input data.
        '''

        self.W = np.random.randn(n_features) * 0.01
        self.b = 0

    def forward(self, X:np.ndarray) -> np.ndarray:

        '''
        Compute the forward pass of the linear regression model.

        Parameters
        ----------
        X: np.ndarray
            Input data of shape (m, n_features).

        Returns
        -------
        return: np.ndarray
            Predictions of shape (m,).
        '''

        return np.dot(X, self.W) + self.b

    def compute_cost(self, predictions:np.ndarray) -> float:

        '''
        Compute the mean squared error cost.

        Parameters
        ----------
        predictions: np.ndarray
            Predictions of shape (m,).

        Returns
        -------
        return: float
            Mean squared error cost.
        '''
        
        return np.sum(np.square(predictions - self.y)) / (2*len(predictions))

    def backward(self, predictions:np.ndarray) -> None:

        '''
        Compute gradients for model parameters.

        Parameters
        ----------
        predictions: np.ndarray
            Predictions of shape (m,).

        Updates
        -------
        dW: np.ndarray
            Gradient of W.
        db: float
            Gradient of b.
        '''

        n = len(predictions) 
        self.dW = np.dot(predictions - self.y, self.X) / n
        self.db = np.sum(predictions - self.y) / n

    def fit(self, X:np.ndarray, y:np.ndarray, iterations:int=10000, 
            plot_cost:bool=True, verbose:bool=True) -> None:

        '''
        Fit the linear regression model to the training data.

        Parameters
        ----------
        X: np.ndarray
            Training input data of shape (m, n_features).
        y: np.ndarray
            Training labels of shape (m,).
        iterations: int
            The number of iterations for gradient descent. Also named epochs.
        plot_cost: bool
            Whether to plot the cost during training. Defaults to True.
        verbose: bool
            True to print training results.

        Raises
        ------
        AssertionError: If input data and labels are not NumPy arrays or have mismatched shapes.

        Plots
        -----
        Plotly line chart showing cost vs. iteration (if plot_cost is True).
        '''

        assert isinstance(X, np.ndarray), "X must be a NumPy array"
        assert isinstance(y, np.ndarray), "y must be a NumPy array"
        assert X.shape[0] == y.shape[0], "X and y must have the same number of samples"
        assert iterations > 0, "Iterations must be greater than 0"

        X = self.__checkStandarization(X)
        self.X = X
        self.y = y
        self.initialize_parameters(self.X.shape[1])

        self.dW_hist, self.db_hist, self.W_hist, self.b_hist, self.costs = [], [], [], [], []

        for i in range(iterations):
            # forward propagation
            predictions = self.forward(self.X)
            
            # compute cost
            self.cost = self.compute_cost(predictions)
            
            self.backward(predictions)
            
            # update parameters
            self.W = self.W - self.learning_rate * self.dW
            self.b = self.b - self.learning_rate * self.db
            
            self.costs.append(self.cost)
            self.dW_hist.append(self.dW)
            self.db_hist.append(self.db)
            self.W_hist.append(self.W)
            self.b_hist.append(self.b)

            if i % 100 == 0 and verbose:
                print(f'Iteration: {i}, Cost: {self.cost}')

            if i > 0 and abs(self.costs[-1] - self.costs[-2]) < self.convergence_tol:
                print(f'Converged after {i} iterations.')
                break

            if len(self.costs) > 2 and self.costs[-1] > self.costs[-2]:
                print(f'Stoped after {i} iterations as it is not converging.')
                break

        if plot_cost:
            self.plotCosts()
            
    def plotCosts(self, template:str='plotly_dark', color:str='#41BEE9') -> None:
        
        '''
        Plotly line chart showing cost vs. iteration.

        Parameters
        ----------
        template: str
            Template from the list available: ['ggplot2', 'seaborn', 'simple_white', 'plotly',
            'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
            'ygridoff', 'gridon', 'none']. Defaults to 'plotly_dark'.
        color: str
            Hexagesimal color.

        Plots
        -----
        Plotly line chart showing cost vs. iteration.
        '''
        
        color = color if '#' in color else f'#{color}'
        fig = px.line(y=self.costs, title="Cost vs Iteration", template=template)
        fig.update_layout(
            title_font_color=color,
            xaxis=dict(color=color, title="Iterations"),
            yaxis=dict(color=color, title="Cost")
        )
        fig.show()

    def predict(self, X:np.ndarray) -> np.ndarray:

        '''
        Predict target values for new input data.

        Parameters
        ----------
        X: np.ndarray
            Input data of shape (m, n_features).

        Returns
        -------
        return: np.ndarray
            Predicted target values of shape (m,).
        '''

        X = self.__checkStandarization(X)
        self.X = X

        return self.forward(self.X)
    
    def getWeights(self, features:list) -> pd.DataFrame:

        '''
        Get the weights from the last training.

        Parameters
        ----------
        features: list
            List of the features names associated to the weights.

        Returns
        -------
        return: pd.DataFrame
            DataFrame containing the weights ranked.
        '''
        
        return pd.DataFrame({'Weights':self.W}, index=features) \
                .sort_values(by='Weights', ascending=False)
    
    def save_model(self, filename:str='last_LinReg_model.pkl') -> None:

        '''
        Save the trained model to a file using pickle.

        Parameters
        ----------
        filename: str
            The name of the file to save the model to.
        '''

        model_data = {
            'learning_rate': self.learning_rate,
            'convergence_tol': self.convergence_tol,
            'W': self.W,
            'b': self.b
        }

        with open(filename, 'wb') as file:
            pickle.dump(model_data, file)

    @classmethod
    def load_model(cls, filename:str='last_LinReg_model.pkl'):

        '''
        Load a trained model from a file using pickle.

        Parameters
        ----------
        filename: str
            The name of the file to load the model from.

        Returns
        -------
        loaded_model: LinearRegression
            An instance of the LinearRegression class with loaded parameters.
        '''

        with open(filename, 'rb') as file:
            model_data = pickle.load(file)

        # Create a new instance of the class and initialize it with the loaded parameters
        loaded_model = cls(model_data['learning_rate'], model_data['convergence_tol'])
        loaded_model.W = model_data['W']
        loaded_model.b = model_data['b']

        return loaded_model
    
    def plotRegressions(self, X:np.ndarray=None, features:list=None) -> None:
        
        '''
        Plotly line chart showing the linear regression for each feature.

        Parameters
        ----------
        X: np.ndarray
            Input data of shape (m, n_features).
        features: list
            List of the features names.

        Plots
        -----
        Plotly line chart showing the linear regression for each feature.
        '''

        X = self.X if not isinstance(X, np.ndarray) else X
        
        from plotly.subplots import make_subplots
        import plotly.graph_objs as go
        size = math.ceil(len(X[0])**(1/2))
        
        fig = make_subplots(rows=size, cols=size)
        f = 0
        for r, c in [[i+1, j+1] for i in range(size) for j in range(size)]:
            fig.add_trace(go.Scatter(y=[line[f] for line in X], 
                                     name=features[f] if features != None else None), 
                          row=r, col=c)
            fig.add_trace(go.Scatter(y=[self.W[f] * i + self.b for i in range(len(X))]), row=r, col=c)
            f += 1
            if f >= len(X[0]):
                break
        
        fig.update_layout(
            xaxis_title='X',
            yaxis_title='Y',
            title='Regression of scatter data',
            hovermode="x"
        )
        fig.show()
        
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

        X = self.X if not isinstance(X, np.ndarray) else utils.scale(X)
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
            Dictionary containing 'mse', 'rmse' and 'r_squared' for the model.
        '''
        
        mse = utils.RegressionMetrics.mean_squared_error(y_real, y_pred)
        rmse = utils.RegressionMetrics.root_mean_squared_error(y_real, y_pred)
        r_squared = utils.RegressionMetrics.r_squared(y_real, y_pred)
        
        if show:
            print(f"Mean Squared Error (MSE): {mse}")
            print(f"Root Mean Squared Error (RMSE): {rmse}")
            print(f"R-squared (Coefficient of Determination): {r_squared}")
            
        return {'mse':mse, 'rmse':rmse, 'r_squared':r_squared}

# TODO: Check the Theil Sen Regression ------------------------------------------------------------------------
        
    


if __name__ == '__main__':

    import yfinance as yf
    from principal_component import PCA
    
    pca_apply = False

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
        
    data['target'] = data['close']#np.where(data['open'] < data['close'], 1, 0)
    data.dropna(inplace=True)

    features = ['range_pu', 'open_to_close_pu', 'gap_pu', 'outlier_pu', 'day', 'month', 'week_day', 'is_quarter_end']

    X_train_stand, X_test_stand, y_train, y_test = utils.train_test_split(data[features], data['target'], 
                                                              random_state=41, test_size=0.5)

    #X_train_stand, X_test_stand = utils.standardize_data(X_train_stand, X_test_stand)
    
    if pca_apply:
        pca = PCA(len(features))
        pca.fit(X_train_stand)
        X_train_stand = pca.transform(X_train_stand)
        X_test_stand = pca.transform(X_test_stand)
        pca.plotComponents(X_train_stand)
        pca.cumulative_variance_ratio
        
        features = [f'PC{i}' for i in range(X_train_stand.shape[-1])]

    model = LinearRegression(learning_rate=0.01)
    model.fit(X_train_stand, y_train, 10000, verbose=False)

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
        y_df['Orig_side'] = np.where(y_df['Orig'] > y_df['Orig'].shift(1), 1, 
                            np.where(y_df['Orig'] < y_df['Orig'].shift(1), -1, 0))
        y_df['Pred_side'] = np.where(y_df['Pred'] > y_df['Pred'].shift(1), 1, 
                            np.where(y_df['Pred'] < y_df['Pred'].shift(1), -1, 0))
        success = y_df[y_df['Pred_side'] == y_df['Orig_side']]
        error = y_df[y_df['Pred_side'] != y_df['Orig_side']]
        
        wr = len(success)/len(y_df)
        rr = (success['Range'].abs().mean())/(error['Range'].abs().mean())
        print(f'Side Success: {wr:.2%}')
        print(f'Risk Reward: {rr:.2} R')
        print(f"Spectancy: {(wr * success['Range'].abs().mean() - (1-wr) * error['Range'].abs().mean()):.2%}")

    # Plot prediction
    model.plotPrediction(X=X_test_stand, y=y_test)
    print(model.getWeights(features))