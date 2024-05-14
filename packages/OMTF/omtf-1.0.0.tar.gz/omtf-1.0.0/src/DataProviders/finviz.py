
import datetime as dt
from random import choice

import certifi
import numpy as np
import pandas as pd
import urllib3
from bs4 import BeautifulSoup

from data import DataProvider

class Finviz(DataProvider):

    '''
    Class used for webscraping Finviz.
    '''

    # URLs and endpoints used
    BASE_URL: str = 'https://finviz.com'
    SCREENER_EP: str = '/screener.ashx?v=111&ft=4&o=-change&f='
    TICKER_EP: str = '/quote.ashx?ty=c&p=d&b=1&t='
    GROUPS_EP: str = '/groups.ashx?v=140&o=-change'

    def _request(self, url:str) -> BeautifulSoup:

        '''
        Makes a request with the correct header and certifications.

        Parameters
        ----------
        url: str
            String with the url from which to get the HTML.

        Returns
        -------
        soup: bs4.BeautifulSoup
            Contains the HTML of the url.
        '''

        content: urllib3.PoolManager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                               ca_certs=certifi.where()) \
                              .urlopen('GET',url,headers=self._random_header())
        soup: BeautifulSoup = BeautifulSoup(content.data,'html.parser')

        return soup

    def _getTable(self, soup:BeautifulSoup=None) -> pd.DataFrame:

        '''
        Extraction of screener table.

        Parameters
        ----------
        soup: bs4.BeautifulSoup
            HTML of a webpage.

        Returns
        -------
        table: pd.DataFrame
            Contains the screener table.
        '''
        
        soup: BeautifulSoup = self.soup if soup == None else soup
        
        table = soup.find('table', {'class':'screener_table'})
        if table:
            cols: list = [col.get_text().replace('\n', '') for col in table.find_all('th')]
            rows: list = [[a.get_text() for a in row.find_all('a')] \
                            for row in table.find_all('tr')[1:]]
            return pd.DataFrame(data=rows, columns=cols)
        else:
            return pd.DataFrame()
    
    def _getPages(self, filters:list=None) -> pd.DataFrame:

        '''
        Extraction of screener table.

        Parameters
        ----------
        filters: list
            List of filters to apply. The filters must be the ids of 
            the ones from finviz.com.

        Returns
        -------
        table: pd.DataFrame
            Contains the screener table.
        '''

        self.filters: list = self.filters if filters == None else filters
        complete_data: list = []
        
        # Defining the url and connecting to obtain html 
        self.tempurl: str = f"{self.BASE_URL}{self.SCREENER_EP}{','.join(self.filters)}"
        self.soup: BeautifulSoup = self._request(self.tempurl)
        complete_data.append(self._getTable())
        page = max([int(a.get_text().replace('\n', '')) \
                    for a in self.soup.find('td', {'id': 'screener_pagination'}).find_all('a') \
                    if a.get_text().replace('\n', '') != ''])
        
        if page:
            n: int = page - 1
            print(n)
            if n > 0:
                for i in range(1, n):
                    self.tempurl: str = f"{self.BASE_URL}{self.SCREENER_EP}\
                                        {','.join(self.filters)}&r={i*2}1"
                    self.soup: BeautifulSoup = self._request(self.tempurl)
                    complete_data.append(self._getTable())
                    
            return pd.concat(complete_data)
        else:
            return pd.DataFrame()
        
    def screener(self,exchange:list=['nyse','nasd','amex'],
                  filters:list=['cap_smallunder','sh_avgvol_o500','sh_outstanding_u50',
                                'sh_price_u10','sh_relvol_o3'],
                  minpctchange:float=None, justtickers:bool=False) -> pd.DataFrame:
      
        '''
        Function to get data from Finviz Screener based on some filters.

        Parameters
        ----------
        exchange: list
            List of selected exchanges. The options are: 'nyse', 'nasd' and 
            'amex'.
        filters: list
            List of filters used by Finviz in their url.
        minpctchange: float
            Minimum percentage change of the ticker in case you want to 
            filter it.
        justtickers: bool
            True to return just the ticker names. False if you want all 
            the default data offered from the ticker by Finviz.

        Returns
        -------
        screener_df: pd.DataFrame
            DataFrame containing the screener.
        '''

        # Variables
        self.minpctchange = minpctchange
        self.justtickers = justtickers
        
        minpctchange = self.minpctchange if minpctchange == None else minpctchange
        
        # Getting data
        if len(exchange) == 0:
            self.filters: list = filters
            self.screener_df: pd.DataFrame = self._getPages(filters=filters)

        else:
            temp_data: list = []
            for ex in exchange:
                self.filters: list = ['exch_'+ex]+filters
                temp: pd.DataFrame = self._getPages(filters=['exch_'+ex]+filters)
                temp['Exchange'] = ex
                temp_data.append(temp.copy())
                            
            self.screener_df: pd.DataFrame = pd.concat(temp_data, ignore_index=True)
    
        self.screener_df: pd.DataFrame = self.screener_df.drop_duplicates()
        self.screener_df['Market Cap'] = self.screener_df['Market Cap'].apply(lambda x: self._to_numeric(x))
        self.screener_df['P/E'] = self.screener_df['P/E'].apply(lambda x: float('nan' if x == '-' else x))
        self.screener_df['Price'] = self.screener_df['Price'].astype(float)
        self.screener_df['Change'] = self.screener_df['Change'].apply(lambda x: float(x.replace('%', ''))/100)
        self.screener_df['Volume'] = self.screener_df['Volume'].str.replace(',','').astype(float)
        self.screener_df: pd.DateFrame = self.screener_df[self.screener_df['Change'] >= minpctchange/100]

        return self.screener_df

    def tickerCompany(self, ticker:str=None, soup:BeautifulSoup=None) -> dict:

        '''
        Gets company info from a ticker in finviz.

        Parameters
        ----------
        ticker: str
            Ticker for which to extract the company data. If it is not None the 
            HTML will be overwritten with one for this ticker.
        soup: bs4.BeautifulSoup
            HTML code.

        Returns
        -------
        company_info: dict
            Contains the data for the company.
        '''

        if ticker != None:
            url: str = self.BASE_URL + self.TICKER_EP + ticker            
            soup: BeautifulSoup = self._request(url)
        elif soup == None and ticker == None:
            raise(ValueError('Soup or ticker must be entered!'))


        # Get company info
        sources: dict = self.tickerSources(soup=soup)
        header = soup.find('div', {'class': 'quote-header_left'})
        details = soup.find('div', {'class': 'quote-links'}).find('div').find_all('a')
                        
        company_info: dict = {
            'Symbol': header.find('h1')['data-ticker'],
            'Exchange': details[3].get_text(),
            'Company': header.find('a').get_text().replace('\n', '') \
                            .replace('\r', '').replace('  ', ''),
            'Web': header.find('a')['href'],
            'Sector': details[0].get_text(),
            'Industry': details[1].get_text(),
            'Country': details[2].get_text(),
            'Description': soup.find_all('td', {'class':'fullview-profile'})[0] \
                              .get_text(),
            'CIK': int(sources['EDGAR'].split('=')[-1].zfill(10)) \
                    if 'EDGAR' in sources else float('nan'),
        }

        return company_info

    def tickerData(self, ticker:str=None, soup:BeautifulSoup=None) -> dict:

        '''
        Gets key data from a ticker in finviz.

        Parameters
        ----------
        ticker: str
            Ticker for which to extract the key metrics. If is not None the 
            HTML will be overwritten with one for this ticker.
        soup: bs4.BeautifulSoup
            HTML code.

        Returns
        -------
        main_data: dict
            Contains the key data for the ticker.
        '''

        if ticker != None:
            url: str = self.BASE_URL + self.TICKER_EP + ticker            
            soup: BeautifulSoup = self._request(url)
        elif soup == None and ticker == None:
            raise(ValueError('Soup or ticker must be entered!'))

        main_data: dict = {
            group['keys'][i]: (group['values'][i] if group['values'][i] != '-' else 'nan') for group in 
                [{'keys': [v.get_text() for v in row.find_all('td') if v['width'] == '7%'], 
                'values':[v.get_text() for v in row.find_all('td') if v['width'] == '8%']} \
                for row in soup.find('table', {'class': 'snapshot-table2'}).find_all('tr')] \
            for i in  range(len(group['keys']))
        }
        
        data: dict = {}
        for key in main_data:
            if ' / ' in main_data[key]:
                data[key.split(' / ')[0]] = main_data[key].split(' / ')[0]
                data[key.split(' / ')[1]] = main_data[key].split(' / ')[1]
            elif ' - ' in main_data[key]:
                data[key+' Low'] = main_data[key].split(' - ')[0]
                data[key+' High'] = main_data[key].split(' - ')[1]
            elif ' ' in main_data[key] and key not in ['Earnings', 'Index']:
                data[key+' Low'] = main_data[key].split(' ')[0]
                data[key+' High'] = main_data[key].split(' ')[1]
            else:
                data[key] = main_data[key]
        
        main_data: dict = {}
        for key in data:
            if '%' in data[key]:
                main_data[key+' Pct'] = self._to_numeric(data[key].replace('%',''))
            elif data[key] == 'Yes':
                main_data[key] = True
            elif data[key] == 'No':
                main_data[key] = False
            elif key == 'Earnings':
                main_data[key] = data[key].replace('AMC', 'After Market Close') \
                                          .replace('BMC', 'Before Market Close') 
            elif key == 'Index':
                main_data[key] = data[key].split(', ')
            else:
                main_data[key] = self._to_numeric(data[key])
        
        return main_data

    def tickerNews(self, ticker:str=None, soup:BeautifulSoup=None, 
                   df:bool=False) -> (list | pd.DataFrame):

        '''
        Gets news from a ticker in finviz.

        Parameters
        ----------
        ticker: str
            Ticker for which to extract the news. If is not None the 
            HTML will be overwritten with one for this ticker.
        soup: bs4.BeautifulSoup
            HTML code.
        df: bool
            True to return data in DataFrame.

        Returns
        -------
        news: list | pd.DataFrame
            Contains the news for the ticker.
        '''

        if ticker != None:
            url: str = self.BASE_URL + self.TICKER_EP + ticker            
            soup: BeautifulSoup = self._request(url)
        elif soup == None and ticker == None:
            raise(ValueError('Soup or ticker must be entered!'))
        
        table = soup.find('table', {'class': 'news-table'})
        news: list = [
            {'Date':row.find('td').get_text().replace('\n', '') \
                    .replace('\r', '').replace('  ', ''), 
            'Header':row.find('a').get_text(), 'Source':row.find('span').get_text(), 
            'URL':row.find('a')['href']} \
            for row in table.find_all('tr')
        ]
        
        prev_date = None
        news_data: list = []
        for p in news:
            temp_date: str = p['Date']
            if 'Today' in temp_date:
                temp_date = dt.datetime.today().strftime('%b-%d-%y') + ' ' + temp_date.split(' ')[-1]
            elif '-' not in temp_date:
                temp_date = prev_date + ' ' + temp_date
            temp_date: dt.datetime = dt.datetime.strptime(temp_date,'%b-%d-%y %I:%M%p')

            news_data.append({
                'Date': temp_date.strftime('%Y-%m-%d %H:%M:%S'),
                'Header': p['Header'],
                'Source': p['Source'],
                'URL': p['URL'],
            })
            prev_date: str = temp_date.strftime('%b-%d-%y')

        if df:
            news: pd.DataFrame = pd.DataFrame(news_data)
            # Set timezone awareness
            if 'Date' in news:
                news['Date'] = pd.to_datetime(news['Date'], 
                                              format='%Y-%m-%d %H:%M:%S')
                news.set_index('Date', drop=True, inplace=True)
                news.index = news.index.tz_localize(
                                        tz=dt.datetime.now(dt.timezone.utc) \
                                            .astimezone().tzinfo)
        else:
            news: list = news_data
        
        return news

    def tickerInsiders(self, ticker:str=None, soup:BeautifulSoup=None, 
                       df:bool=False) -> (list | pd.DataFrame):

        '''
        Gets insiders transactions from a ticker in finviz.

        Parameters
        ----------
        ticker: str
            Ticker for which to extract the insiders transactions. If is not 
            None the HTML will be overwritten with one for this ticker.
        soup: bs4.BeautifulSoup
            HTML code.
        df: bool
            True to return data in DataFrame.

        Returns
        -------
        insiders: list | pd.DataFrame
            Contains the insiders transactions for the ticker.
        '''

        if ticker != None:
            url: str = self.BASE_URL + self.TICKER_EP + ticker            
            soup: BeautifulSoup = self._request(url)
        elif soup == None and ticker == None:
            raise(ValueError('Soup or ticker must be entered!'))
        
        table = soup.find_all('table', {'class':'body-table'})
        
        if len(table) > 0:
            insiders = table[0]

            head: list = [j.get_text() for j in insiders.find_all('th')]
            urls: list = [i.find_all('a')[-1]['href'] for i in insiders.find_all('tr')[1:]]
            insiders: list = [[j.get_text() for j in i.find_all('td')] \
                                for i in insiders.find_all('tr')[1:]]

            insiders: pd.DataFrame = pd.DataFrame(data=insiders, columns=head)
            insiders['Date'] = insiders['Date'].apply(lambda x: 
                    f'{x} {dt.datetime.today().year-1}' \
                    if dt.datetime.strptime(f'{x} {dt.datetime.today().year}', '%b %d %Y') \
                    > dt.datetime.today() else f'{x} {dt.datetime.today().year}')
            insiders['Date'] = pd.to_datetime(insiders['Date'], format='%b %d %Y')
            insiders['Cost'] = insiders['Cost'].astype(float)
            insiders['#Shares'] = insiders['#Shares'].str.replace(',','').astype(int)
            insiders['Value ($)'] = insiders['Value ($)'].str.replace(',','').astype(float)
            insiders['#Shares Total'] = insiders['#Shares Total'].str.replace(',','').astype(float)
            insiders['SEC Form 4'] = insiders['SEC Form 4'].apply(lambda x: 
                    f'{dt.datetime.today().year-1} {x}' \
                    if dt.datetime.strptime(f'{dt.datetime.today().year-1} {x}', '%Y %b %d %I:%M %p') \
                    > dt.datetime.today() else f'{dt.datetime.today().year-1} {x}')
            insiders['SEC Form 4'] = pd.to_datetime(insiders['SEC Form 4'], format='%Y %b %d %I:%M %p')
            insiders['SEC URL'] = urls

            return insiders if df else insiders.to_dict('records')
        else:
            return pd.DataFrame() if df else []

    def tickerSources(self, ticker:str=None, soup:BeautifulSoup=None) -> dict:

        '''
        Gets other source for a ticker in finviz.

        Parameters
        ----------
        ticker: str
            Ticker for which to extract the sources. If is not None the HTML 
            will be overwritten with one for this ticker.
        soup: bs4.BeautifulSoup
            HTML code.

        Returns
        -------
        main_data: dict
            Contains the sources for the ticker.
        '''

        if ticker != None:
            url: str = self.BASE_URL + self.TICKER_EP + ticker            
            soup: BeautifulSoup = self._request(url)
        elif soup == None and ticker == None:
            raise(ValueError('Soup or ticker must be entered!'))

        references = soup.find_all('table')[-1].find_all('a')
        references: dict = {i.get_text().split(' ')[-1]: i['href'] for i in references}

        return references, soup

    def tickerInfo(self, tickers:list=None, df:bool=True) -> dict:

        '''
        Gets info of a list of tickers from finviz.

        Parameters
        ----------
        tickers: list
            List of tickers to look for.
        df: bool
            True to return data in dataframe format.

        Returns
        -------
        df: dict
            Contains the data of the .csv file.
        '''

        tickers: list = tickers if tickers != None else self.watchlist_df
                
        if isinstance(tickers,pd.DataFrame):
            ticker_list: list = tickers['Ticker'].tolist()
        elif isinstance(tickers,str):
            ticker_list: list = [tickers]
        elif isinstance(tickers,list):
            ticker_list: list = tickers

        final_data: dict = {} 
        for ticker in ticker_list:
            
            url: str = self.BASE_URL + self.TICKER_EP + ticker            
            soup: BeautifulSoup = self._request(url)

            # Get company info
            company_info: dict = self.tickerCompany(soup=soup)

            # Get key data
            main_data: dict = self.tickerData(soup=soup)

            data: dict = {**company_info, **main_data}

            # Get news
            data['News'] = self.tickerNews(soup=soup, df=df)

            # Get insiders transactions
            data['Insiders'] = self.tickerInsiders(soup=soup, df=df)
            
            # Get other sources for ticker
            data['Sources'] = self.tickerSources(soup=soup)

            final_data[ticker] = data

        return final_data

    def hotSectors(self, column:str='%Week', df:bool=True) -> (dict | pd.DataFrame):

        '''
        Function for extracting the sectors sorted.

        Parameters
        ----------
        column: str
            Column to sort by the sectors. Choose from: %Week, %Month, 
            %Quart, %Half, %Year, %YTD, %Change
        df: bool
            True to return data in dataframe format.

        Returns
        -------
        df: dict | pd.DataFrame
            Contains the data.
        '''
        url: str = self.BASE_URL + self.GROUPS_EP + '&g=sector'
        soup: BeautifulSoup = self._request(url)
        table = soup.find('table', {'class': 'groups_table'})

        # Columns
        columns: list = []
        columns_temp: list = [j.get_text().replace('\n', '') for j in table.find_all('th')]
        for c in columns_temp:
            if 'Perf' in c:
                c: str = c.replace('Perf ','%')
            elif 'Change' in c:
                c: str = '%'+c
            columns.append(c)

        # Rows
        rows: list = []
        rows_temp: set = table.find_all('tr')[1:]
        for r in rows_temp:
            data: list = []
            data_temp = r.find_all('td')
            for d in data_temp:
                d: str = d.get_text()
                if d[0].isnumeric() or d[1].isnumeric():
                    d = self._to_numeric(d)
                data.append(d)                
            rows.append(data)

        # Dataframe
        data_df: pd.DataFrame = pd.DataFrame(rows,columns=columns)
        data_df.sort_values(column,ascending=False,inplace=True)
        data_df.reset_index()
        if 'No.' in data_df.columns:
            data_df.drop(columns=['No.'], inplace=True)

        return data_df if df else data_df.to_dict('records')

    def hotIndustry(self,column:str='%Week', df:bool=True) -> (dict | pd.DataFrame):

        '''
        Function for extracting the industries sorted.

        Parameters
        ----------
        column: str
            Column to sort by the industries. Choose from: %Week, %Month, 
            %Quart, %Half, %Year, %YTD, %Change
        df: bool
            True to return data in dataframe format.

        Returns
        -------
        df: dict | pd.DataFrame
            Contains the data.
        '''
        url: str = self.BASE_URL + self.GROUPS_EP + '&g=industry'
        soup: BeautifulSoup = self._request(url)
        table = soup.find('table', {'class': 'groups_table'})

        # Columns
        columns: list = []
        columns_temp: list = [j.get_text().replace('\n', '') for j in table.find_all('th')]
        for c in columns_temp:
            if 'Perf' in c:
                c = c.replace('Perf ','%')
            elif 'Change' in c:
                c = '%'+c
            columns.append(c)

        # Rows
        rows: list = []
        rows_temp: set = table.find_all('tr')[1:]
        for r in rows_temp:
            data: list = []
            data_temp = r.find_all('td')
            for d in data_temp:
                d: str = d.get_text()
                if d[0].isnumeric() or d[1].isnumeric():
                    d = self._to_numeric(d)
                data.append(d)                
            rows.append(data)

        # Dataframe
        data_df = pd.DataFrame(rows,columns=columns)
        data_df.sort_values(column,ascending=False,inplace=True)
        data_df.reset_index()
        if 'No.' in data_df.columns:
            data_df.drop(columns=['No.'], inplace=True)

        return data_df if df else data_df.to_dict('records')
    


if __name__ == '__main__':

    fv = Finviz()
    stock_filters = ['cap_largeunder','sh_avgvol_o1000','ta_highlow20d_b0to10h',
                    'ta_perf_4w30o','ta_sma20_pa10','ta_sma50_pa']
    screen = fv.screener(exchange=['nasd','nyse','amex'],filters=stock_filters,minpctchange=-10.,justtickers=False)
    ticker = 'AAPL' #screen['Ticker'].iloc[0]
    #data = fv.tickerInfo([ticker])
    #sectors = fv.hotSectors()
    industries = fv.hotIndustry()
    #print(data)