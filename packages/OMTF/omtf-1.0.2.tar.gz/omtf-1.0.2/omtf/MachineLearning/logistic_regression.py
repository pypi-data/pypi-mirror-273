
import pickle
import numpy as np
import pandas as pd
import plotly.express as px

import utils

class LogisticRegression:
    
    # From: https://www.kaggle.com/code/fareselmenshawii/logistic-regression-from-scratch
    
    '''
    Logistic Regression model.
    
    Logistic regression is a widely used model in machine learning for binary 
    classification tasks. It models the probability that a given input belongs 
    to a particular class. 

    Parameters
    ----------
    learning_rate: float
        Learning rate for the model.

    Methods
    -------
    initialize_parameter(): Initializes the parameters of the model.
    sigmoid(z): Computes the sigmoid activation function for given input z.
    forward(X): Computes forward propagation for given input X.
    compute_cost(predictions): Computes the cost function for given predictions.
    compute_gradient(predictions): Computes the gradients for the model using given predictions.
    fit(X, y, iterations, plot_cost): Trains the model on given input X and labels y for specified iterations.
    predict(X): Predicts the labels for given input X.
    '''

    def __init__(self, learning_rate:float=0.0001, convergence_tol:float=0.00000000001) -> None:
        
        '''
        Constructor method that initializes the LogisticRegression object.

        Parameters
        ----------
        learning_rate : float
            The learning rate used in gradient descent. Defults to 0.0001.
        convergence_tol: float
            The tolerance for convergence (stopping criterion). Defaults to 0.00000000001.
        '''
        
        np.random.seed(1)
        self.learning_rate = learning_rate
        self.convergence_tol = convergence_tol

    def initialize_parameter(self) -> None:
        
        '''
        Initializes the parameters of the model.
        '''
        
        self.W = np.zeros(self.X.shape[1])
        self.b = 0.0

    def forward(self, X:np.ndarray) -> (np.ndarray):

        '''
        Compute the forward propagation for given input X.

        Parameters
        ----------
        X: np.ndarray
            Input data of shape (m, n_features).

        Returns
        -------
        return: np.ndarray
            Output data of shape (m,).
        '''
        
        # print(X.shape, self.W.shape)
        Z = np.matmul(X, self.W) + self.b
        A, cache = utils.sigmoid(Z)
        
        return A

    def compute_cost(self, predictions:np.ndarray) -> float:
        
        '''
        Computes the cost function for given predictions.

        Parameters
        ----------
        predictions: np.ndarray
            Predictions of shape (m,).

        Returns
        -------
        return: float
            Cost of the model.
        '''
        
        # compute the cost
        cost = np.sum((-np.log(predictions + 1e-8) * self.y) + (-np.log(1 - predictions + 1e-8)) * \
                        (1 - self.y))  # we are adding small value epsilon to avoid log of 0
        
        return cost / self.X.shape[0]

    def compute_gradient(self, predictions:np.ndarray) -> None:
        
        '''
        Computes the gradients for the model using given predictions.

        Parameters
        ----------
        predictions: np.ndarray
            Predictions of the model.
        '''
        
        # get training shape
        m = self.X.shape[0]

        # compute gradients and scale them
        self.dW = np.array([np.mean(grad) for grad in \
                    np.matmul(self.X.T, (predictions - self.y)) ]) * 1/m
        self.db = np.sum(np.subtract(predictions, self.y)) * 1/m

    def fit(self, X:np.ndarray, y:np.ndarray, iterations:int=1000000, 
            plot_cost:bool=True, verbose:bool=True) -> None:

        '''
        Trains the model on given input X and labels y for specified iterations.

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
        
        X = X if round(np.mean(X)) == 0 and round(np.std(X)) == 1 else utils.scale(X)
        self.X = X
        self.y = y
        self.initialize_parameter()
        
        self.dW_hist, self.db_hist, self.W_hist, self.b_hist, self.costs = [], [], [], [], []

        for i in range(iterations):
            # forward propagation
            predictions = self.forward(self.X)

            # compute cost
            self.cost = self.compute_cost(predictions)

            # compute gradients
            self.compute_gradient(predictions)

            # update parameters
            self.W = self.W - self.learning_rate * self.dW
            self.b = self.b - self.learning_rate * self.db
            
            self.costs.append(self.cost)
            self.dW_hist.append(self.dW)
            self.db_hist.append(self.db)
            self.W_hist.append(self.W)
            self.b_hist.append(self.b)

            # print cost every 100 iterations
            if i % 10000 == 0 and verbose:
                print(f'Cost after iteration {i}: {self.cost}')

            if i > 0 and abs(self.costs[-1] - self.costs[-2]) < self.convergence_tol:
                print(f'Converged after {i} iterations.')
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
        
        X = X if round(np.mean(X)) == 0 and round(np.std(X)) == 1 else utils.scale(X)
        self.X = X
        
        return np.round(self.forward(X))
    
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
    
    def save_model(self, filename:str='last_LogReg_model.pkl') -> None:

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
    def load_model(cls, filename:str='last_LogReg_model.pkl'):

        '''
        Load a trained model from a file using pickle.

        Parameters
        ----------
        filename: str
            The name of the file to load the model from.

        Returns
        -------
        loaded_model: LogisticRegression
            An instance of the LogisticRegression class with loaded parameters.
        '''

        with open(filename, 'rb') as file:
            model_data = pickle.load(file)

        # Create a new instance of the class and initialize it with the loaded parameters
        loaded_model = cls(model_data['learning_rate'], model_data['convergence_tol'])
        loaded_model.W = model_data['W']
        loaded_model.b = model_data['b']

        return loaded_model

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

    X_train, X_test, y_train, y_test = utils.train_test_split(data[features], data['target'], 
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

    model = LogisticRegression(learning_rate=0.0001)
    model.fit(X_train_stand, y_train, 1000000, verbose=False)
    
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
        if just_side:
            y_df['Orig_side'] = np.where(y_df['Orig'] > y_df['Orig'].shift(1), 1, 
                                np.where(y_df['Orig'] < y_df['Orig'].shift(1), -1, 0))
            y_df['Pred_side'] = np.where(y_df['Pred'] > y_df['Pred'].shift(1), 1, 
                                np.where(y_df['Pred'] < y_df['Pred'].shift(1), -1, 0))
            success = y_df[y_df['Pred_side'] == y_df['Orig_side']]
            error = y_df[y_df['Pred_side'] != y_df['Orig_side']]
        else:
            success = y_df[y_df['Pred'] == y_df['Orig']]
            error = y_df[y_df['Pred'] != y_df['Orig']]
        
        wr = len(success)/len(y_df)
        rr = (success['Range'].abs().mean())/(error['Range'].abs().mean())
        print(f'Side Success: {wr:.2%}')
        print(f'Risk Reward: {rr:.2} R')
        print(f"Spectancy: {(wr * success['Range'].abs().mean() - (1-wr) * error['Range'].abs().mean()):.2%}")

    # Plot prediction
    model.plotPrediction(X=X_test_stand, y=y_test)
    print(model.getWeights(features))