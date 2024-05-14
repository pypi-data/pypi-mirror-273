
import math
import pickle
import numpy as np
import pandas as pd

import utils

class SupportVectorMachine:
    
    '''
    A Support Vector Machine (SVM) implementation using gradient descent.
    
    The goal is to find a hyperplane that separates the data into 2 
    categories (Binary Classification).

    Parameters
    -----------
    iterations: int
        The number of iterations for gradient descent.
    lr: float
        The learning rate for gradient descent.
    lambdaa: float
        The regularization parameter.

    Attributes
    -----------
    lambdaa: float
        The regularization parameter.
    iterations: int
        The number of iterations for gradient descent.
    learning_rate: float
        The learning rate for gradient descent.
    w: np.ndarray
        The weights.
    b: float
        The bias.

    Methods
    --------
    initialize_parameters(X)
        Initializes the weights and bias.
    gradient_descent(X, y)
        Updates the weights and bias using gradient descent.
    update_parameters(dw, db)
        Updates the weights and bias.
    fit(X, y)
        Fits the SVM to the data.
    predict(X)
        Predicts the labels for the given data.
    '''

    def __init__(self, iterations:int=1000, learning_rate:float=0.01, 
                 lambdaa:float=0.01) -> None:
        
        '''
        Initializes the SVM model.

        Parameters:
        -----------
        iterations: int
            The number of iterations for gradient descent.
        learning_rate: float
            The learning rate for gradient descent.
        lambdaa: float
            The regularization parameter.
        '''
        
        self.lambdaa = lambdaa
        self.iterations = iterations
        self.learning_rate = learning_rate
        self.W = None
        self.b = None

    def initialize_parameters(self, X:np.ndarray) -> None:
        
        '''
        Initializes the weights and bias.

        Parameters:
        -----------
        X: np.ndarray
            The input data.
        '''
        
        self.W = np.zeros(X.shape[1])
        self.b = 0

    def gradient_descent(self, X:np.ndarray, y:np.ndarray) -> None:
        
        '''
        Updates the weights and bias using gradient descent.

        Parameters:
        -----------
        X : np.ndarray
            The input data.
        y : np.ndarray
            The target values.
        '''
        
        y_ = np.where(y <= 0, -1, 1)
        for i, x in enumerate(X):
            if y_[i] * (np.dot(x, self.W) - self.b) >= 1:
                dw = 2 * self.lambdaa * self.W
                db = 0
            else:
                dw = 2 * self.lambdaa * self.W - np.dot(x, y_[i])
                db = y_[i]
            self.update_parameters(dw, db)

    def update_parameters(self, dw:np.ndarray, db:float) -> None:
        
        '''
        Updates the weights and bias.

        Parameters:
        -----------
        dw: np.ndarray
            The change in weights.
        db: np.ndarray
            The change in bias.
        '''
        
        self.W = self.W - self.learning_rate * dw
        self.b = self.b - self.learning_rate * db

    def fit(self, X:np.ndarray, y:np.ndarray) -> None:
        
        '''
        Fits the SVM to the data.

        Parameters:
        -----------
        X: np.ndarray
            The input data.
        y: np.ndarray
            The target values.
        '''
        X = X if round(np.mean(X)) == 0 and round(np.std(X)) == 1 else utils.scale(X)
        self.initialize_parameters(X)
        for i in range(self.iterations):
            self.gradient_descent(X, y)

    def predict(self, X:np.ndarray) -> np.ndarray:
        
        '''
        Predicts the class labels for the test data.

        Parameters
        ----------
        X: np.ndarray
            The input data with shape (n_samples, n_features).

        Returns
        -------
        predictions: np.ndarray
            The predicted class labels with shape (n_samples,).
        '''
        
        # get the outputs
        X = X if round(np.mean(X)) == 0 and round(np.std(X)) == 1 else utils.scale(X)
        output = np.dot(X, self.W) - self.b
        # set predictions to 0 if they are less than 0 else set them to 1
        predictions = np.where(output < 0, 0, 1)
        
        return predictions
    
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
                
    def save_model(self, filename:str='last_SVM_model.pkl') -> None:

        '''
        Save the trained model to a file using pickle.

        Parameters
        ----------
        filename: str
            The name of the file to save the model to.
        '''

        model_data = {
            'learning_rate': self.learning_rate,
            'lambdaa': self.lambdaa,
            'iterations': self.iterations,
            'W': self.W,
            'b': self.b
        }

        with open(filename, 'wb') as file:
            pickle.dump(model_data, file)

    @classmethod
    def load_model(cls, filename:str='last_SVM_model.pkl'):

        '''
        Load a trained model from a file using pickle.

        Parameters
        ----------
        filename: str
            The name of the file to load the model from.

        Returns
        -------
        loaded_model: SupportVectorMachine
            An instance of the SupportVectorMachine class with loaded parameters.
        '''

        with open(filename, 'rb') as file:
            model_data = pickle.load(file)

        # Create a new instance of the class and initialize it with the loaded parameters
        loaded_model = cls(model_data['iterations'], model_data['learning_rate'], 
                           model_data['lambdaa'])
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

    X_train, X_test, y_train_raw, y_test_raw = utils.train_test_split(data[features], data['target'], 
                                                              random_state=41, test_size=0.2)
    X_train_stand, X_test_stand = utils.standardize_data(X_train, X_test)

    model = SupportVectorMachine(iterations=1000, learning_rate=0.0001, lambdaa=0.01)
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
    print(model.getWeights(features))