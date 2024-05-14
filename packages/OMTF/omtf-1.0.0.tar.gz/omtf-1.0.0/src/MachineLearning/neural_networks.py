
import math
import pickle
import numpy as np
import pandas as pd
import plotly.express as px

import utils

class NeuralNetwork:

    '''
    Initialize Parameters: We start by initializing the weights and biases of the model. 
    For each layer l in the network, we initialize  W[l] to be a matrix with dimensions 
    (n[l],n[l−1]), where  n[l] is the number of units in layer  l and  n[l−1] is the number 
    of units in the previous layer. We also initialize  b[l] to be a vector with dimensions 
    (n[l],1).

    Forward Propagation: In the forward pass, we propagate through the network calculating 
    the output of every layer. For each layer l in the network, we calculate:

        Z[l]=W[l].A[l−1]+b[l]

        A[l]=g(Z[l])
    
    where  A[0]=X
    is the input to the network and  g(.)
    is the activation function used in layer  l
    .

    Compute Cost: We calculate the cost function to determine how well we are doing. For binary 
    classification problems, we often use the binary cross-entropy to measure our network 
    performance. The cost function can be computed as:

        J=−1/m* ∑ (i=1 m) [y(i) log(aL) + (1−y(i)) log(1−aL)]
    
    where  aL is the predicted output of the network for the  i-th input example and  y(i)
    is the true output for the  i-th input example.

    Backpropagation: In the backward pass, we compute the derivatives of the loss function 
    with respect to the parameters of the network using the chain rule of differentiation. 
    Specifically, we calculate the derivatives of the cost function with respect to  Z[l], which 
    can then be used to calculate the derivatives of the cost function with respect to W[l] and b[l].

    Updating Parameters: We update the parameters of the network using gradient descent, which 
    tries to reduce the cost by adjusting the parameters in the opposite direction of the gradient. 
    The gradient descent rule is, for each layer l in the network:

        W[l]=W[l]−α dW[l]
        
        b[l]=b[l]−α db[l]
        
    where α is the learning rate and dW[l] and db[l] are the derivatives of the cost function with 
    respect to W[l] and b[l], respectively.
    '''
    
    class Optimizers:
        MOMENTUM = 'momentum'
        RMSPROP = 'rmsprop'
        ADAM = 'adam' 
    
    def __init__(self, layer_dimensions:list, learning_rate:float=0.00001, 
                 verbose:bool=False) -> None:
        
        '''
        Parameters
        ----------
        layer_dimensions: list
            List containing the dimensions of each layer in our network
        learning_rate: float
            Learning rate of the network.
        '''

        self.layer_dimensions = layer_dimensions
        self.n_layers =  len(layer_dimensions)
        self.learning_rate = learning_rate
        self.verbose = verbose
        
    def initialize_parameters(self, verbose:bool=False) -> None:
        
        '''
        Initializes the parameters.

        Parameters
        ----------
        verbose: bool
            True to print the evolution.
        '''
        
        np.random.seed(3)
        for l in range(1, self.n_layers):
            rows = l - 1
            cols = l 
            vars(self)[f'W{l}'] = np.random.randn(self.layer_dimensions[cols], 
                                                  self.layer_dimensions[rows]) * 0.01
            vars(self)[f'b{l}'] = np.zeros((self.layer_dimensions[cols], 1))
            
            if verbose or self.verbose:
                print('Layer: ', l)
                print('W: ', vars(self)['W' + str(l)], '\nSize: ', vars(self)['W' + str(l)].shape)
                print('b: ', vars(self)['b' + str(l)], '\nSize: ', vars(self)['b' + str(l)].shape)

    def _linear_forward(self, A:np.ndarray, W:np.ndarray, b:np.ndarray
                        ) -> (np.ndarray, tuple):
        
        '''
        Implements the linear part of a layer's forward propagation.

        Parameters
        ----------
        A: np.ndarray
            Activations from previous layer (size of previous layer, number of examples).
        W: np.ndarray
            Weights matrix, numpy array of shape (size of current layer, size of previous layer).
        b: np.ndarray
            Bias vector, numpy array of shape (size of the current layer, 1).

        Returns
        -------
        Z: np.ndarray
            Pre-activation parameter.
        cache: tuple
            Tuple containing "A", "W" and "b"  for backpropagation.
        '''
        
        # Compute Z
        Z = np.dot(W,A) + b
        # Cache  A, W , b for backpropagation
        cache = (A, W, b)
        
        return Z, cache
    
    def _forward_propagation(self, A_prev:np.ndarray, W:np.ndarray, b:np.ndarray, 
                             activation:str) -> (np.ndarray, tuple):
        
        '''
        Implements the forward propagation for a network layer.

        Parameters
        ----------
        A_prev: np.ndarray
            Activations from previous layer, shape : (size of previous layer, number of examples).
        W: np.ndarray
            Weights matrix, numpy array of shape (size of current layer, size of previous layer).
        b: np.ndarray
            Bias vector, numpy array of shape (size of the current layer, 1).
        activation: str
            The activation to be used in this layer.

        Returns
        -------
        A: np.ndarray
            The output of the activation function.
        cache: tuple
            Tuple containing "linear_cache" and "activation_cache" for backpropagation.
        '''
        
        Z, linear_cache = self._linear_forward(A_prev, W, b)
            
        # Compute Z using the function defined above, compute A using the activaiton function
        if activation == "sigmoid":
            A, activation_cache = utils.sigmoid(Z) 
        elif activation == "relu":
            A, activation_cache = utils.relu(Z) 
        
        #Store the cache for backpropagation
        cache = (linear_cache, activation_cache)
        
        return A, cache

    def forward_propagation(self, X:np.ndarray) -> (np.ndarray, list):
        
        '''
        Implements forward propagation for the whole network.

        Parameters
        ----------
        X: np.ndarray
            Array of shape (input size, number of examples).

        Returns
        -------
        AL: np.ndarray
            Last post-activation value.
        caches: list
            List of cache returned by _forward_propagation helper function.
        '''
        
        # Initialize empty list to store caches
        caches = []
        # Set initial A to X 
        A = X
        L =  self.n_layers - 1
        for l in range(1, L):
            A_prev = A 
            # Forward propagate through the network except the last layer
            A, cache = self._forward_propagation(A_prev, vars(self)['W' + str(l)], 
                                                 vars(self)['b' + str(l)], "relu")
            caches.append(cache)
            
        # Forward propagate through the output layer and get the predictions
        predictions, cache = self._forward_propagation(A, vars(self)['W' + str(L)], 
                                                       vars(self)['b' + str(L)], "sigmoid")
        
        # Append the cache to caches list recall that cache will be (linear_cache, activation_cache)
        caches.append(cache)

        return predictions, caches
    
    def compute_cost(self, predictions:np.ndarray, y:np.ndarray) -> np.ndarray:
        
        '''
        Implements the cost function .

        Parameters
        ----------
        predictions: np.ndarray
            The model predictions, shape : (1, number of examples).
        y: np.ndarray
            The true values, shape : (1, number of examples).

        Returns
        -------
        cost: np.ndarray
            Cross-entropy cost.
        '''
        
        # Get number of training examples
        m = y.shape[0]
        # Compute cost we're adding small epsilon for numeric stability
        cost = (-1/m) * (np.dot(y, np.log(predictions+1e-9).T) + \
                        np.dot((1-y), np.log(1-predictions+1e-9).T))
        # squeeze the cost to set it into the correct shape 
        cost = np.squeeze(cost)
        
        return cost   
        
    def _linear_backward(self, dZ:np.ndarray, cache:tuple
                         ) -> (np.ndarray, np.ndarray, np.ndarray):
        
        '''
        Implements the linear portion of backward propagation.

        Parameters
        ----------
        dZ: np.ndarray
            Gradient of the cost with respect to the linear output of the current layer.
        cache: tuple
            Tuple of values (A_prev, W, b) coming from the forward propagation in the current layer.

        Returns
        -------
        dA_prev: np.ndarray
            Gradient of the cost with respect to the activation (of the previous layer l-1), 
            same shape as A_prev.
        dW: np.ndarray
            Gradient of the cost with respect to W (current layer l), same shape as W.
        db: np.ndarray
            Gradient of the cost with respect to b (current layer l), same shape as b.
        '''
        
        # Get the cache from forward propagation
        A_prev, W, b = cache
        # Get number of training examples
        m = A_prev.shape[1]
        # Compute gradients for W, b and A
        dW = (1/m) * np.dot(dZ, A_prev.T)
        db = (1/m) * np.sum(dZ, axis=1, keepdims=True)
        dA_prev = np.dot(W.T,dZ)
        
        return dA_prev, dW, db
    
    def _back_propagation(self, dA:np.ndarray, cache:tuple, activation:str
                          ) -> (np.ndarray, np.ndarray, np.ndarray):
        
        '''
        Implements the backward propagation for a single layer.

        Parameters
        ----------
        dA: np.ndarray
            Post-activation gradient for current layer l.
        cache: tuple
            Tuple of values (linear_cache, activation_cache).
        activation: str
            The activation to be used in this layer. Choose one from: 'relu' or 'sigmoid'.

        Returns
        -------
        dA_prev: np.ndarray
            Gradient of the cost with respect to the activation (of the previous layer l-1), 
            same shape as A_prev.
        dW: np.ndarray
            Gradient of the cost with respect to W (current layer l), same shape as W.
        db: np.ndarray
            Gradient of the cost with respect to b (current layer l), same shape as b.
        '''
        
        # get the cache from forward propagation and activation derivates function
        linear_cache, activation_cache = cache
        # compute gradients for Z depending on the activation function
        if activation == "relu":
            dZ = utils.relu_backward(dA, activation_cache)

        elif activation == "sigmoid":
            dZ = utils.sigmoid_backward(dA, activation_cache)
            
        # Compute gradients for W, b and A 
        dA_prev, dW, db = self._linear_backward(dZ, linear_cache)
        
        return dA_prev, dW, db

    def back_propagation(self, predictions:np.ndarray, Y:np.ndarray, 
                         caches:list) -> None:
        
        '''
        Implements the backward propagation for the NeuralNetwork.

        Parameters
        ----------
        predictions: np.ndarray
            Output of the forward propagation.
        Y: np.ndarray
            True values.
        caches: list
            List of caches.
        '''
        
        L =  self.n_layers - 1
        # Get number of examples
        m = predictions.shape[1]
        Y = Y.reshape(predictions.shape) 
        # Initializing the backpropagation we're adding a small epsilon for numeric stability 
        dAL = - (np.divide(Y, predictions+1e-9) - np.divide(1 - Y, 1 - predictions+1e-9))
        current_cache = caches[L-1] # Last Layer
        # Compute gradients of the predictions
        vars(self)[f'dA{L-1}'], vars(self)[f'dW{L}'], vars(self)[f'db{L}'] = self._back_propagation(dAL, current_cache, "sigmoid")
        for l in reversed(range(L-1)):
            # update the cache
            current_cache = caches[l]
            # compute gradients of the network layers 
            vars(self)[f'dA{l}'] , vars(self)[f'dW{l+1}'], vars(self)[f'db{l+1}'] = self._back_propagation(vars(self)[f'dA{l + 1}'], current_cache, activation = "relu")
            
    def momentum(self, beta:float=0.9) -> None:
        
        '''
        Update parameters using Momentum.
        
        Parameters
        ----------
        beta: float
            The momentum hyperparameter.
        '''
        
        L = self.n_layers - 1
        for l in range(L):
            vars(self)[f'vdW{l+1}'] = np.zeros((vars(self)[f'W{l+1}'].shape[0], vars(self)[f'W{l+1}'].shape[1]))
            vars(self)[f'vdb{l+1}'] = np.zeros((vars(self)[f'b{l+1}'].shape[0], vars(self)[f'b{l+1}'].shape[1]))
            
        for l in range(L):
            vars(self)[f'vdW{l+1}'] = beta * vars(self)[f'vdW{l+1}'] + (1-beta) * vars(self)[f'dW{l+1}']
            vars(self)[f'vdb{l+1}'] = beta * vars(self)[f'vdb{l+1}'] + (1-beta) * vars(self)[f'db{l+1}']
            
            
            vars(self)[f'W{l+1}'] = vars(self)[f'W{l+1}'] - self.learning_rate*vars(self)[f'vdW{l+1}']
            vars(self)[f'b{l+1}'] = vars(self)[f'b{l+1}'] - self.learning_rate*vars(self)[f'vdb{l+1}']
       
    def rmsProp(self, beta:float=0.9) -> None:
        
        '''
        Update parameters using RMSProp.
        
        Parameters
        ----------
        beta: float
            The momentum hyperparameter.
        '''
        L = self.n_layers -1
        for l in range(L):
            vars(self)[f'sdW{l+1}'] = np.zeros((vars(self)[f'W{l+1}'].shape[0], vars(self)[f'W{l+1}'].shape[1]))
            vars(self)[f'sdb{l+1}'] = np.zeros((vars(self)[f'b{l+1}'].shape[0], vars(self)[f'b{l+1}'].shape[1]))
                
            
        for l in range(L):
            vars(self)[f'sdW{l+1}'] = beta * vars(self)[f'sdW{l+1}'] + (1-beta) * np.square(vars(self)[f'dW{l+1}'])
            vars(self)[f'sdb{l+1}'] = beta * vars(self)[f'sdb{l+1}'] + (1-beta) * np.square(vars(self)[f'db{l+1}'])
            
            vars(self)[f'sdW{l+1}'] = vars(self)[f'sdW{l+1}']/(1-beta**2)
            vars(self)[f'sdb{l+1}'] = vars(self)[f'sdb{l+1}']/(1-beta**2)

        
            vars(self)[f'W{l+1}'] = vars(self)[f'W{l+1}'] - self.learning_rate*vars(self)[f'dW{l+1}'] / np.sqrt(vars(self)[f'sdW{l+1}']+1e-9)
            vars(self)[f'b{l+1}'] = vars(self)[f'b{l+1}'] - self.learning_rate*vars(self)[f'db{l+1}'] / np.sqrt(vars(self)[f'sdb{l+1}']+1e-9)
      
    def adam(self, beta1:float=0.9, beta2:float=0.999) -> None:

        '''
        Update parameters using Adam.
        
        Parameters
        ----------
        beta1:float
            Exponential decay hyperparameter for the first moment estimates.
        beta2: float
            Exponential decay hyperparameter for the second moment estimates.
        '''

        L = self.n_layers - 1
        for l in range(L):
            vars(self)[f'vdW{l+1}'] = np.zeros((vars(self)[f'W{l+1}'].shape[0], vars(self)[f'W{l+1}'].shape[1]))
            vars(self)[f'vdb{l+1}'] = np.zeros((vars(self)[f'b{l+1}'].shape[0], vars(self)[f'b{l+1}'].shape[1]))     
            vars(self)[f'sdW{l+1}'] = np.zeros((vars(self)[f'W{l+1}'].shape[0], vars(self)[f'W{l+1}'].shape[1]))
            vars(self)[f'sdb{l+1}'] = np.zeros((vars(self)[f'b{l+1}'].shape[0], vars(self)[f'b{l+1}'].shape[1]))
            
        for l in range(L):
            vars(self)[f'vdW{l+1}'] = beta1 * vars(self)[f'vdW{l+1}'] + (1-beta1) * vars(self)[f'dW{l+1}']
            vars(self)[f'vdb{l+1}'] = beta1 * vars(self)[f'vdb{l+1}'] + (1-beta1) * vars(self)[f'db{l+1}']
            
            vars(self)[f'vdW{l+1}'] = vars(self)[f'vdW{l+1}']/(1-beta1**2)
            vars(self)[f'vdb{l+1}'] = vars(self)[f'vdb{l+1}']/(1-beta1**2)
            
            
            vars(self)[f'sdW{l+1}'] = beta2 * vars(self)[f'sdW{l+1}'] + (1-beta2) * np.square(vars(self)[f'dW{l+1}'])
            vars(self)[f'sdb{l+1}'] = beta2 * vars(self)[f'sdb{l+1}'] + (1-beta2) * np.square(vars(self)[f'db{l+1}'])
            
            vars(self)[f'sdW{l+1}'] = vars(self)[f'sdW{l+1}']/(1-beta2**2)
            vars(self)[f'sdb{l+1}'] = vars(self)[f'sdb{l+1}']/(1-beta2**2)

            vars(self)[f'W{l+1}'] = vars(self)[f'W{l+1}'] - self.learning_rate*vars(self)[f'vdW{l+1}'] / np.sqrt(vars(self)[f'sdW{l+1}']+1e-9)
            vars(self)[f'b{l+1}'] = vars(self)[f'b{l+1}'] - self.learning_rate*vars(self)[f'vdb{l+1}'] / np.sqrt(vars(self)[f'sdb{l+1}']+1e-9)
        
    def update_parameters(self, optimizer:Optimizers=None) -> None:
        
        '''
        Updates parameters 
        
        Parameters
        ----------
        optimizer: Optimizers
            The optimizer used. Default is None. If can be one of: 'momentum', 
            'rmsprop' or 'adam'. 
        '''
        
        L = self.n_layers - 1
        if optimizer == self.Optimizers.MOMENTUM:
            self.momentum(beta=0.9)
        elif optimizer == self.Optimizers.RMSPROP:
            np.seterr(divide='ignore', invalid='ignore')
            self.rmsProp(beta=0.999)
        elif optimizer == self.Optimizers.ADAM:
            self.adam()
        else:
            for l in range(L):
                vars(self)[f'W{l+1}'] = vars(self)[f'W{l+1}'] - self.learning_rate * vars(self)[f'dW{l+1}']
                vars(self)[f'b{l+1}']  = vars(self)[f'b{l+1}'] - self.learning_rate * vars(self)[f'db{l+1}']

    def fit(self, X:np.ndarray, y:np.ndarray, epochs:int=2000, optimizer:Optimizers=None, 
            plot_cost:bool=True, verbose:bool=False) -> None:
        
        '''
        Trains the Neural Network using input data.
        
        Parameters
        ----------
        X: np.ndarray
            Array with input data of shape (input size, number of examples).
        Y: np.ndarray
            True values.
        epochs: int
            Number of iterations of the optimization loop.
        optimizer: Optimizers
            The optimizer used. Default is None. If can be one of: 'momentum', 
            'rmsprop' or 'adam'. 
        plot_cost: bool
            Whether to plot the cost during training. Defaults to True.
        verbose: bool
            True to print the evolution of the training.
        '''

        assert isinstance(X, np.ndarray), "X must be a NumPy array"
        assert isinstance(y, np.ndarray), "y must be a NumPy array"
        assert X.shape[0] == y.shape[0], "X and y must have the same number of samples"
        assert epochs > 0, "Iterations must be greater than 0"

        X = X if round(np.mean(X)) == 0 and round(np.std(X)) == 1 else utils.scale(X)
        if X.shape[1] != self.layer_dimensions[0]:
            self.layer_dimensions[0] = X.shape[1]
            
        # Transpose X to get the correct shape
        X = X.T
        np.random.seed(1)
        #create empty array to store the costs
        self.costs = [] 
        # Get number of training examples
        m = X.shape[1]
        # Initialize parameters 
        self.initialize_parameters()
        # loop for stated number of epochs
        for i in range(0, epochs):
            # Forward propagate and get the predictions and caches
            predictions, caches = self.forward_propagation(X)
            #compute the cost function
            cost = self.compute_cost(predictions, y)
            # Calculate the gradient and update the parameters
            self.back_propagation(predictions, y, caches)

            self.update_parameters(optimizer=optimizer)

            # To obtain always a 100 items costs array
            if i % int(str(epochs)[0] + ('0'*(len(str(epochs))-3))) == 0:
                self.costs.append(cost)
                if (verbose or self.verbose):
                    print(f"Cost after iteration {i}: {np.squeeze(cost)}")
                    
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
        
        fig = px.line(y=np.squeeze(self.costs), title="Cost vs Iteration", template=template)
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
        predictions: np.ndarray
            Predicted target values of shape (m,).
        '''
        
        X = X if round(np.mean(X)) == 0 and round(np.std(X)) == 1 else utils.scale(X)
        X = X.T
        # Get predictions from forward propagation
        predictions, _ = self.forward_propagation(X)
        # Predictions Above 0.5 are True otherwise they are False
        predictions = (predictions > 0.5)
        # Squeeze the predictions into the correct shape and cast true/false values to 1/0
        predictions = np.squeeze(predictions.astype(int))
        
        return predictions
    
    def save_model(self, filename:str='last_ONN_model.pkl') -> None:

        '''
        Save the trained model to a file using pickle.

        Parameters
        ----------
        filename: str
            The name of the file to save the model to.
        '''

        model_data = {
            'learning_rate': self.learning_rate,
            'layer_dimensions': self.layer_dimensions
        }
        for v in dir(self):
            if 'W' == v[0] or 'b' == v[0]:
                model_data[v] = vars(self)[v]

        with open(filename, 'wb') as file:
            pickle.dump(model_data, file)

    @classmethod
    def load_model(cls, filename:str='last_ONN_model.pkl'):

        '''
        Load a trained model from a file using pickle.

        Parameters
        ----------
        filename: str
            The name of the file to load the model from.

        Returns
        -------
        loaded_model: NeuralNetwork
            An instance of the NeuralNetwork class with loaded parameters.
        '''

        with open(filename, 'rb') as file:
            model_data = pickle.load(file)

        # Create a new instance of the class and initialize it with the loaded parameters
        loaded_model = cls(layer_dimensions=model_data['layer_dimensions'], 
                           learning_rate=model_data['learning_rate'])
        for k,v in model_data.items():
            vars(loaded_model)[k] = v

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


def train_evaluate_model(data:pd.DataFrame, X_train:np.ndarray, y_train:np.ndarray, 
                         X_test:np.ndarray, y_test:np.ndarray, learning_rates:list, 
                         layer_dimensions:list, epochs:list) -> pd.DataFrame:
    
    '''
    Keyword arguments:
    X_train -- Training data
    y_train -- Traing labels
    X_train -- test data
    y_train -- test labels
    layer_dimensions -- list with the dimension of each iteration
    learning_rates --  list with the learning_rate of each directions
    Epochs -- list of epochs for each iteration

    returns a dataframe 
    '''

    if len(learning_rates) != len(layer_dimensions) or len(layer_dimensions) != len(epochs):
        raise ValueError('List containing the learnings rates, layer dimensions and epochs \
                         don\'t match in length!')

    dfs = []
    for i in range(len(learning_rates)):
        # create model instance with the given hyperparameters
        model = NeuralNetwork(learning_rate=learning_rates[i],layer_dimensions=layer_dimensions[i])
        # fit the model
        model.fit(X_train, y_train,epochs=epochs[i],verbose=False)
        
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        # Show metrics
        result = {
            'index': f'model_{i}',
            'learningRate': learning_rates[i],
            'layers': layer_dimensions[i],
            'epochs': epochs[i],
        }
        tests = {'train': [y_train, y_train_pred], 'test':[y_test, y_test_pred]}
        for k in tests:
            y_test, y_pred = tests[k]
            
            result[f'{k}Accuracy'] = utils.ClassificationMetrics.accuracy(y_test, y_pred)
            result[f'{k}Precision'] = utils.ClassificationMetrics.precision(y_test, y_pred)
            result[f'{k}Recall'] = utils.ClassificationMetrics.recall(y_test, y_pred)
            result[f'{k}F1-Score'] = utils.ClassificationMetrics.f1_score(y_test, y_pred)
            
            y_df = pd.DataFrame({'Open':data['open'].iloc[-len(y_test):], 
                                'Close':data['close'].iloc[-len(y_test):],
                                'Orig': y_test, 'Pred': y_pred})
            y_df['Range'] = y_df['Close'] - y_df['Open']
            success = y_df[y_df['Pred'] == y_df['Orig']]
            error = y_df[y_df['Pred'] != y_df['Orig']]
            
            wr = len(success)/len(y_df)
            rr = (success['Range'].abs().mean())/(error['Range'].abs().mean())
            result[f'{k}WinRate'] = wr
            result[f'{k}RiskReward'] = rr
            result[f'{k}Spectancy'] = (wr * success['Range'].abs().mean() - (1-wr) * error['Range'].abs().mean())

        dfs.append(pd.DataFrame([result]))

    return pd.concat(dfs)



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

    if not True:
            
        model = NeuralNetwork(layer_dimensions=[X_train_stand.shape[1], 16, 16, 1], 
                                    learning_rate=0.0001)
        model.fit(X_train_stand, y_train, epochs=10000, 
                optimizer=None, #NeuralNetwork.Optimizers.ADAM, 
                verbose=False)
        
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
        # print(model.getWeights(features))
    
    else:

        fl = X_train_stand.shape[1] # first layer dimension
        learning_rates=[0.000001, 0.000001, 0.000001, 0.000001]
        layer_dimensions=[[fl, 1, 1], [fl, 16, 16, 1], [fl, 16, 16, 1], [fl, 16, 16, 1]]
        epochs=[10000, 10000, 10000, 10000]
        
        results = train_evaluate_model(data=data, X_train=X_train_stand, y_train=y_train, 
                         X_test=X_test_stand, y_test=y_test, learning_rates=learning_rates, 
                         layer_dimensions=layer_dimensions, epochs=epochs)
        
        import seaborn as sns
        results.style.background_gradient(cmap =sns.cubehelix_palette(start=.5, rot=-.5, as_cmap=True))