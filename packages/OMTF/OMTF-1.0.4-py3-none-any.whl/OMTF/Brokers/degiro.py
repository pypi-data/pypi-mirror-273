
import datetime as dt
import json
import enum

import pandas as pd
import requests



def pretty_json(data):

    return json.dumps(data, indent=4, sort_keys=True)

class AssetType(enum.Enum):

    STOCKS: str = 'stocks'
    BONDS: str = 'bonds'
    CURRENCIES: str = 'currencies'
    FUTURES: str = 'futures'
    OPTIONS: str = 'options'
    CFD: str = 'cfd'
    ETFS: str = 'etfs'

class Order:

    class Type(enum.Enum):

        LIMIT: int = 0
        STOPLIMIT: int = 1
        MARKET: int = 2
        STOPLOSS: int = 3

    class Time(enum.Enum):
        
        DAY: int = 1
        GTC: int = 3
    
    class Side(enum.Enum):

        BUY: str = 'BUY'
        SELL: str = 'SELL'

class DataType(enum.Enum):

    PORTFOLIO: str = 'portfolio'
    CASHFUNDS: str = 'cashFunds'
    
class IntervalType(enum.Enum):

    D1: str = 'P1D',
    W1: str = 'P1W',
    M1: str = 'P1M',
    M3: str = 'P3M',
    M6: str = 'P6M',
    Y1: str = 'P1Y',
    Y3: str = 'P3Y',
    Y5: str = 'P5Y',
    Max: str = 'P50Y'
    
class ResolutionType:

    # PT1M, PT5M, PT10M, PT15M, PT1H, P1D, P7D, P1M, P3M, P1Y

    S1: str = 'PT1S'
    M1: str = 'PT1M',
    M5: str = 'PT5M',
    M10: str = 'PT10M',
    M15: str = 'PT15M',
    H1: str = 'PT1H',
    D1: str = 'P1D',
    D7: str = 'P7D',

    def resToSeconds(self, resolution:str):

        resolution = resolution.replace('PT', '').replace('P','')
        if 'S' in resolution:
            return int(resolution[:-1])
        elif 'M' in resolution:
            return int(resolution[:-1]) * 60
        elif 'H' in resolution:
            return int(resolution[:-1]) * 60 * 60
        elif 'D' in resolution:
            return int(resolution[:-1]) * 60 * 60 * 24
        else:
            raise ValueError('Not a valid resolution.')

class Product:

    def __init__(self, product):

        self.props = product  # for later access to any property which is not included below
        self.__id = product['id']
        self.__name = product['name']
        self.__isin = product['isin']
        self.__symbol = product['symbol']
        self.__min_contract = product['contractSize']
        self.__currency = product['currency']
        self.__product_type = product['productTypeId']
        self.__tradable = product['tradable']
        self.__close_price = product.get('closePrice')
        close_price_date = product.get('closePriceDate')
        self.__close_price_date = dt.datetime.strptime(close_price_date, '%Y-%m-%d').date() if close_price_date else None
        expiration_date = product.get('expirationDate')
        self.__expiration_date = dt.datetime.strptime(expiration_date, '%d-%m-%Y').date() if expiration_date else None
        self.__strike_price = product.get('strikePrice')

    def __getitem__(self, item):

        """e.g. product["exchangeId"] """
        return self.props[item]

    @property
    def id(self):

        return self.__id

    @property
    def name(self):

        return self.__name

    @property
    def isin(self):

        return self.__isin

    @property
    def symbol(self):

        return self.__symbol

    @property
    def min_contract(self):

        return self.__min_contract

    @property
    def currency(self):

        return self.__currency

    @property
    def product_type(self):

        return self.__product_type

    @property
    def tradable(self):

        return self.__tradable

    @property
    def close_price(self):

        return self.__close_price

    @property
    def close_price_date(self):

        return self.__close_price_date

    @property
    def expiration_date(self):

        return self.__expiration_date

    @property
    def strike_price(self):

        return self.__strike_price

    @property
    def is_option(self):  # stock option?

        return self.product_type == 8
    
class ClientInfo:

    def __init__(self, client_info):

        self.__token = client_info['id']
        self.__account_id = client_info['intAccount']
        self.__username = client_info['username']
        self.__first_name = client_info['firstContact']['firstName']
        self.__last_name = client_info['firstContact']['lastName']
        self.__email = client_info['email']

    @property
    def token(self):
        return self.__token

    @property
    def account_id(self):
        return self.__account_id

    @property
    def username(self):
        return self.__username

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def email(self):
        return self.__email
    
urls = {
    'allocationsUrl': "https://trader.degiro.nl/allocations/",
    'betaLandingPath': "/beta-trader/",
    'clientId': 3442517,
    'companiesServiceUrl': "https://trader.degiro.nl/dgtbxdsservice/",
    'dictionaryUrl': "https://trader.degiro.nl/product_search/config/dictionary/",
    'exanteReportingUrl': "https://trader.degiro.nl/exante-reporting",
    'favoritesUrl': "https://trader.degiro.nl/favorites/",
    'feedbackUrl': "https://trader.degiro.nl/feedback/",
    'i18nUrl': "https://trader.degiro.nl/i18n/",
    'landingPath': "/trader/",
    'latestSearchedProductsUrl': "https://trader.degiro.nl/latest-searched-products/secure/",
    'loginUrl': "https://trader.degiro.nl/login/es",
    'mobileLandingPath': "/trader/",
    'paUrl': "https://trader.degiro.nl/pa/secure/",
    'paymentServiceUrl': "https://trader.degiro.nl/payments/",
    'productNotesUrl': "https://trader.degiro.nl/product-notes-service/secure/",
    'productSearchUrl': "https://trader.degiro.nl/product_search/secure/",
    'productSearchV2Url': "https://internal.degiro.eu/dgproductsearch/secure/",
    'productTypesUrl': "https://trader.degiro.nl/product_search/config/productTypes/",
    'refinitivAgendaUrl': "https://trader.degiro.nl/dgtbxdsservice/agenda/v2",
    'refinitivClipsUrl': "https://trader.degiro.nl/refinitiv-insider-proxy/secure/",
    'refinitivCompanyProfileUrl': "https://trader.degiro.nl/dgtbxdsservice/company-profile/v2",
    'refinitivCompanyRatiosUrl': "https://trader.degiro.nl/dgtbxdsservice/company-ratios",
    'refinitivEsgsUrl': "https://trader.degiro.nl/dgtbxdsservice/esgs",
    'refinitivEstimatesUrl': "https://trader.degiro.nl/dgtbxdsservice/estimates-summaries",
    'refinitivFinancialStatementsUrl': "https://trader.degiro.nl/dgtbxdsservice/financial-statements",
    'refinitivInsiderTransactionsUrl': "https://trader.degiro.nl/dgtbxdsservice/insider-transactions",
    'refinitivInsidersReportUrl': "https://trader.degiro.nl/dgtbxdsservice/insiders-report",
    'refinitivInvestorUrl': "https://trader.degiro.nl/dgtbxdsservice/investor",
    'refinitivNewsUrl': "https://trader.degiro.nl/dgtbxdsservice/newsfeed/v2",
    'refinitivShareholdersUrl': "https://trader.degiro.nl/dgtbxdsservice/shareholders",
    'refinitivTopNewsCategoriesUrl': "https://trader.degiro.nl/dgtbxdsservice/newsfeed/v2/top-news-categories",
    'reportingUrl': "https://trader.degiro.nl/reporting/secure/",
    'sessionId': "CC36B531899BB8A7E010ED1CC9E7E753.prod_a_168_3",
    'settingsUrl': "https://trader.degiro.nl/settings/",
    'taskManagerUrl': "https://trader.degiro.nl/taskmanager/",
    'tradingUrl': "https://trader.degiro.nl/trading/secure/",
    'translationsUrl': "https://trader.degiro.nl/translations/",
    'vwdChartApiUrl': "https://charting.vwdservices.com/hchart/v1/deGiro/api.js",
    'vwdGossipsUrl': "https://solutions.vwdservices.com/customers/degiro.nl/news-feed/api/",
    'vwdNewsUrl': "https://solutions.vwdservices.com/customers/degiro.nl/news-feed/api/",
    'vwdQuotecastServiceUrl' : "https://trader.degiro.nl/vwd-quotecast-service/",
}

class DeGiro(object):

    __LOGIN_URL = 'https://trader.degiro.nl/login/secure/login'
    __LOGIN_TOTP_URL = 'https://trader.degiro.nl/login/secure/login/totp'
    __CONFIG_URL = 'https://trader.degiro.nl/login/secure/config'

    __LOGOUT_URL = 'https://trader.degiro.nl/trading/secure/logout'

    __CLIENT_INFO_URL = 'https://trader.degiro.nl/pa/secure/client'

    __GET_STOCKS_URL = 'https://trader.degiro.nl/products_s/secure/v5/stocks'
    __GET_URL = 'https://trader.degiro.nl/products_s/secure/v5/'
    ##__GET_STOCKS_URL = 'https://trader.degiro.nl/products_s/secure/v5/etfs'
    ##__GET_OPTIONS_URL = 'https://trader.degiro.nl/products_s/secure/v5/options'
    __PRODUCT_SEARCH_URL = 'https://trader.degiro.nl/product_search/secure/v5/products/lookup'
    __PRODUCT_INFO_URL = 'https://trader.degiro.nl/product_search/secure/v5/products/info'
    __ID_DICTIONARY_URL = 'https://trader.degiro.nl/product_search/config/dictionary'
    __TRANSACTIONS_URL = 'https://trader.degiro.nl/reporting/secure/v4/transactions'
    __ORDERS_URL = 'https://trader.degiro.nl/reporting/secure/v4/order-history'
    __ACCOUNT_URL = 'https://trader.degiro.nl/reporting/secure/v6/accountoverview'
    __DIVIDENDS_URL = 'https://trader.degiro.nl/reporting/secure/v3/ca/'

    __PLACE_ORDER_URL = 'https://trader.degiro.nl/trading/secure/v5/checkOrder'
    __ORDER_URL = 'https://trader.degiro.nl/trading/secure/v5/order/'

    __DATA_URL = 'https://trader.degiro.nl/trading/secure/v5/update/'
    __PRICE_DATA_URL = 'https://charting.vwdservices.com/hchart/v1/deGiro/data.js'
    __NEWS_DATA_URL = 'https://solutions.vwdservices.com/customers/degiro.nl/news-feed/api/'
    __CALENDAR_DATA_URL = 'https://trader.degiro.nl/dgtbxdsservice/agenda/v2'
    __TOPNEWS_DATA_URL = 'https://trader.degiro.nl/dgtbxdsservice/newsfeed/v2/top-news-preview?intAccount=51060786&sessionId=C40B0EC272B45977BB4F2FFA75CFC051.prod_a_165_4'
    __LATESTNEWS_DATA_URL = 'https://trader.degiro.nl/dgtbxdsservice/newsfeed/v2/latest-news?offset=0&languages=es&limit=10&intAccount=51060786&sessionId=C40B0EC272B45977BB4F2FFA75CFC051.prod_a_165_4'
    __FINANCIAL_STATEMENTS_DATA_URL = 'https://trader.degiro.nl/dgtbxdsservice/financial-statements/LU1681048804?intAccount=51060786&sessionId=C40B0EC272B45977BB4F2FFA75CFC051.prod_a_165_4'
    __COMPANY_RATIOS = 'https://trader.degiro.nl/dgtbxdsservice/company-ratios/LU1681048804?intAccount=51060786&sessionId=C40B0EC272B45977BB4F2FFA75CFC051.prod_a_165_4'
    __COMPANY_PROFILE = 'https://trader.degiro.nl/dgtbxdsservice/company-profile/v2/LU1681048804?intAccount=51060786&sessionId=C40B0EC272B45977BB4F2FFA75CFC051.prod_a_165_4'

    __GET_REQUEST = 0
    __POST_REQUEST = 1
    __DELETE_REQUEST = 2

    client_token = None
    session_id = None
    client_info = None
    confirmation_id = None
    username = None
    password = None
    totp = None

    def __init__(self, username:str, password:str, totp:str=None, login:bool=True):

        '''
        Class used to connect DeGiro.
        '''

        self._id_dictionary = None
        self.username = username
        self.password = password
        self.totp = totp
        if login:
            self.login(username=username, password=password, totp=totp)
            info = self.clientInfo()
            self.clientToken()

    # @staticmethod
    def __request(self, url:str, cookie:dict=None, payload:dict=None, headers:dict=None, 
                  data:dict=None, post_params:dict=None, request_type:int=__GET_REQUEST,
                  error_message:str='An error occurred.') -> dict:

        '''
        Carries out the login to DeGiro.

        Parameters
        ----------
        username: str
            Username of the account.
        password: str
            Password of the account.
        totp: str
            One time password, is optional.

        Returns
        -------
        client_info_response: dict
            Contains the information of the client.
        '''

        if not headers:
            headers = {
                'Accept-Encoding': 'gzip, deflate', 
                'Accept': '*/*', 
                'Connection': 'keep-alive'
            }
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                                "Chrome/108.0.0.0 Safari/537.36"

        if request_type == DeGiro.__DELETE_REQUEST:
            response = requests.delete(url, headers=headers, json=payload)
        elif request_type == DeGiro.__GET_REQUEST and cookie:
            response = requests.get(url, headers=headers, cookies=cookie)
        elif request_type == DeGiro.__GET_REQUEST:
            response = requests.get(url, headers=headers, params=payload)
        elif request_type == DeGiro.__POST_REQUEST and headers and data:
            response = requests.post(url, headers=headers, params=payload, data=data)
        elif request_type == DeGiro.__POST_REQUEST and post_params:
            response = requests.post(url, headers=headers, params=post_params, json=payload)
        elif request_type == DeGiro.__POST_REQUEST:
            response = requests.post(url, headers=headers, json=payload)
        else:
            raise Exception(f'Unknown request type: {request_type}')
        
        self.r = response
        
        if response.status_code == 200 or response.status_code == 201:
            try:
                return response.json()
            except:
                return "No data retrieved"
        else:
            raise Exception(f'{error_message} Response: {response.text}')

    def __request_iter(self, url:str, cookie:dict=None, payload:dict=None, headers:dict=None, 
                  data:dict=None, post_params:dict=None, request_type:int=__GET_REQUEST,
                  error_message:str='An error occurred.') -> dict:

        '''
        Carries out the login to DeGiro.

        Parameters
        ----------
        username: str
            Username of the account.
        password: str
            Password of the account.
        totp: str
            One time password, is optional.

        Returns
        -------
        client_info_response: dict
            Contains the information of the client.
        '''

        if not headers:
            headers = {}
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                                "Chrome/108.0.0.0 Safari/537.36"

        request = False
        c = 0
        while not request:
            if request_type == DeGiro.__DELETE_REQUEST:
                response = requests.delete(url, headers=headers, json=payload)
            elif request_type == DeGiro.__GET_REQUEST and cookie:
                response = requests.get(url, headers=headers, cookies=cookie)
            elif request_type == DeGiro.__GET_REQUEST:
                response = requests.get(url, headers=headers, params=payload)
            elif request_type == DeGiro.__POST_REQUEST and headers and data:
                response = requests.post(url, headers=headers, params=payload, data=data)
            elif request_type == DeGiro.__POST_REQUEST and post_params:
                response = requests.post(url, headers=headers, params=post_params, json=payload)
            elif request_type == DeGiro.__POST_REQUEST:
                response = requests.post(url, headers=headers, json=payload)
            else:
                raise Exception(f'Unknown request type: {request_type}')
            
            print(response)
            self.r = response
            
            if response.status_code == 200 or response.status_code == 201:
                try:
                    request = True
                    return response.json()
                except:
                    self.login()
                    info = self.clientInfo()
                    self.clientToken()
                    print(response.text)
                    request = False
            else:
                self.login()
                info = self.clientInfo()
                self.clientToken()
                request = False
                print('Loged in')
            
            if c > 5:
                raise Exception(f'{error_message} Response: {response.text}')
            else:
                c += 1

    def login(self, username:str=None, password:str=None, totp:str=None) -> dict:

        '''
        Carries out the login to DeGiro.

        Parameters
        ----------
        username: str
            Username of the account.
        password: str
            Password of the account.
        totp: str
            One time password, is optional.

        Returns
        -------
        client_info_response: dict
            Contains the information of the client.
        '''

        self.username = self.username if username == None else username
        self.password = self.password if password == None else password
        self.totp = self.totp if totp == None else totp

        # Request login
        login_payload = {
            'username': self.username,
            'password': self.password,
            'isPassCodeReset': False,
            'isRedirectToMobile': False
        }
        if self.totp is not None:
            login_payload["oneTimePassword"] = self.totp
            url = DeGiro.__LOGIN_TOTP_URL
        else:
            url = DeGiro.__LOGIN_URL
            
        self.login_response = self.__request(url, payload=login_payload, 
                                        request_type=DeGiro.__POST_REQUEST,
                                        error_message='Could not login.')
        
        self.session_id = self.login_response['sessionId']

    def clientToken(self) -> dict:

        '''
        Gets the client Token.

        Returns
        -------
        client_token_response: dict
            Contains the information of the client's session.
        '''
        
        client_token_response = self.__request(DeGiro.__CONFIG_URL, cookie={'JSESSIONID': self.session_id}, 
                                               request_type=DeGiro.__GET_REQUEST,
                                               error_message='Could not get client config.')
        self.token_response = client_token_response
        self.client_token = client_token_response['data']['clientId']

        return client_token_response
    
    def clientInfo(self) -> dict:

        '''
        Gets information about the client.

        Returns
        -------
        client_info_response: dict
            Contains the information of the client.
        '''
        
        client_info_payload = {'sessionId': self.session_id}
        client_info_response = self.__request(DeGiro.__CLIENT_INFO_URL, payload=client_info_payload,
                                              error_message='Could not get client info.')
        self.client_info = ClientInfo(client_info_response['data'])

        return client_info_response

    def logout(self) -> None:

        '''
        Carries out the logout of DeGiro.
        '''

        logout_payload = {
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id,
        }

        self.__request(DeGiro.__LOGOUT_URL + ';jsessionid=' + self.session_id, 
                       payload=logout_payload,
                       error_message='Could not log out')

    def searchProducts(self, search_text:str, limit:int=1):

        product_search_payload = {
            'searchText': search_text,
            'limit': limit,
            'offset': 0,
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }

        return self.__request(DeGiro.__PRODUCT_SEARCH_URL, payload=product_search_payload,
                              error_message='Could not get products.')['products']

    def productInfo(self, product_id:str):

        product_info_payload = {
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }

        return self.__request(DeGiro.__PRODUCT_INFO_URL, payload=product_info_payload,
                              headers={'content-type': 'application/json'},
                              data=json.dumps([str(product_id)]),
                              request_type=DeGiro.__POST_REQUEST,
                              error_message='Could not get product info.')['data'][str(product_id)]

    @property
    def id_dictionary(self):

        if self._id_dictionary:  # already cached
            return self._id_dictionary

        raw_dict = self.__request(DeGiro.__ID_DICTIONARY_URL, error_message='Could not get Degiro ID dictionary.')
        self._id_dictionary = {k: {str(i["id"]): i for i in ids} for k, ids in raw_dict.items()}

        return self._id_dictionary

    def transactions(self, from_date:dt.datetime=None, to_date:dt.datetime=None, 
                     group_transactions:bool=False) -> dict:

        '''
        [{
            'id': 405196840,
            'productId': 14501924,
            'date': '2023-10-05T11:11:44+02:00',
            'buysell': 'B',
            'price': 78.2505,
            'quantity': 1,
            'total': -78.2505,
            'orderTypeId': 2,
            'counterParty': 'MK',
            'transfered': False,
            'fxRate': 0,
            'nettFxRate': 0,
            'grossFxRate': 0,
            'autoFxFeeInBaseCurrency': 0,
            'totalInBaseCurrency': -78.2505,
            'feeInBaseCurrency': -1.0,
            'totalFeesInBaseCurrency': -1.0,
            'totalPlusFeeInBaseCurrency': -79.2505,
            'totalPlusAllFeesInBaseCurrency': -79.2505,
            'transactionTypeId': 0,
            'tradingVenue': 'XPAR',
            'executingEntityId': '529900MKYC1FZ83V3121'
        }]
        '''

        if to_date == None:
            to_date = dt.datetime.today()
        if from_date == None:
            from_date = to_date - dt.timedelta(days=90)

        transactions_payload = {
            'fromDate': from_date if isinstance(from_date, str) else from_date.strftime('%d/%m/%Y'),
            'toDate': to_date if isinstance(to_date, str) else to_date.strftime('%d/%m/%Y'),
            'group_transactions_by_order': group_transactions,
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }

        return self.__request(DeGiro.__TRANSACTIONS_URL, payload=transactions_payload,
                              error_message='Could not get transactions.')['data']

    def accountHistory(self, from_date:dt.datetime=None, to_date:dt.datetime=None) -> dict:

        '''
        {'cashMovements': [{
            'date': '2023-10-05T11:11:44+02:00',
            'valueDate': '2023-10-05T11:11:44+02:00',
            'id': 1826447127,
            'orderId': '11c4e9cf-f672-409d-a51d-87638eaa86cb',
            'description': 'Costes de transacción y/o externos de DEGIRO',
            'productId': 14501924,
            'currency': 'EUR',
            'change': -1.0,
            'balance': {'flatexCash': 1999.99,
                'cashFund': [{'participation': 0.0, 'price': 10043.68, 'id': 15694501}],
                'unsettledCash': -79.25,
                'total': 1920.74},
            'type': 'CASH_TRANSACTION'},
            {'date': '2023-10-05T11:11:44+02:00',
            'valueDate': '2023-10-05T11:11:44+02:00',
            'id': 405196840,
            'orderId': '11c4e9cf-f672-409d-a51d-87638eaa86cb',
            'description': 'Compra 1 AMUNDI ETF SP 500@78,2505 EUR (LU1681048804)',
            'productId': 14501924,
            'currency': 'EUR',
            'change': -78.25,
            'balance': {'flatexCash': 1999.99,
                'cashFund': [{'participation': 0.0, 'price': 10043.68, 'id': 15694501}],
                'unsettledCash': -78.25,
                'total': 1921.74},
            'type': 'TRANSACTION'},
            {'date': '2023-10-01T16:03:20+02:00',
            'valueDate': '2023-09-30T23:59:59+02:00',
            'id': 1819703177,
            'description': 'Flatex Interest Income',
            'currency': 'EUR',
            'change': 0.0,
            'balance': {'flatexCash': 1999.99,
                'cashFund': [{'participation': 0.0, 'price': 10037.4, 'id': 15694501}],
                'unsettledCash': 0.0,
                'total': 1999.99},
            'type': 'CASH_TRANSACTION'},
            {'date': '2023-09-11T16:50:56+02:00',
            'valueDate': '2023-09-11T16:50:56+02:00',
            'id': 1800039138,
            'description': 'Transferir desde su Cuenta de Efectivo en flatexDEGIRO Bank: 0,01 EUR',
            'currency': 'EUR',
            'balance': {'flatexCash': 1999.99,
                'cashFund': [{'participation': 0.0, 'price': 10019.61, 'id': 15694501}],
                'unsettledCash': 0.0,
                'total': 1999.99},
            'type': 'FLATEX_CASH_SWEEP'},
            {'date': '2023-09-11T16:50:56+02:00',
            'valueDate': '2023-09-11T16:50:56+02:00',
            'id': 1800039137,
            'description': 'Degiro Cash Sweep Transfer',
            'productId': 17707507,
            'currency': 'EUR',
            'change': 0.01,
            'balance': {'flatexCash': 2000.0,
                'cashFund': [{'participation': 0.0, 'price': 10019.61, 'id': 15694501}],
                'unsettledCash': 0.0,
                'total': 2000.0},
            'type': 'FLATEX_CASH_SWEEP'},
            {'date': '2023-09-09T04:51:49+02:00',
            'valueDate': '2023-09-08T23:59:59+02:00',
            'id': 1799407261,
            'description': 'Flatex Instant Deposit',
            'currency': 'EUR',
            'change': 2000.0,
            'balance': {'flatexCash': 2000.0,
                'cashFund': [{'participation': 0.0, 'price': 10017.02, 'id': 15694501}],
                'unsettledCash': -0.01,
                'total': 1999.99},
            'type': 'CASH_TRANSACTION'},
            {'date': '2023-09-09T04:51:49+02:00',
            'valueDate': '2023-09-08T23:59:59+02:00',
            'id': 1799407260,
            'description': 'Reservation iDEAL / Sofort Deposit',
            'currency': 'EUR',
            'change': -2000.0,
            'balance': {'cashFund': [{'participation': 0.0,
                'price': 10017.02,
                'id': 15694501}],
                'unsettledCash': -0.01,
                'total': -0.01},
            'type': 'CASH_TRANSACTION'},
            {'date': '2023-09-07T16:34:58+02:00',
            'valueDate': '2023-09-07T16:34:58+02:00',
            'id': 1798346976,
            'description': 'Transferir desde su Cuenta de Efectivo en flatexDEGIRO Bank: 0,99 EUR',
            'currency': 'EUR',
            'balance': {'cashFund': [{'participation': 0.0,
                'price': 10016.17,
                'id': 15694501}],
                'unsettledCash': 1999.99,
                'total': 1999.99},
            'type': 'FLATEX_CASH_SWEEP'},
            {'date': '2023-09-07T16:34:58+02:00',
            'valueDate': '2023-09-07T16:34:58+02:00',
            'id': 1798346975,
            'description': 'Degiro Cash Sweep Transfer',
            'productId': 17707507,
            'currency': 'EUR',
            'change': 0.99,
            'balance': {'flatexCash': 0.99,
                'cashFund': [{'participation': 0.0, 'price': 10016.17, 'id': 15694501}],
                'unsettledCash': 1999.99,
                'total': 2000.98},
            'type': 'FLATEX_CASH_SWEEP'},
            {'date': '2023-09-07T13:35:32+02:00',
            'valueDate': '2023-09-07T13:35:32+02:00',
            'id': 1798112541,
            'description': 'Comisión por transferencia Trustly/Sofort',
            'currency': 'EUR',
            'change': -1.0,
            'balance': {'flatexCash': 0.99,
                'cashFund': [{'participation': 0.0, 'price': 10016.17, 'id': 15694501}],
                'unsettledCash': 1999.0,
                'total': 1999.99},
            'type': 'CASH_TRANSACTION'},
            {'date': '2023-09-07T13:35:32+02:00',
            'valueDate': '2023-09-07T13:35:32+02:00',
            'id': 1798112540,
            'description': 'Reservation iDEAL / Sofort Deposit',
            'currency': 'EUR',
            'change': 2000.0,
            'balance': {'flatexCash': 0.99,
                'cashFund': [{'participation': 0.0, 'price': 10016.17, 'id': 15694501}],
                'unsettledCash': 2000.0,
                'total': 2000.99},
            'type': 'CASH_TRANSACTION'}
        ]}
        '''
        
        if to_date == None:
            to_date = dt.datetime.today()
        if from_date == None:
            from_date = to_date - dt.timedelta(days=90)

        account_payload = {
            'fromDate': from_date if isinstance(from_date, str) else from_date.strftime('%d/%m/%Y'),
            'toDate': to_date if isinstance(to_date, str) else to_date.strftime('%d/%m/%Y'),
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }

        return self.__request(DeGiro.__ACCOUNT_URL, payload=account_payload,
                              error_message='Could not get account overview.')['data']

    def futureDividends(self) -> dict:

        dividends_payload = {
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }

        return self.__request(DeGiro.__DIVIDENDS_URL + str(self.client_info.account_id), 
                              payload=dividends_payload,
                              error_message='Could not get future dividends.')['data']

    def getOrders(self, from_date:dt.datetime=None, to_date:dt.datetime=None, 
                  not_executed:bool=False) -> dict:
        
        '''
        [{
            'created': '2023-10-05T11:11:44+02:00',
            'orderId': '11c4e9cf-f672-409d-a51d-87638eaa86cb',
            'productId': 14501924,
            'size': 1.0,
            'price': 0.0,
            'buysell': 'B',
            'orderTypeId': 2,
            'orderTimeTypeId': 3,
            'stopPrice': 0.0,
            'currentTradedSize': 0,
            'totalTradedSize': 0,
            'type': 'CREATE',
            'status': 'CONFIRMED',
            'last': '2023-10-05T11:11:44+02:00',
            'isActive': False
        },
        {
            'created': '2023-10-05T11:18:45+02:00',
            'orderId': 'f7afe500-3c90-40a5-840c-4781cb1c4bf7',
            'productId': 14501924,
            'size': 1.0,
            'price': 0.0,
            'buysell': 'B',
            'orderTypeId': 3,
            'orderTimeTypeId': 3,
            'stopPrice': 78.4,
            'currentTradedSize': 0,
            'totalTradedSize': 0,
            'type': 'CREATE',
            'status': 'CONFIRMED',
            'last': '2023-10-05T11:18:45+02:00',
            'isActive': True
        }]
        '''

        if to_date == None:
            to_date = dt.datetime.today()
        if from_date == None:
            from_date = to_date - dt.timedelta(days=90)

        orders_payload = {
            'fromDate': from_date.strftime('%d/%m/%Y'),
            'toDate': to_date.strftime('%d/%m/%Y'),
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }

        # max 90 days
        if (to_date - from_date).days > 90:
            raise Exception('The maximum timespan is 90 days')
        
        data = self.__request(DeGiro.__ORDERS_URL, payload=orders_payload, 
                              error_message='Could not get orders.')['data']
        data_not_executed = []
        if not_executed:
            for d in data:
                if d['isActive']:
                    data_not_executed.append(d)
            return data_not_executed
        else:
            return data

    def deleteOrder(self, orderId:str):

        delete_order_params = {
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id,
        }

        return self.__request(DeGiro.__ORDER_URL + orderId + ';jsessionid=' + self.session_id,
                              payload=delete_order_params,
                              request_type=DeGiro.__DELETE_REQUEST,
                              error_message='Could not delete order' + " " + orderId)

    @staticmethod
    def _filtercashfunds(cashfunds:dict) -> list:

        data = []
        for item in cashfunds['cashFunds']['value']:
            if item['value'][2]['value'] != 0:
                data.append(item['value'][1]['value'] + " " + str(item['value'][2]['value']))

        return data

    @staticmethod
    def _filterportfolio(portfolio:dict, filter_zero:bool=False) -> list:

        data = []
        data_non_zero = []
        for item in portfolio['portfolio']['value']:
            positionType = size = price = value = breakEvenPrice = None
            for i in item['value']:
                size = i['value'] if i['name'] == 'size' else size
                positionType = i['value'] if i['name'] == 'positionType' else positionType
                price = i['value'] if i['name'] == 'price' else price
                value = i['value'] if i['name'] == 'value' else value
                breakEvenPrice = i['value'] if i['name'] == 'breakEvenPrice' else breakEvenPrice
            data.append({
                "id": item['id'],
                "positionType": positionType,
                "size": size,
                "price": price,
                "value": value,
                "breakEvenPrice": breakEvenPrice
            })
        if filter_zero:
            for d in data:
                if d['size'] != 0.0:
                    data_non_zero.append(d)
            return data_non_zero
        else:
            return data

    def getData(self, datatype:DataType=DataType.PORTFOLIO, filter_zero:bool=False):

        '''
        portfolio = [
            {'id': '13585545',
            'positionType': 'PRODUCT',
            'size': 0,
            'price': 1.784,
            'value': 0.0,
            'breakEvenPrice': 0},
            {'id': '15694501',
            'positionType': 'CASH',
            'size': 0.0,
            'price': 10043.6833,
            'value': 0.0,
            'breakEvenPrice': 0},
            {'id': 'EUR',
            'positionType': 'CASH',
            'size': -79.25,
            'price': 1,
            'value': -79.25,
            'breakEvenPrice': 0},
            {'id': 'FLATEX_EUR',
            'positionType': 'CASH',
            'size': 1999.99,
            'price': 1,
            'value': 1999.99,
            'breakEvenPrice': 0},
            {'id': '14501924',
            'positionType': 'PRODUCT',
            'size': 1.0,
            'price': 78.0248,
            'value': 78.0248,
            'breakEvenPrice': 78.2505}
        ]
        '''

        data_payload = {
            datatype.value: 0
        }

        if datatype == DataType.CASHFUNDS:
            return self._filtercashfunds(
                self.__request(DeGiro.__DATA_URL + str(self.client_info.account_id) + ';jsessionid=' + self.session_id,
                               payload=data_payload,
                               error_message='Could not get data'))
        elif datatype == DataType.PORTFOLIO:
            return self._filterportfolio(
                self.__request(DeGiro.__DATA_URL + str(self.client_info.account_id) + ';jsessionid=' + self.session_id,
                               payload=data_payload,
                               error_message='Could not get data'), filter_zero)
        else:
            return self.__request(
                DeGiro.__DATA_URL + str(self.client_info.account_id) + ';jsessionid=' + self.session_id,
                payload=data_payload,
                error_message='Could not get data')

    def getQuote(self, product:(dict | Product), interval:str='P50Y') -> dict:
        
        # Get instrument info
        if isinstance(product, str):
            temp = self.productInfo(product)
            vw_id = temp['vwdId']
            vw_type = temp['vwdIdentifierType']
        elif isinstance(product, dict):
            vw_id = product['vwdId']
            vw_type = product['vwdIdentifierType']
        else:
            vw_id = product.props['vwdId']
            vw_type = product.props['vwdIdentifierType']

        price_payload = {
            'requestid': 1,
            'period': interval,
            'series': [f'{vw_type}:{vw_id}'], # 
            'userToken': self.client_token
        }

        return self.__request(DeGiro.__PRICE_DATA_URL, payload=price_payload,
                             error_message='Could not get real time price')['series'][0]

    @staticmethod
    def _parseStart(start:str, resolution:str=None) -> float:

        """Extract the start timestamp of a timeserie.
        Args:
            times (str):
                Combination of `start date` and `resolution` of the serie.
                Example :
                    times = "2021-10-28/P6M"
                    times = "2021-11-03T00:00:00/PT1H"
        Returns:
            float:
                Timestamp of the start date of the serie.
        """

        if '/' in start:
            (start, resolution) = start.rsplit(sep="/", maxsplit=1)
        resolution = resolution.replace('Z', '')

        date_format = ""
        if resolution.startswith("PT"):
            date_format = "%Y-%m-%dT%H:%M:%S"
        else:
            date_format = "%Y-%m-%d"

        start_datetime = dt.datetime.strptime(start, date_format)
        start_timestamp = start_datetime.timestamp()

        return start_timestamp

    @staticmethod
    def _resToSeconds(resolution: str) -> int:
        """Extract the interval of a timeserie.
        Args:
            times (str):
                Combination of `start date` and `resolution` of the serie.
                Example :
                    times = "2021-10-28/P6M"
                    times = "2021-11-03T00:00:00/PT1H"
        Raises:
            AttributeError:
                if the resolution is unknown.
        Returns:
            int:
                Number of seconds in the interval.
        """

        if '/' in resolution:
            (_start, resolution) = resolution.rsplit(sep="/", maxsplit=1)

        resolution = resolution.replace('PT', '').replace('P','')
        if 'S' in resolution:
            return int(resolution[:-1])
        elif 'M' in resolution:
            return int(resolution[:-1]) * 60
        elif 'H' in resolution:
            return int(resolution[:-1]) * 60 * 60
        elif 'D' in resolution:
            return int(resolution[:-1]) * 60 * 60 * 24
        else:
            raise ValueError('Not a valid resolution.')
        
    @staticmethod
    def _serieToDF(serie:dict) -> pd.DataFrame:

        """Converts a timeserie into a DataFrame.
        Only series with the following types can be converted into DataFrame :
        - serie.type == "time"
        - serie.type == "ohlc"
        Beware of series with the following type :
         - serie.type == "object"
        These are not actual timeseries and can't converted into DataFrame.
        Args:
            serie (Chart.Serie):
                The serie to convert.
        Raises:
            AttributeError:
                If the serie.type is incorrect.
        Returns:
            pd.DataFrame: [description]
        """

        columns = []
        if serie['type'] == 'ohlc' and serie['id'].startswith('ohlc:'):
            columns = [
                'timestamp',
                'open',
                'high',
                'low',
                'close',
            ]
        elif serie['type'] == 'time' and serie['id'].startswith('price:'):
            columns = [
                'timestamp',
                'price',
            ]
        elif serie['type'] == 'time' and serie['id'].startswith('volume:'):
            columns = [
                'timestamp',
                'volume',
            ]
        elif serie['type'] == 'object':
            raise AttributeError(f"Not a timeserie, serie['type'] = {serie['type']}")
        else:
            raise AttributeError(f"Unknown serie, serie['type'] = {serie['type']}")
        
        return pd.DataFrame.from_records(serie['data'], columns=columns)
    
    def getCandles(self, product:Product, resolution:str=ResolutionType.D1, 
                   interval:str=IntervalType.Max, df:bool=True) -> dict:
        
        # Get instrument info
        if isinstance(product, str):
            temp = self.productInfo(product)
            vw_id = temp['vwdId']
            vw_type = temp['vwdIdentifierType']
        else:
            vw_id = product.props['vwdId']
            vw_type = product.props['vwdIdentifierType']

        price_payload = {
            'requestid': 1,
            'period': interval.value,
            'resolution': resolution,
            'series': [f'{vw_type}:{vw_id}', f'ohlc:{vw_type}:{vw_id}', f'volume:{vw_type}:{vw_id}'], # 
            'userToken': self.client_token,
            'tz': 'UTC',
            'culture': 'en-US',
        }
        data = self.__request(DeGiro.__PRICE_DATA_URL, payload=price_payload,
                             error_message='Could not get real time price')['series']
        
        if df:
            quote = data[0]['data']
            start = quote['windowFirst']
            dfs = []
            for serie in data:
                if serie['type'] in ["time", "ohlc"]:
                    times = serie['times']
                    start = self._parseStart(start=times)
                    interval = self._resToSeconds(resolution=times)
                    
                    for datapoint in serie['data']:
                        datapoint[0] = start + datapoint[0] * interval

                    dfs.append(self._serieToDF(serie))
                    
            data = pd.merge(dfs[0], dfs[1], left_index=True, right_index=True)
            data = data[[c for c in data.columns if '_y' not in c]]
            data.rename(columns={k: k.replace('_x','') for k in data.columns}, inplace=True)
            # data = pd.merge(dfs[0], dfs[1], on='timestamp')
            data.columns = [c.capitalize() for c in data.columns]
            if 'Timestamp' in data.columns:
                data['DateTime'] = pd.to_datetime(data['Timestamp'], utc=True, unit='s')
        else:
            data = {d['id'].split(':')[0]: d['data'] for d in data}

        return data

    def tradeOrder(self, productId:str, size:int, side:str, orderType:str=Order.Type.MARKET, 
                 timeType:int=Order.Time.GTC, limit=None, stop_loss=None) -> dict:
        
        '''
        {'data': {'orderId': 'f7afe500-3c90-40a5-840c-4781cb1c4bf7'}}
        '''

        place_order_params = {
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id,
        }

        if orderType not in [v for k, v in Order.Type.__dict__.items() if '_' not in k]:
            raise Exception('Invalid order type')

        if timeType not in [v for k, v in Order.Time.__dict__.items() if '_' not in k]:
            raise Exception('Invalid time type')
    
        if side not in [v for k, v in Order.Side.__dict__.items() if '_' not in k]:
            raise Exception('Invalid side for the order.')

        place_order_payload = {
            'buySell': side,
            'orderType': orderType,
            'productId': productId,
            'timeType': timeType,
            'size': int(size),
            'price': limit,
            'stopPrice': stop_loss,
        }

        self.place_check_order_response = self.__request(DeGiro.__PLACE_ORDER_URL + ';jsessionid=' + self.session_id,
                                                    payload=place_order_payload, post_params=place_order_params,
                                                    request_type=DeGiro.__POST_REQUEST,
                                                    error_message='Could not place order')

        self.confirmation_id = self.place_check_order_response['data']['confirmationId']

        return self.__request(DeGiro.__ORDER_URL + self.confirmation_id + ';jsessionid=' + self.session_id,
                       payload=place_order_payload, post_params=place_order_params,
                       request_type=DeGiro.__POST_REQUEST,
                       error_message='Could not confirm order')

    def getStockList(self, indexId:str=None, stockCountryId:str=None):

        stock_list_params = {
            'indexId': indexId,
            'stockCountryId': stockCountryId,
            'offset': 0,
            'limit': None,
            'requireTotal': "true",
            'sortColumns': "name",
            'sortTypes': "asc",
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }

        return self.__request(DeGiro.__GET_STOCKS_URL, payload=stock_list_params, 
                           error_message='Could not get stock list')['products']

    def getAsset(self, assetType:str='stocks', args:dict={}):

        '''
        assetType: str
            stocks, etfs
        '''

        params = {
            'offset': 0,
            'limit': None,
            'requireTotal': "true",
            'sortColumns': "name",
            'sortTypes': "asc",
            'intAccount': self.client_info.account_id,
            'sessionId': self.session_id
        }

        if len(list(args.keys())) > 0:
            params.update(args)

        return self.__request(DeGiro.__GET_URL+assetType, payload=params, 
                           error_message='Could not get stock list')['products']
    




if __name__ == '__main__':

    dg = DeGiro('OneMade','Onemade3680')
    portfolio = dg.getData(DataType.PORTFOLIO, filter_zero=True)

    products = dg.searchProducts('LU1681048804')
    data = dg.getCandles(Product(products[0]), resolution=ResolutionType.D1, 
                                             interval=IntervalType.Y3)
    #products = dg.searchProducts('Amundi Nasdaq-100') # dg.searchProducts('LU1681038243')
    #data = dg.getCandles(Product(products[0]), interval=IntervalType.Max)
    #products = dg.searchProducts('SPY') # dg.searchProducts('IE00B6YX5C33')



