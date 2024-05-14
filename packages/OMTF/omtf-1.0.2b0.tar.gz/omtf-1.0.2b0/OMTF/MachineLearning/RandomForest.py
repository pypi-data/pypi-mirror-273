
import math
import numpy as np

from gradientboosting import DecisionTree, RegressionTree

class RandomForest:

    """    Random forest common class.    """

    def __init__(self, trees:list[(DecisionTree | RegressionTree)], n_trees:int,
                 prediction_aggrigation_calculation, max_feature:int=None) -> None:

        """
        :param trees: List - list of tree objects. classification tree/regression trees.
        :param n_trees: int - How may estimators/tree should be used for random forest building.
        :param prediction_aggrigation_calculation: Function - Aggication function to find the prediction.
        :param max_feature: Int - How many features can be used for a tree from the whole features.
        """

        self.n_estimators = n_trees
        self.max_features = max_feature
        self.tree_feature_indexes:list = []
        self.prediction_aggrigation_calculation = prediction_aggrigation_calculation 
        # Initialize the trees.
        self.trees:list[(DecisionTree | RegressionTree)] = trees

    def bootstrap_samples(self, X:np.ndarray, y:np.ndarray, n_subsets:int, 
                           replacement:bool=True) -> list[dict]:

        """
        Creata a random subset of dataset with/without replacement.

        :param X: Depentand variables.
        :param y: Indepentant variable.
        :param n_subsets: int of subset we need.
        :param replacement: bool - Can we use the data sample again or not.
        """

        subset = []
        # use 100% of data when replacement is true , use 50% otherwise.
        sample_size = (X.shape[0] if replacement else (X.shape[0] // 2))

        # First concadinate the X and y datasets in order to make a choice.
        Xy = np.concatenate((X, y if len(y.shape) > 1 else np.reshape(y, (-1, 1))), axis=1)
        np.random.shuffle(Xy)
    
        # Select randome subset of data with replacement.
        for i in range(n_subsets):
            index = np.random.choice(range(sample_size), size=np.shape(range(sample_size)), 
                                     replace=replacement)
            X = Xy[index][:, :-1]
            y = Xy[index][: , -1]
            subset.append({"X" : X, "y": y})

        return subset

    def fit(self, X:np.ndarray, y:np.ndarray) -> None:

        """
        Build the model.
        :param X: Depentand variables.
        :param y: Indepentant variable.
        """

        self.X = X
        self.y = y

        # if the max_features is not given then select it as square root of no on feature availabe.
        n_features = X.shape[1]
        if self.max_features == None:
            self.max_features = n_features # int(math.sqrt(n_features))

        # Split the dataset into number of subsets equal to n_estimators.
        subsets = self.bootstrap_samples(X, y, self.n_estimators)

        for i, subset in enumerate(subsets):
            X_subset , y_subset = subset["X"], subset["y"]
            # select a random sucset of features for each tree. This is called feature bagging.
            idx = np.random.choice(range(n_features), size=self.max_features, replace=True)
            # track this for prediction.
            self.tree_feature_indexes.append(idx)
            # Get the X with the selected features only.
            X_subset = X_subset[:, idx]

            # change the y_subet to i dimentional array.
            y_subset = np.expand_dims(y_subset, axis =1)
            # build the model with selected features and selected random subset from dataset.
            self.trees[i].fit(X_subset, y_subset)

    def predict(self, test_X:np.ndarray) -> np.ndarray:

        """
        Predict the new samples.

        :param test_X: Depentant variables for prediction.
        """

        # predict each sample one by one.
        y_preds = np.empty((test_X.shape[0], self.n_estimators))
        # find the prediction from each tree for eeach samples
        for i, tree in enumerate(self.trees):
            features_index = self.tree_feature_indexes[i]
            X_selected_features = test_X[:, features_index]
            if isinstance(tree, DecisionTree):
                y_preds[:, i] = tree.predict(X_selected_features).reshape((-1,))
            else:
                y_preds[:, i] = tree.predict(X_selected_features)
        # find the arrgrecated output.
        y_pred = self.prediction_aggrigation_calculation(y_preds)

        return y_pred
    
    def plotPrediction(self, X:np.ndarray=None, y:np.ndarray=None) -> None:

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


class RandomForestClassifier(RandomForest):

    """Rnadom forest for classification task."""

    def __init__(self, max_depth:int, n_trees:int=100, min_samples:int=2, 
                 min_impurity:float=1e-7, max_feature:int=None) -> None:

        """
        :param max_depth: Int - Max depth of each tree.
        :param n_trees: Int - Number of trees/estimetors.
        :param min_samples: Int - minimum samples for a node to have before going for split.
        :param min_impurity: Int - Min inpurity a node can have.
        """
        
        # Initializing the trees.
        self.trees:list[DecisionTree] = []
        for _ in range(n_trees):
            self.trees.append(DecisionTree(min_samples=min_samples,
                                        min_impurity=min_impurity, 
                                        max_depth=max_depth))

        super().__init__(trees=self.trees, n_trees=n_trees, max_feature=max_feature,
                         prediction_aggrigation_calculation=self._maximum_vote_calculation)
    
    def _maximum_vote_calculation(self, y_preds:np.ndarray) -> np.ndarray:

        """
        Find which prediction class has higest frequency in all tree prediction for each sampple.

        :param y_preds: Prediction value from number of estimators trees.
        """

        # create a empty array to store the prediction.
        y_pred = np.empty((y_preds.shape[0], 1))
        # iterate over all the data samples.
        for i, sample_predictions in enumerate(y_preds):
            y_pred[i] = np.bincount(sample_predictions.astype('int')).argmax()

        return y_pred



class RandomForestRegression(RandomForest):

    """Rnadom forest for classification task."""

    def __init__(self, max_depth:int, n_trees:int=100, min_samples:int=2, 
                 min_impurity:float=1e-7, max_feature:int=None) -> None:

        """
        :param max_depth: Int - Max depth of each tree.
        :param n_trees: Int - Number of trees/estimetors.
        :param min_samples: Int - minimum samples for a node to have before going for split.
        :param min_impurity: Int - Min inpurity a node can have.
        """
        
        # Initializing the trees.
        self.trees:list[RegressionTree] = []
        for _ in range(n_trees):
            self.trees.append(RegressionTree(min_samples=min_samples, 
                                             min_impurity=min_impurity, 
                                             max_depth=max_depth))

        super().__init__(trees=self.trees, n_trees=n_trees, max_feature=max_feature,
                         prediction_aggrigation_calculation=self._mean_calculation)
    
    def _mean_calculation(self, y_preds:np.ndarray) -> np.ndarray:

        """
        Find mean prediction of all tree prediction for each sampple.

        :param y_preds: Prediction value from number of estimators trees.
        """

        # create a empty array to store the prediction.
        y_pred = np.empty((y_preds.shape[0], 1))
        # iterate over all the data samples.
        for i, sample_predictions in enumerate(y_preds):
            y_pred[i] = np.mean(sample_predictions)

        return y_pred
    


    
if __name__ == '__main__':
    
    import pandas as pd
    import yfinance as yf
    
    import MachineLearning.utils
    from MachineLearning.principal_component import PCA

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

    X_train, X_test, y_train, y_test = MachineLearning.utils.train_test_split(data[features], data['target'], 
                                                              random_state=41, test_size=0.2)
    X_train_stand, X_test_stand = MachineLearning.utils.standardize_data(X_train, X_test)

    model = RandomForestRegression(n_trees=10, max_depth=10, min_samples=2)
    model.fit(X_train_stand, y_train)
    
    y_train_pred = model.predict(X_train_stand)
    y_test_pred = model.predict(X_test_stand)
    
    # Show metrics
    tests = {'train': [y_train, y_train_pred], 'test':[y_test, y_test_pred]}
    for k in tests:
        y_test, y_pred = tests[k]
        
        print(f'\nMETRICS FOR THE {k.upper()} ----------------')
        accuracy = MachineLearning.utils.ClassificationMetrics.accuracy(y_test, y_pred)
        precision = MachineLearning.utils.ClassificationMetrics.precision(y_test, y_pred)
        recall = MachineLearning.utils.ClassificationMetrics.recall(y_test, y_pred)
        f1_score = MachineLearning.utils.ClassificationMetrics.f1_score(y_test, y_pred)

        print(f"Accuracy: {accuracy:.2%}")
        print(f"Precision: {precision:.2%}")
        print(f"Recall: {recall:.2%}")
        print(f"F1-Score: {f1_score:.2%}")
        
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