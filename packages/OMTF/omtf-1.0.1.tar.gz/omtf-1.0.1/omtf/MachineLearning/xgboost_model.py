
import math
import numpy as np 
import pandas as pd
from collections import defaultdict

class XGBoost():
    
    '''
    XGBoost from Scratch
    '''
    
    class SquaredErrorObjective():
        
        def loss(self, y:np.ndarray, pred:np.ndarray) -> float: 
            return np.mean((y - pred)**2)
        
        def gradient(self, y:np.ndarray, pred:np.ndarray) -> np.ndarray: 
            return pred - y
        
        def hessian(self, y:np.ndarray) -> np.ndarray: 
            return np.ones(len(y))
    
    def __init__(self, subsample:float=1.0, learning_rate:float=0.3, base_score:float=0.5, 
                 min_child_weight:float=1.0, max_depth:int=5, reg_lambda:float=1.0, 
                 gamma:float=0.0, colsample_bymode:float=1.0, random_seed:int=None) -> None:
        
        self.subsample = subsample
        self.learning_rate = learning_rate
        self.base_prediction = base_score
        self.max_depth = max_depth
        self.rng = np.random.default_rng(seed=random_seed)
        self.min_child_weight = min_child_weight
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.colsample_bymode = colsample_bymode
        self.objective = self.SquaredErrorObjective()
                
    def fit(self, X:np.ndarray, y:np.ndarray, num_boost_round:int, 
            objective:SquaredErrorObjective=None, verbose:bool=False) -> None:
        
        self.X = X
        self.y = y
        
        if objective == None:
            objective = self.objective
        
        current_predictions = self.base_prediction * np.ones(shape=y.shape)
        self.boosters:list[TreeBooster] = []
        for i in range(num_boost_round):
            
            gradients = objective.gradient(y, current_predictions)
            hessians = objective.hessian(y)
            sample_idxs = None if self.subsample == 1.0 \
                else self.rng.choice(len(y), 
                                     size=math.floor(self.subsample*len(y)), 
                                     replace=False)
            booster = TreeBooster(X=X, g=gradients, h=hessians, 
                                min_child_weight=self.min_child_weight, max_depth=self.max_depth,
                                reg_lambda=self.reg_lambda, gamma=self.gamma, 
                                colsample_bymode=self.colsample_bymode, 
                                idxs=sample_idxs)
            current_predictions += self.learning_rate * booster.predict(X)
            self.boosters.append(booster)
            
            if verbose: 
                print(f'[{i}] train loss = {objective.loss(y, current_predictions)}')
            
    def predict(self, X:np.ndarray) -> np.ndarray:
        
        return (self.base_prediction + self.learning_rate 
                * np.sum([booster.predict(X) for booster in self.boosters], axis=0))
    
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
    

class TreeBooster():
 
    def __init__(self, X:np.ndarray, g:np.ndarray, h:np.ndarray, min_child_weight:float=1.0, 
                 max_depth:int=5, reg_lambda:float=1.0, gamma:float=0.0, 
                 colsample_bymode:float=1.0, idxs:np.ndarray=None) -> None:
        
        self.max_depth = max_depth
        
        assert self.max_depth >= 0, 'max_depth must be nonnegative'
        
        self.min_child_weight = min_child_weight
        self.reg_lambda = reg_lambda
        self.gamma = gamma
        self.colsample_bymode = colsample_bymode
        if isinstance(g, pd.Series): 
            g = g.values
        if isinstance(h, pd.Series): 
            h = h.values
        if idxs is None: 
            idxs = np.arange(len(g))
        if isinstance(X, pd.DataFrame):
            X = X.values
        self.X, self.g, self.h, self.idxs = X, g, h, idxs
        self.n, self.c = len(idxs), X.shape[1]
        self.value = -g[idxs].sum() / (h[idxs].sum() + self.reg_lambda) # Eq (5)
        self.best_score_so_far = 0.
        if self.max_depth > 0:
            self._maybe_insert_child_nodes()

    def _maybe_insert_child_nodes(self) -> None:
        
        for i in range(self.c): 
            self._find_better_split(i)
            
        if self.is_leaf: 
            return
        
        x = self.X[self.idxs,self.split_feature_idx]
        left_idx = np.nonzero(x <= self.threshold)[0]
        right_idx = np.nonzero(x > self.threshold)[0]
        self.left = TreeBooster(X=self.X, g=self.g, h=self.h, 
                            min_child_weight=self.min_child_weight, 
                            max_depth=self.max_depth -1,
                            reg_lambda=self.reg_lambda, gamma=self.gamma, 
                            colsample_bymode=self.colsample_bymode, 
                            idxs=self.idxs[left_idx])
        self.right = TreeBooster(X=self.X, g=self.g, h=self.h, 
                            min_child_weight=self.min_child_weight, 
                            max_depth=self.max_depth -1,
                            reg_lambda=self.reg_lambda, gamma=self.gamma, 
                            colsample_bymode=self.colsample_bymode, 
                            idxs=self.idxs[right_idx])

    @property
    def is_leaf(self) -> bool: 
        
        return self.best_score_so_far == 0.
    
    def _find_better_split(self, feature_idx:int) -> None:
        
        x = self.X[self.idxs, feature_idx]
        g, h = self.g[self.idxs], self.h[self.idxs]
        sort_idx = np.argsort(x)
        sort_g, sort_h, sort_x = g[sort_idx], h[sort_idx], x[sort_idx]
        sum_g, sum_h = g.sum(), h.sum()
        sum_g_right, sum_h_right = sum_g, sum_h
        sum_g_left, sum_h_left = 0., 0.

        for i in range(0, self.n - 1):
            
            g_i, h_i, x_i, x_i_next = sort_g[i], sort_h[i], sort_x[i], sort_x[i + 1]
            sum_g_left += g_i; sum_g_right -= g_i
            sum_h_left += h_i; sum_h_right -= h_i
            
            if sum_h_left < self.min_child_weight or x_i == x_i_next:
                continue
            if sum_h_right < self.min_child_weight: 
                break

            gain = 0.5 * ((sum_g_left**2 / (sum_h_left + self.reg_lambda))
                            + (sum_g_right**2 / (sum_h_right + self.reg_lambda))
                            - (sum_g**2 / (sum_h + self.reg_lambda))
                            ) - self.gamma/2 # Eq(7) in the xgboost paper
            
            if gain > self.best_score_so_far: 
                self.split_feature_idx = feature_idx
                self.best_score_so_far = gain
                self.threshold = (x_i + x_i_next) / 2
                
    def predict(self, X:np.ndarray) -> np.ndarray:
        
        return np.array([self._predict_row(row) for i, row in enumerate(X)])

    def _predict_row(self, row:np.ndarray) -> float:
        
        if self.is_leaf: 
            return self.value
        
        child = self.left if row[self.split_feature_idx] <= self.threshold \
                else self.right
            
        return child._predict_row(row)




if __name__ == '__main__':

    import yfinance as yf

    import MachineLearning.utils
    from MachineLearning.principal_component import PCA

    pca_apply = True

    data = yf.Ticker('TSLA').history(period='5y', interval='1d')
    data.columns = [c.lower() for c in data.columns]
    data['date'] = data.index
    data['prev_close'] = data['close'].shift(1)
    data['outlier'] = data['open']/data['open'].rolling(50).mean()
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
    
    data['target'] = data['close'].shift(-1) #np.where(data['open'] < data['close'], 1, 0)
    data.dropna(inplace=True)
    
    features = ['range_pu', 'open_to_close_pu', 'gap_pu', 'outlier_pu', 'day', 
                'month', 'year', 'week_day', 'is_quarter_end']

    X_train, X_test, y_train, y_test = MachineLearning.utils.train_test_split(data[features], data['target'], 
                                                            random_state=41, test_size=0.2)
    X_train_stand, X_test_stand = MachineLearning.utils.standardize_data(X_train, X_test)
        
    if pca_apply:
        pca = PCA(len(features))
        pca.fit(X_train_stand)
        X_train_stand = pca.transform(X_train_stand)
        X_test_stand = pca.transform(X_test_stand)

    learning_rate = 0.1
    max_depth = 5
    subsample = 0.8
    reg_lambda = 1.5
    gamma = 0.0
    min_child_weight = 25
    base_score = 0.0
    num_boost_round = 50
    
    
    model = XGBoost(subsample=0.8, learning_rate=0.1, base_score=0.0, 
                    min_child_weight=25, max_depth=5, reg_lambda=1.5, 
                    gamma=0.0, colsample_bymode=1.0, random_seed=42)
    model.fit(X=X_train_stand, y=y_train, num_boost_round=50)
    y_train_pred = model.predict(X_train_stand)
    y_test_pred = model.predict(X_test_stand)
    
    # Show metrics
    tests = {'train': [np.where(y_train > np.concatenate(([np.nan], y_train[:-1])), 1, 0), 
                       np.where(y_train_pred > np.concatenate(([np.nan], y_train_pred[:-1])), 1, 0)], 
            'test':[np.where(y_test > np.concatenate(([np.nan], y_test[:-1])), 1, 0), 
                    np.where(y_test_pred > np.concatenate(([np.nan], y_test_pred[:-1])), 1, 0)]}
    for k in tests:
        y_test, y_pred = tests[k]
        
        print(f'\nMETRICS FOR THE {k.upper()} ----------------')
        print(f"Accuracy: {MachineLearning.utils.ClassificationMetrics.accuracy(y_test, y_pred):.2%}")
        print(f"Precision: {MachineLearning.utils.ClassificationMetrics.precision(y_test, y_pred):.2%}")
        print(f"Recall: {MachineLearning.utils.ClassificationMetrics.recall(y_test, y_pred):.2%}")
        print(f"F1-Score: {MachineLearning.utils.ClassificationMetrics.f1_score(y_test, y_pred):.2%}")
        
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
    
    if False:
        from sklearn.datasets import fetch_california_housing
        from sklearn.model_selection import train_test_split
            
        X, y = fetch_california_housing(as_frame=True, return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, 
                                                            random_state=43)
        
        learning_rate = 0.1
        max_depth = 5
        subsample = 0.8
        reg_lambda = 1.5
        gamma = 0.0
        min_child_weight = 25
        base_score = 0.0
        tree_method = 'exact'
        num_boost_round = 50
        
        
        model = XGBoostModel(subsample=0.8, learning_rate=0.1, base_score=0.0, 
                                    min_child_weight=25, max_depth=5, reg_lambda=1.5, 
                                    gamma=0.0, colsample_bymode=1.0, random_seed=42)
        model.fit(X=X_train, y=y_train, num_boost_round=50)
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)