import sys
import os
# modify this path to match your environment
sys.path.append(os.path.join(os.getcwd(), 'MachineLearning'))

import numpy as np
import pandas as pd


class RegressionMetrics:

    @staticmethod
    def mean_squared_error(y_true:np.ndarray, y_pred:np.ndarray) -> float:

        '''
        Calculate the Mean Squared Error (MSE).
        A lower MSE indicates a better fit of the model to the data, as it 
        means the model's predictions are closer to the actual values.
        MSE is sensitive to outliers because the squared differences magnify 
        the impact of large errors.

        Parameters
        ----------
        y_true: np.ndarray
            The true target values.
        y_pred: np.ndarray
            The predicted target values.

        Returns
        -------
        mse: float
            The Mean Squared Error.
        '''

        assert len(y_true) == len(y_pred), 'Input arrays must have the same length.'
        mse = np.mean((y_true - y_pred) ** 2)

        return mse

    @staticmethod
    def root_mean_squared_error(y_true:np.ndarray, y_pred:np.ndarray) -> float:

        '''
        Calculate the Root Mean Squared Error (RMSE).
        Like MSE, a lower RMSE indicates a better fit of the model to the data.
        RMSE is also sensitive to outliers due to the square root operation.

        Parameters
        ----------
        y_true: np.ndarray
            The true target values.
        y_pred: np.ndarray
            The predicted target values.

        Returns
        -------
        rmse: float
            The Root Mean Squared Error.
        '''

        assert len(y_true) == len(y_pred), "Input arrays must have the same length."
        mse = RegressionMetrics.mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)

        return rmse

    @staticmethod
    def r_squared(y_true:np.ndarray, y_pred:np.ndarray) -> float:

        '''
        Calculate the R-squared (R^2) coefficient of determination.
        A higher R-squared value suggests that the model explains a 
        larger proportion of the variance in the target variable.
        However, R-squared does not provide information about the 
        goodness of individual predictions or whether the model is 
        overfitting or underfitting.

        Parameters
        ----------
        y_true: np.ndarray
            The true target values.
        y_pred: np.ndarray
            The predicted target values.

        Returns
        -------
        r2: float
            The R-squared (R^2) value.
        '''

        assert len(y_true) == len(y_pred), "Input arrays must have the same length."
        mean_y = np.mean(y_true)
        ss_total = np.sum((y_true - mean_y) ** 2)
        ss_residual = np.sum((y_true - y_pred) ** 2)
        r2 = 1 - (ss_residual / ss_total)

        return r2
    
    

class ClassificationMetrics:
    
    @staticmethod
    def accuracy(y_true:np.ndarray, y_pred:np.ndarray) -> float:
        
        '''
        Computes the accuracy of a classification model.
        A higher accuracy value indicates a better classification model.
        However, accuracy alone may not provide a complete picture, especially 
        in imbalanced datasets.

        Parameters
        ----------
        y_true: np.ndarray
            The true target values.
        y_pred: np.ndarray
            The predicted target values.

        Returns
        -------
        return: float
            The accuracy of the model, expressed as a percentage.
        '''
        
        y_true = y_true.flatten()
        
        return (np.sum(y_true == y_pred) / len(y_true))
    
    @staticmethod
    def balanced_accuracy(y_true:np.ndarray, y_pred:np.ndarray) -> float:
        
        '''
        Calculate the balanced accuracy for a multi-class classification problem.

        Parameters
        ----------
        y_true: np.ndarray
            The true target values.
        y_pred: np.ndarray
            The predicted target values.

        Returns
        -------
        balanced_acc: float
            The balanced accuracyof the model
            
        '''
        
        y_pred = np.array(y_pred)
        y_true = y_true.flatten()
        # Get the number of classes
        n_classes = len(np.unique(y_true))

        # Initialize an array to store the sensitivity and specificity for each class
        sen = []
        spec = []
        # Loop over each class
        for i in range(n_classes):
            # Create a mask for the true and predicted values for class i
            mask_true = y_true == i
            mask_pred = y_pred == i

            # Calculate the true positive, true negative, false positive, and false negative values
            TP = np.sum(mask_true & mask_pred)
            TN = np.sum((mask_true != True) & (mask_pred != True))
            FP = np.sum((mask_true != True) & mask_pred)
            FN = np.sum(mask_true & (mask_pred != True))

            # Calculate the sensitivity (true positive rate) and specificity (true negative rate)
            sensitivity = TP / (TP + FN)
            specificity = TN / (TN + FP)

            # Store the sensitivity and specificity for class i
            sen.append(sensitivity)
            spec.append(specificity)
            
        # Calculate the balanced accuracy as the average of the sensitivity and specificity for each class
        return (np.mean(sen) + np.mean(spec)) / n_classes

    @staticmethod
    def precision(y_true:np.ndarray, y_pred:np.ndarray) -> float:
        
        '''
        Computes the precision of a classification model.
        Higher precision means the model makes fewer false positive predictions.

        Parameters
        ----------
        y_true: np.ndarray
            The true target values.
        y_pred: np.ndarray
            The predicted target values.

        Returns
        -------
        return: float
            The precision of the model, which measures the proportion of true positive predictions
            out of all positive predictions made by the model.
        '''
        
        true_positives = np.sum((y_true == 1) & (y_pred == 1))
        false_positives = np.sum((y_true == 0) & (y_pred == 1))
        
        if true_positives + false_positives == 0:
            return 0
        
        return true_positives / (true_positives + false_positives)

    @staticmethod
    def recall(y_true:np.ndarray, y_pred:np.ndarray) -> float:
        
        '''
        Computes the recall (sensitivity) of a classification model.
        Higher recall means the model captures more of the actual positive instances.

        Parameters
        ----------
        y_true: np.ndarray
            The true target values.
        y_pred: np.ndarray
            The predicted target values.

        Returns
        -------
        return: float
            The recall of the model, which measures the proportion of true positive predictions
            out of all actual positive instances in the dataset.
        '''
        
        true_positives = np.sum((y_true == 1) & (y_pred == 1))
        false_negatives = np.sum((y_true == 1) & (y_pred == 0))
        
        if true_positives + false_negatives == 0:
            return 0
        
        return true_positives / (true_positives + false_negatives)

    @staticmethod
    def f1_score(y_true:np.ndarray, y_pred:np.ndarray) -> float:
        
        '''
        Computes the F1-score of a classification model.
        A higher F1-Score indicates a model that achieves a balance between 
        precision and recall.

        Parameters
        ----------
        y_true: np.ndarray
            The true target values.
        y_pred: np.ndarray
            The predicted target values.

        Returns
        -------
        return: float
            The F1-score of the model, which is the harmonic mean of precision and recall.
        '''
        
        precision_value = ClassificationMetrics.precision(y_true, y_pred)
        recall_value = ClassificationMetrics.recall(y_true, y_pred)
        
        if precision_value + recall_value == 0:
            return 0
        
        return 2 * (precision_value * recall_value) / (precision_value + recall_value)



def scale(X:np.ndarray) -> np.ndarray:

    '''
    Standardizes the data in the array X.

    Parameters
    ----------
    X: np.ndarray
        Input data of shape (m, n_features).

    Returns
    -------
    return: np.ndarray
        The standardized features array.
    '''
    
    if round(np.mean(X)) == 0 and round(np.std(X)) == 1:
        return X
    
    return (X - np.mean(X, axis=0)) / np.std(X, axis=0)

def standardize_data(X_train:np.ndarray, X_test:np.ndarray) -> tuple[np.ndarray, np.ndarray]:

    '''
    Standardizes the input data using mean and standard deviation.

    Parameters
    ----------
    X_train: np.ndarray)
        Training data.
    X_test: np.ndarray
        Testing data.

    Returns
    -------
    return: tuple[np.ndarray]
        Tuple of standardized training and testing data.
    '''
    
    return scale(X_train), scale(X_test)

def train_test_split(X:np.ndarray, y:np.ndarray, random_state:int=41, test_size:float=0.2,
                     shuffle:bool=False
                     ) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
    '''
    Splits the data into training and testing sets.

    Parameters
    ----------
    X: np.ndarray
        Features array of shape (m_samples, n_features).
    y: np.ndarray
        Target array of shape (n_samples,).
    random_state: int
        Seed for the random number generator. Default is 42.
    test_size: float
        Proportion of samples to include in the test set. Default is 0.2.

    Returns
    -------
    return: tuple[numpy.ndarray]
        A tuple containing X_train, X_test, y_train, y_test.
    '''

    # Get number of samples
    n_samples = X.shape[0]

    # Determine the size of the test set
    # test_size = int(n_samples * test_size)
    train_size = int(n_samples * (1 - test_size))

    if shuffle:
        # Set the seed for the random number generator
        np.random.seed(random_state)
        # Shuffle the indices
        shuffled_indices = np.random.permutation(np.arange(n_samples))

        # Split the indices into test and train
        train_indices = shuffled_indices[:train_size]
        test_indices = shuffled_indices[train_size:]
    else:
        # Split the indices into test and train
        train_indices = list(np.arange(n_samples))[:train_size]
        test_indices = list(np.arange(n_samples))[train_size:]

    X = X.values if isinstance(X, pd.DataFrame) or isinstance(X, pd.Series) else X
    y = y.values if isinstance(y, pd.DataFrame) or isinstance(y, pd.Series) else y
    
    # Split the features and target arrays into test and train
    X_train, X_test = X[train_indices], X[test_indices]
    y_train, y_test = y[train_indices], y[test_indices]

    return X_train, X_test, y_train, y_test

def euclidean_distance(x1:np.ndarray, x2:np.ndarray) -> float:
    
    '''
    Calculate the Euclidean distance between two data points.

    Parameters
    -----------
    x1: np.ndarray
        First array.
    x2: np.ndarray
        Second array.

    Returns
    --------
    distance: float
        The Euclidean distance between x1 and x2.
    '''
    
    return np.linalg.norm(x1 - x2)

def sigmoid(z:(float | np.ndarray)) -> tuple[(float | np.ndarray), (float | np.ndarray)]:
    
    '''
    Compute the sigmoid function for a given input.

    The sigmoid function is a mathematical function used in logistic regression and neural networks
    to map any real-valued number to a value between 0 and 1.

    The Sigmoid function is a common activation function used in Neural 
    Networks, particularly for binary classification problems. It is represented 
    by the following formula:

        f(Z)=1/(1+e^(−Z))
    
    where  Z is the input to the function. The Sigmoid function maps any 
    real-valued number to a value between 0 and 1, which can be interpreted 
    as a probability. In binary classification problems, we often use the 
    Sigmoid function as the activation function for the output layer of the 
    Neural Network, since it can be used to compute the probability of the 
    input belonging to the positive class.

    Parameters
    ----------
    z: float or np.ndarray
        The input value(s) for which to compute the sigmoid.

    Returns
    -------
    A: float
        Sigmoid of the input value(s).
    cache: np.ndarray
        The input value(s).

    Example
    -------
    >>> sigmoid(0)
    0.5, 0
    '''
    
    # Compute the sigmoid function using the formula: 1 / (1 + e^(-z)).
    A = 1 / (1 + np.exp(-z))
    cache = z
    
    # Return the computed sigmoid value.
    return A, cache

def sigmoid_backward(dA:np.ndarray, cache:np.ndarray) -> np.ndarray:

    '''
    Implement the backward propagation for a single sigmoid unit 
    (derivative of the sigmoid).

    Arguments
    ---------
    dA: np.ndarray
        Post-activation gradient.
    cache: np.ndarray
        'Z' stored during forward pass.

    Returns
    -------
    dZ: np.ndarray
        Gradient of the cost with respect to Z.
    '''

    Z = cache
    s = 1/(1+np.exp(-Z))
    dZ = dA * s * (1-s)

    return dZ

def entropy(y:np.ndarray, vectorized:bool=True) -> float:
    
    '''
    Computes the entropy of the given label values.

    Parameters
    ----------
    y: np.ndarray
        Input label values.
    vectorized: bool
        True to apply numpy vectorization.
    
    Returns
    -------
    entropy: float
        Entropy of the given label values.
    '''

    if vectorized and (isinstance(y, pd.Series) or isinstance(y, np.ndarray)):

        if isinstance(y, pd.Series):
            a = y.value_counts()
        elif isinstance(y, np.ndarray):
            a = np.unique(y, return_counts=True)[1]
        else:
            raise('Object must be a a valid format.')

        a = np.where(a == 0, 1e-9, a)
        entropy = np.sum(-a * np.log2(a))
    
    else:
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

def relu(Z:np.ndarray) -> tuple[float, np.ndarray]:

    '''
    Implement the ReLU function.

    The Rectified Linear Unit (ReLU) is a simple, yet highly effective 
    activation function commonly used in Neural Networks. It is defined as:

        f(Z)=max(0,Z)
 
    where  Z is the input to the function. ReLU sets all negative values of 
    Z to zero, and leaves the positive values unchanged. This non-linear 
    activation function helps Neural Networks model complex non-linear 
    relationships between inputs and outputs, allowing them to learn more 
    complex representations of the data.
    In addition to its effectiveness in Neural Networks, ReLU is also 
    computationally efficient and easy to implement.

    Arguments
    ---------
    Z: np.ndarray
        Output of the linear layer.

    Returns
    -------
    A: float
        Post-activation parameter
    cache: np.ndarray
        Linear layer used for backpropagation (Z).
    '''

    A = np.maximum(0,Z)
    cache = Z 

    return A, cache

def relu_backward(dA:np.ndarray, cache:np.ndarray) -> np.ndarray:

    '''
    Implement the backward propagation for a single ReLU unit (derivative 
    of the Relu function).

    Arguments
    ---------
    dA: np.ndarray
        Post-activation gradient.
    cache: np.ndarray 
        'Z' stored for backpropagation.

    Returns
    -------
    dZ: np.ndarray
        Gradient of the cost with respect to Z.
    '''

    Z = cache
    dZ = np.array(dA, copy=True) 
    # When z <= 0, dz is equal to 0 as well. 
    dZ[Z <= 0] = 0
    
    return dZ

def softmax(x:np.ndarray) -> np.ndarray:
    
    '''
    Computes the softmax activation function for a given input array.

    Parameters
    ----------
    x: np.ndarray
        Input array.

    Returns
    -------
    return: np.ndarray
        Array of the same shape as 'x', containing the softmax activation values.
    '''
    
    # shift the input to prevent overflow when computing the exponentials
    x = x - np.max(x)
    # compute the exponentials of the shifted input
    p = np.exp(x)
    # normalize the exponentials by dividing by their sum
    
    return p / np.sum(p)

def gini_index(groups:np.ndarray, classes:np.ndarray) -> float:
    
    '''
    Computes the diference between the current distribution and the equality.

    Parameters
    ----------
    groups: np.ndarray
        Input array.
    classes: np.ndarray
        Classes in the input array.

    Returns
    -------
    gini: float
        Value for the Gini Index.
    '''

    # count all samples at split point
    n_instances = float(sum([len(group) for group in groups]))

    # sum weighted Gini index for each group
    gini = 0.0
    for group in groups:

        size = float(len(group))
        # avoid divide by zero
        if size == 0:
            continue

        score = 0.0
        # score the group based on the score for each class
        for class_val in classes:
            p = [row[-1] for row in group].count(class_val) / size
            score += p * p

        # weight the group score by its relative size
        gini += (1.0 - score) * (size / n_instances)

    return gini

def gini_impurity(y:np.ndarray) -> float:

    '''
    Calculates the Gini Impurity. 
    
    Parameters
    ----------
    y: np.ndarray
        Variable with which to calculate Gini Impurity.

    Returns
    -------
    return: float
        Value for the impurity.
    '''

    if isinstance(y, pd.Series):
        p = y.value_counts()
    elif isinstance(y, np.ndarray):
        p = np.unique(y, return_counts=True)[1]
    else:
        raise('Object must be a valid format.')

    return 1-np.sum(p/y.shape[0]**2)

def variance(y:np.ndarray) -> float:

    '''
    Function to help calculate the variance avoiding nan.

    Parameters
    ----------
    y: np.ndarray
        Variable to calculate variance to.
    
    Returns
    -------
    return: float
        Variance of an array.
    '''

    if(len(y) <= 1):
        return 0
    else:
        return y.var()

def information_gain(a:np.ndarray, indexes:np.ndarray, func=entropy) -> float:
    
    '''
    It returns the Information Gain of a variable given a loss function.

    Parameters
    ----------
    a: np.ndarray 
        Target variable.
    b: np.ndarray 
        Contains the indexes of the values to get from a.
    func: function 
        Function used to calculate Information Gain in case of classification.

    Returns
    -------
    ig: float
        Information gain value.
    '''
    
    idx_size = indexes.shape[0]
    del_size = a.shape[0] - idx_size
    
    if(idx_size == 0 or del_size ==0): 
        ig = 0
    
    else:
        if a.dtypes != 'O':
            ig = variance(a) - (idx_size/(idx_size+del_size)* variance(a[indexes])) - \
                (del_size/(idx_size+del_size)*variance(np.delete(a, indexes)))
        else:
            ig = func(a) - idx_size/(idx_size+del_size)*func(a[indexes]) - \
                del_size/(idx_size+del_size)*func(np.delete(a, indexes))
    
    return ig

if __name__ == '__main__':

    import yfinance as yf

    data = yf.Ticker('TSLA').history(period='5y', interval='1d')
    data['target'] = np.where(data['Close'] > data['Open'], 1, 0)

    X_train, X_test, y_train, y_test = train_test_split(data[['Open', 'High', 'Low', 'Close']].values, 
                                                              data['target'].values, random_state=41, test_size=0.2)

