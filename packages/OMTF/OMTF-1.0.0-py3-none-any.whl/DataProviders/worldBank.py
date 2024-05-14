
import datetime as dt
import pandas as pd
import wbgapi as wb

class WorldBank:
    
    BASE_URL = 'https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?date=2000:2001&format=json'

    def __init__(self):

        self.codes = self.countryCodes()

    def series(self,query=None):

        return wb.series.info(q=query)

    def databases(self):

        return wb.source.info()

    def getData(self, keys:list, init:int=None, end:int=None, df:bool=True):

        if init == None:
            init = 1900
        if end == None:
            end = dt.datetime.today().year
        years = range(init, end)
        data = wb.data.DataFrame(keys, time=years).T
        data = data.to_dict()

        new_data = {}
        for d in data:
            for i in data[d]:
                if f'{d[0]}_{i}' not in new_data:
                    temp = {
                        'Country': self.codes[d[0]] if d[0] in self.codes else d[0],
                        'Year':i[2:],
                        d[1]:data[d][i],
                    }
                    new_data[f'{d[0]}_{i}'] = temp
                else:
                    new_data[f'{d[0]}_{i}'][d[1]] = data[d][i]

        data = [new_data[i] for i in new_data]

        return pd.DataFrame(data) if df else data

    def countryCodes(self):

        data = pd.read_html('https://countrycode.org/')[0]

        data = data.to_dict('records')
        rename_dict = {}
        for d in data:
            rename_dict[d['ISO CODES'].split(' / ')[1]] = d['COUNTRY']
          
        return rename_dict
    
    
if __name__ == '__main__':
    
    wbapi = WorldBank()
    wbapi.series('suicide')
    
    data = wbapi.getData(['NY.GDP.PCAP.CD', 'SP.POP.TOTL', 'IQ.SPI.OVRL',
                        'SH.STA.SUIC.P5'])
    data.rename(columns={'NY.GDP.PCAP.CD':'GDP', 
                        'SP.POP.TOTL':'POP', 
                        'BM.KLT.DINV.CD.WD':'OutFlow',
                        'AG.LND.AGRI.ZS':'AgriculturalLand',
                        'AG.LND.TOTL.UR.K2':'UrbanLand', 
                        'BM.GSR.MRCH.CD':'GoodsImports', 
                        'BM.GSR.NFSV.CD':'ServiceImports',
                        'BN.CAB.XOKA.CD':'AccountBalance', 
                        'BX.GSR.MRCH.CD':'GoodsExports', 
                        'BX.GSR.NFSV.CD':'ServiceExports', 
                        'DT.DOD.DSTC.IR.ZS':'ShortTermDebt',
                        'FI.RES.TOTL.DT.ZS':'ReservesOverDebt',
                        'FP.CPI.TOTL.ZG':'Inflation', 
                        'IQ.SPI.OVRL': 'StatPerfInd',
                        'SH.STA.SUIC.P5':'SuicideRate'},
                inplace=True)
        
    data = wbapi.getData(['SH.STA.SUIC.FE.P5', 'SH.STA.SUIC.MA.P5',
                        'SH.STA.SUIC.P5', 'SP.POP.TOTL'])
    data.rename(columns={'SH.STA.SUIC.FE.P5':'FemaleSuicide', 
                        'SH.STA.SUIC.MA.P5': 'MaleSuicide',
                        'SH.STA.SUIC.P5':'SuicideRate',
                        'SP.POP.TOTL':'POP'},
                inplace=True)
    
    
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Make the plot with with the data filtered
    fig = make_subplots(rows=1, cols=1,)

    filtered = data['Country'].unique().tolist()
    filtered = ['Austria', 'Belgium', 'Canada', 'China', 'Czech Republic',
                'Denmark', 'Finland', 'France', 'Germany', 'Greece', 'Iceland', 
                'India', 'Ireland', 'Italy', 'Japan', 'Luxembourg', 'Netherlands', 
                'New Zealand', 'Norway', 'Poland', 'Portugal', 'Russia',
                'Australia','United Kingdom', 'United States', 'Sweden', 
                'Switzerland', 'Spain']
                
    #filtered = data['Country'].unique().tolist()
    for country in data.groupby('Country'):
        if country[0] not in filtered:
            continue
        temp_df = country[1].sort_values('Year')
        #fig.add_trace(
        #    go.Scatter(x=temp_df['Year'], y=temp_df['SuicideRate']*temp_df['POP']/100000, name=country[0]),
        #    row=1, col=1
        #)
        fig.add_trace(
            go.Scatter(x=temp_df['Year'], y=temp_df['MaleSuicide']/(temp_df['MaleSuicide'] + temp_df['FemaleSuicide']), name=country[0]+' Male'),
            row=1, col=1
        )

    fig.update_layout(height=600, width=800, title_text="Charting each year's top rank")
    fig.show()
    
    
    
    
    # Get the correlation matrix for a list of features
    cor = data.corr()

    # Plot the data
    heat = go.Heatmap(
        z=cor, x=cor.columns, y=cor.columns,
        zmin=-1, zmax=1,
        text=[[i*100//1/100 for i in sublist] for sublist in cor.values],
        texttemplate="%{text}", textfont={"size":10}
    )

    layout = go.Layout(
        title_text='Features Correlation Matrix', title_x=0.5, 
        width=1000, height=800,
        xaxis_showgrid=False, yaxis_showgrid=False, yaxis_autorange='reversed',
    )

    fig = go.Figure(data=[heat], layout=layout)
    fig.show()