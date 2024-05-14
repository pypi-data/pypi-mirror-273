
import math
import numpy as np
import pandas as pd

import utils
from linear_regression import LinearRegression
from logistic_regression import LogisticRegression
from kmeans_clustering import Kmeans
from decision_trees import DecisionTreeClassifier
from random_forest import RandomForest
from k_nearest_neighbors import KNN
from principal_component import PCA
from support_vector import SupportVectorMachine
from naive_bayes import NaiveBayes
from neural_networks import NeuralNetwork
from long_short_term_memory import LSTM

import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def getData(ticker:str) -> pd.DataFrame:
    
    data = yf.Ticker(ticker).history(period='5y', interval='1d')
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
        
    data['regression'] = data['close']
    data['classification'] = np.where(data['open'] < data['close'], 1, 0)
    data.dropna(inplace=True)

    return data, ['range_pu', 'open_to_close_pu', 'gap_pu', 'outlier_pu', 'day', 
                  'month', 'week_day', 'is_quarter_end']

def classificationPrepare(data:pd.DataFrame, apply_pca:bool=False, features:list=[]
                          ) -> (dict):

    X_train, X_test, y_train, y_test = utils.train_test_split(data[features], data['classification'], 
                                                                random_state=41, test_size=0.5)

    if apply_pca:
        pca = PCA(len(features)/2)
        pca.fit(X_train)
        X_train = pca.transform(X_train)
        X_test = pca.transform(X_test)
        pca.plotComponents(X_train)
        pca.cumulative_variance_ratio
        
        features = [f'PC{i}' for i in range(X_train.shape[-1])]
        
    return {'data':data, 'X_train':X_train, 'X_test':X_test, 'y_train':y_train, 
            'y_test':y_test, 'features':features}

def regressionPrepare(data:pd.DataFrame, apply_pca:bool=False, features:list=[]
                          ) -> (dict):

    X_train, X_test, y_train, y_test = utils.train_test_split(data[features], data['regression'], 
                                                                random_state=41, test_size=0.5)

    if apply_pca:
        pca = PCA(len(features)/2)
        pca.fit(X_train)
        X_train = pca.transform(X_train)
        X_test = pca.transform(X_test)
        pca.plotComponents(X_train)
        pca.cumulative_variance_ratio
        
        features = [f'PC{i}' for i in range(X_train.shape[-1])]
        
    return {'data':data, 'X_train':X_train, 'X_test':X_test, 'y_train':y_train, 
            'y_test':y_test, 'features':features}

def linear_model(X_stand:np.ndarray, y_train:np.ndarray, learning_rate:float=0.01, 
                 iterations:int=10000, plot_cost:bool=False, verbose:bool=False
                 ) -> LinearRegression:
    
    model = LinearRegression(learning_rate=learning_rate)
    model.fit(X_stand, y_train, iterations, plot_cost=plot_cost, verbose=verbose)
    
    return model

def logistic_model(X_stand:np.ndarray, y_train:np.ndarray, learning_rate:float=0.01, 
                 convergence_tol:float=0.00000000001, iterations:int=1000000, 
                 plot_cost:bool=False, verbose:bool=False) -> LogisticRegression:
    
    model = LogisticRegression(learning_rate=learning_rate, convergence_tol=convergence_tol)
    model.fit(X_stand, y_train, iterations=iterations, plot_cost=plot_cost, verbose=verbose)
    
    return model

def decision_tree_model(X_stand:np.ndarray, y_train:np.ndarray, min_samples:int=2, 
                        max_depth:int=10) -> DecisionTreeClassifier:
    
    model = DecisionTreeClassifier(min_samples=min_samples, max_depth=max_depth)
    model.fit(X_stand, y_train)
    
    return model

def k_nearest_model(X_train:np.ndarray, y_train:np.ndarray, n_neighbors:int=7) -> KNN:
    
    model = KNN(n_neighbors)
    model.fit(X_train, y_train)
    
    return model

def naive_bayes(X_train:np.ndarray, y_train:np.ndarray) -> NaiveBayes:
    
    model = NaiveBayes()
    model.fit(X_train, y_train)
    
    return model

def neural_networks(X_train:np.ndarray, y_train:np.ndarray, 
                    layer_dimensions:list=[25, 16, 16, 1], 
                    learning_rate:float=0.0001, epochs:int=10000,
                    optimizer:NeuralNetwork.Optimizers=None,
                    plot_cost:bool=False, verbose:bool=False) -> NeuralNetwork:
    
    layer_dimensions = [X_train.shape[1]] + layer_dimensions
    model = NeuralNetwork(layer_dimensions=layer_dimensions, 
                            learning_rate=learning_rate)
    model.fit(X_train, y_train, epochs=epochs, 
                optimizer=optimizer, #NeuralNetwork.Optimizers.ADAM, 
                plot_cost=plot_cost, verbose=verbose)
    
    return model

def random_forest(X_train:np.ndarray, y_train:np.ndarray, n_trees:int=10, 
                  max_depth:int=10, min_samples:int=2) -> RandomForest:
    
    model = RandomForest(n_trees=n_trees, max_depth=max_depth, 
                         min_samples=min_samples)
    model.fit(X_train, y_train)
    
    return model

def support_vector(X_train:np.ndarray, y_train:np.ndarray, 
                   iterations:int=1000, learning_rate:float=0.0001, 
                   lambdaa:float=0.01) -> SupportVectorMachine:
    
    model = SupportVectorMachine(iterations=iterations, learning_rate=learning_rate, 
                                 lambdaa=lambdaa)
    model.fit(X_train, y_train)
    
    return model

    
def plotPrediction(y_pred:np.ndarray=None, y_real:np.ndarray=None) -> go.Figure:
    
    '''
    Plotly chart containing the real data and the prediction.

    Parameters
    ----------
    y_pred: np.ndarray
        Data predicted of shape (m, ).
    y_real: np.ndarray
        Real data of shape (m, ).

    Plots
    -----
    Plotly chart containing the real data and the prediction.
    '''
    
    fig = go.Figure([
        go.Scatter(
            name='Data',
            y=y_real,
            mode='markers',
            marker=dict(color='red', size=2),
            showlegend=True
        ),
        go.Scatter(
            name='Prediction',
            y=y_pred,
            mode='lines',
            marker=dict(color='#444'),
            line=dict(width=1),
            showlegend=True
        )
    ])
    fig.update_layout(
        template='gridon',
        xaxis_title='X',
        yaxis_title='Y',
        title='Prediction vs. target',
        hovermode='x'
    )
    
    return fig


def tickerModels(ticker:str, use_pca:bool=False, complete:bool=False):

    # args = [a for a in args]
    # ticker:str = args[0] 
    # use_pca:bool = args[1]

    data, features = getData(ticker)

    # Prepare data
    f_data = {
        'classification': classificationPrepare(data=data, apply_pca=use_pca, features=features),
        'regression': regressionPrepare(data=data, apply_pca=use_pca, features=features)
    } 
    
    # Prepare models
    if complete:
        models = {
            'regression': {
                'linear': linear_model(f_data['regression']['X_train'], f_data['regression']['y_train'], 
                                    learning_rate=0.01, iterations=10000),
                'decision_tree': decision_tree_model(f_data['regression']['X_train'], f_data['regression']['y_train'], 
                                                    min_samples=2, max_depth=10),
            },
            'classification': {
                'logistic': logistic_model(f_data['classification']['X_train'], f_data['classification']['y_train'], 
                                        learning_rate=0.001, convergence_tol=1e-11, iterations=1000000),
                'knn': k_nearest_model(f_data['classification']['X_train'], f_data['classification']['y_train'], 
                                    n_neighbors=9),
                'naive_bayes': naive_bayes(f_data['classification']['X_train'], f_data['classification']['y_train']),
                'neural_network': neural_networks(f_data['classification']['X_train'], f_data['classification']['y_train'], 
                                                    layer_dimensions=[16, 16, 1], learning_rate=0.0001, epochs=10000, 
                                                    optimizer=None, verbose=False),
                'random_forest': random_forest(f_data['classification']['X_train'], f_data['classification']['y_train'], 
                                            n_trees=5, max_depth=3, min_samples=2),
                'svm': support_vector(f_data['classification']['X_train'], f_data['classification']['y_train'], 
                                    iterations=1000, learning_rate=0.0001, lambdaa=0.1)
            }
        }
    else:
        models = {
            'classification': {
                'svm1': support_vector(f_data['classification']['X_train'], f_data['classification']['y_train'], 
                                    iterations=1000, learning_rate=0.0001, lambdaa=0.001),
                'svm2': support_vector(f_data['classification']['X_train'], f_data['classification']['y_train'], 
                                    iterations=1000, learning_rate=0.0001, lambdaa=0.01),
                'svm3': support_vector(f_data['classification']['X_train'], f_data['classification']['y_train'], 
                                    iterations=1000, learning_rate=0.0001, lambdaa=0.1),
            }
        }

    message = ''
    model_results = {}
    ticker_results = {}
    figs = []
    predictions = {}
    # Iterate for each model
    for model_type in models:
        data, X_train, X_test, y_train, y_test, features = (i for i in f_data[model_type].values())
        for name, model in models[model_type].items():
            
            message += f'\nMETRICS FOR {name} ###############################################################'

            # Generate predictions
            tests = {'train': [y_train, model.predict(X_train)], 
                    'test':[y_test, model.predict(X_test)]}
            
            # Show metrics
            for k in tests:
                y_test, y_pred = tests[k]
                
                message += f'\nMETRICS FOR THE {k.upper()} ----------------'
                model.getMetrics(y_test, y_pred, show=True)
                
                y_df = pd.DataFrame({'Open':data['open'].iloc[-len(y_test):], 
                                    'Close':data['close'].iloc[-len(y_test):],
                                    'Orig': y_test, 'Pred': y_pred})
                y_df['Ticker'] = ticker
                y_df['Range'] = y_df['Close'] - y_df['Open']
                if model_type == 'regression':
                    y_df['Orig_side'] = np.where(y_df['Orig'] > y_df['Orig'].shift(1), 1, 
                                        np.where(y_df['Orig'] < y_df['Orig'].shift(1), -1, 0))
                    y_df['Pred_side'] = np.where(y_df['Pred'] > y_df['Pred'].shift(1), 1, 
                                        np.where(y_df['Pred'] < y_df['Pred'].shift(1), -1, 0))
                    success = y_df[y_df['Pred_side'] == y_df['Orig_side']]
                    error = y_df[y_df['Pred_side'] != y_df['Orig_side']]
                else:
                    y_df['Orig_side'] = y_df['Orig']
                    y_df['Pred_side'] = y_df['Pred']
                    success = y_df[y_df['Pred'] == y_df['Orig']]
                    error = y_df[y_df['Pred'] != y_df['Orig']]
                    
                if k == 'test':
                    predictions[name] = y_df.copy()
                
                wr = len(success)/len(y_df)
                rr = (success['Range'].abs().mean())/(error['Range'].abs().mean())
                temp = {
                    'winrate': wr,
                    'rr': rr,
                    'expectancy': wr * success['Range'].abs().mean() - (1-wr) * error['Range'].abs().mean()
                }
                model_results[(name, ticker, k)] = temp
                ticker_results[(ticker, name, k)] = temp
                
                message += f'Side Success: {wr:.2%}'
                message += f'Risk Reward: {rr:.2} R'
                message += f"Expectancy: {(wr * success['Range'].abs().mean() - (1-wr) * error['Range'].abs().mean()):.2%}"

            # Plot prediction
            figs.append(plotPrediction(y_real=tests['test'][0], y_pred=tests['test'][1]))
    
    return {'models': models, 'model_results': model_results, 'ticker_results':ticker_results, 
            'message': message, 'figs': figs, 'predictions': predictions, 'ticker': ticker}


def prepare3Dplot(df:pd.DataFrame, xname:str='level_0', yname:str='level_1', 
                  zname:str='level_3', title:str='', ret:bool=False
                  ) -> (np.ndarray, np.ndarray, np.ndarray):
    
    x = metrics[xname].unique()
    y = metrics[yname].unique()
    z = []
    for i in y:
        k = []
        for j in x:
            k.append(df[(df[xname] == j) & (df[yname] == i)][zname].iloc[0])
        z.append(k)
        
    z = np.array([np.array(i) for i in z])
        
    fig: go.Figure = go.Figure(data=[
        go.Surface(
            z=z, 
            y=y, 
            x=x,
            contours = {
                "z": {"show": True, "size": 0.05, 'usecolormap': True,
                        'highlightcolor': 'limegreen', 'project_z': True} 
                #  "start": 0.5, "end": 0.8, 
            }
        ),
        go.Surface(
            z=np.zeros(shape=z.shape), 
            y=y, 
            x=x,
            opacity=0.6, showscale=False

        ),
    ])

    fig.update_layout(
        template='gridon',
        scene = {
            'xaxis_title': '',
            'yaxis_title': '',
            'zaxis_title': ''
        }, 
        title=title, 
        autosize=False,
        width=900, height=700,
        margin=dict(l=20, r=20, b=20, t=30)
    )
    
    fig.show()
    
    if ret:
        return x, y, z


def calculateDfEquity(orig_df:pd.DataFrame, signal_col:str, equity:float=100000.0) -> pd.Series:
    
    balance = []
    profit = []
    df = orig_df[['Open', 'Range', signal_col]].copy()
    for i in df.index:
        candle = df.loc[i]
        if candle[signal_col] > 0:
            last_bal = balance[-1] if len(balance) > 0 else equity
            profit.append(math.floor(last_bal / candle['Open']) * candle['Range'])
        else:
            profit.append(0)
            
    df['profit'] = profit
    df['balance'] = df['profit'].cumsum() + equity
            
    return df['profit'], df['balance']

if __name__ == '__main__':

    use_pca = True
    complete = True
    plot = True

    tickers = ['SPY', '^GSPC', '^DJI', '^IXIC', '^FCHI', '^GDAXI', '^AORD', '^HSI', '^N225']
    args = [[ticker, use_pca] for ticker in tickers]

    import multiprocessing
    import time

    pool = multiprocessing.Pool(3)
    start_time = time.perf_counter()
    processes = [pool.apply_async(tickerModels, args=(ticker, use_pca, complete)) for ticker in tickers]
    result = [p.get() for p in processes]
    finish_time = time.perf_counter()
    
    print(f"Program finished in {finish_time-start_time} seconds")

    if plot:
        model_comparison = pd.DataFrame({k:v for r in result for k, v in r['model_results'].items()}).T # To select a group: model_comparison.xs('SPY', level=1, drop_level=False)
        ticker_comparison = pd.DataFrame({k:v for r in result for k, v in r['ticker_results'].items()}).T

        temp = model_comparison.copy()
        temp['wr_diff'] = temp['winrate'] - temp['winrate'].shift(1)
        temp['exp_diff'] = temp['expectancy'] - temp['expectancy'].shift(1)

        metrics = temp.xs('test', level=2, drop_level=True)
        if True:
            metrics = metrics.loc[[(True if 'decision_tree' not in i else False) \
                                    for i in metrics.index], :]
        metrics = metrics.copy()
        metrics.reset_index(drop=False, inplace=True)

        x, y, z = prepare3Dplot(metrics, zname='wr_diff', ret=True,
                                title='Variation of the model precision (test - training)')
        x, y, z = prepare3Dplot(metrics, zname='exp_diff', ret=True,
                                title='Variation of the model expectancy (test - training)')
        x, y, z = prepare3Dplot(metrics, zname='expectancy', ret=True,
                                title='Expectancy')

    models = {key: value for r in result for v in r['models'].values() for key, value in v.items()}
    pred_data = {r['ticker']: {k:v for k, v in r['predictions'].items()} for r in result}
    
    final = {t:pd.DataFrame() for t in tickers}
    for ticker, m in pred_data.items():
        if ticker not in final:
            final[ticker] = pd.DataFrame()
        for k, v in m.items():
            if final[ticker].empty:
                final[ticker] = v.copy()
            final[ticker][f'model_{k}'] = v['Pred_side']
            final[ticker][f'return_{k}'] = v['Range'] * v['Pred_side']
            final[ticker][f'cum_profit_{k}'], final[ticker][f'cum_equity_{k}'] = calculateDfEquity(v, signal_col='Pred_side')

        
    default_colors = [
        '#1f77b4',  # muted blue
        '#ff7f0e',  # safety orange
        '#2ca02c',  # cooked asparagus green
        '#d62728',  # brick red
        '#9467bd',  # muted purple
        '#8c564b',  # chestnut brown
        '#e377c2',  # raspberry yogurt pink
        '#7f7f7f',  # middle gray
        '#bcbd22',  # curry yellow-green
        '#17becf'   # blue-teal
    ]
    colors = {m: default_colors[i] for i, m in enumerate(models.keys())}

    cols = 2
    rows = math.ceil(len(tickers)/2)
    fig = make_subplots(
        rows=rows, cols=cols,
        column_widths=[1]*cols,
        row_heights=[1]*rows,
        vertical_spacing=0.05,
        subplot_titles=[f"<b>{ticker.replace('^', '').upper()}</b>" for ticker in tickers]
    )
    r = 1
    c = 1
    for ticker in final.values():
        temp = ticker[[c for c in ticker.columns if 'cum_equity' in c and 'decision_tree' not in c]]
        for t in temp.columns:
            model = t.split('_')[2:]
            fig.add_trace(go.Scatter(x=temp.index, y=temp[t], 
                                    name=(' '.join(model)).capitalize(),
                                    marker_color=colors['_'.join(model)],
                                    showlegend=True if r == 1 and c == 1 else False), 
                        row=r, col=c)
            
        if c < cols:
            c += 1
        elif c == cols:
            c = 1
            r += 1
            
    fig.update_layout(
        template='gridon',
        width=800,
        height=1600,
        legend=dict(y=0.05, x=0.65),
        margin=dict(
            l=35,
            r=15,
            b=20,
            t=30
        ),
    )