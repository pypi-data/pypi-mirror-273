
import json
import requests
import pandas as pd

class WHO:

    headers = {'Content-type': 'application/json'}
    BASEURL = 'https://ghoapi.azureedge.net/api/'
    INDICATORS = 'https://ghoapi.azureedge.net/api/Indicator'
    COUNTRIES = 'https://countrycode.org/'

    def _request(self, url:str):

        # Post the data request to the BLS API. Return the resulting JSON structure.

        post = requests.post(url, headers = self.headers)
        data = json.loads(post.text)
        data_list = data['value']

        return data_list

    def indicators(self, key:str=None, df:bool=True):

        data = self._request(self.INDICATORS)
        data = pd.DataFrame(data)

        if key != None:
            data = data[data['IndicatorName'].str.contains(key)]

        return data if df else data.to_dict('records')


    def getData(self, indicator:str, df:bool=True):

        data = self._request(self.BASEURL+indicator)
        data = pd.DataFrame(data)
        data.replace({'SpatialDim': self.countryCodes(complete=False, df=False)}, 
                     inplace=True)
        #data.columns = [c.capitalize() for c in data.columns]

        return data if df else data.to_dict('records')

    def countryCodes(self, complete:bool=True, df:bool=True):

        data = pd.read_html(self.COUNTRIES)[0]

        if complete:
            data['ISO2'] = data['ISO CODES'].apply(lambda x: x.split(' / ')[0])
            data['ISO3'] = data['ISO CODES'].apply(lambda x: x.split(' / ')[1])
            
            return data if df else data.to_dict('records')

        data = data.to_dict('records')
        rename_dict = {}
        for d in data:
            rename_dict[d['ISO CODES'].split(' / ')[1]] = d['COUNTRY']
          
        return rename_dict




if __name__ == '__main__':
    
    who = WHO()
    
    ind = who.indicators(key='Population|poblation',df=True)
    ind
    
    population = who.getData('RS_1845')
    population
    
    suicide = who.getData('SDGSUICIDE')
    suicide['idx'] = suicide['SpatialDim'] + '_' + suicide['TimeDim'].astype(str)

    grouped = []
    for g in suicide.groupby('idx'):

        temp = g[1]
        df = pd.DataFrame([{
            'Country':temp['SpatialDim'].iloc[0],
            'Year':temp['TimeDim'].iloc[0],
            'Value':temp['NumericValue'].sum()}
        ])
        grouped.append(df)

    suicide = pd.concat(grouped)
    suicide.reset_index(drop=True, inplace=True)
    
    

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Make the plot with with the data filtered
    fig = make_subplots(rows=1, cols=1,)

    filtered = suicide['Country'].unique().tolist()
    filtered = ['Austria', 'Belgium', 'Canada', 'China', 'Czech Republic',
                'Denmark', 'Finland', 'France', 'Germany', 'Greece', 'Iceland', 
                'India', 'Ireland', 'Italy', 'Japan', 'Luxembourg', 'Netherlands', 
                'New Zealand', 'Norway', 'Poland', 'Portugal', 'Russia',
                'Australia','United Kingdom', 'United States', 'Sweden', 
                'Switzerland', 'Spain']
    for country in suicide.groupby('Country'):
        if country[0] not in filtered:
            continue
        temp_df = country[1].sort_values('Year')
        fig.add_trace(
            go.Scatter(x=temp_df['Year'], y=temp_df['Value'], name=country[0]),
            row=1, col=1
        )

    fig.update_layout(height=600, width=800, title_text="Charting each year's top rank")
    fig.show()
    
    # For each year get the 10 countries with bets happiness score
    years_complete = []
    for year in suicide.groupby('Year'):
        temp = year[1].sort_values('Value', ascending=False)
        years_complete.append(temp.head(10))
    years_complete = pd.concat(years_complete)

    # Make the plot with with the data filtered
    fig = make_subplots(rows=1, cols=1,)

    for country in years_complete.groupby('Country'):
        temp_df = country[1].sort_values('Year')
        fig.add_trace(
            go.Scatter(x=temp_df['Year'], y=temp_df['Value'], name=country[0]),
            row=1, col=1
        )

    fig.update_layout(height=600, width=800, title_text="Charting each year's top rank")
    fig.show()