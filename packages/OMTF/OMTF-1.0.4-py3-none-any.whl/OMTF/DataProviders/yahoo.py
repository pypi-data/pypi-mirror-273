
import enum
import datetime as dt

import requests
from bs4 import BeautifulSoup

from .data import DataProvider

class YahooFinance(DataProvider):

    class Method(enum.Enum):
        GET: str = 'GET'
        POST: str = 'POST'
    
    __api_delayed = 'https://query1.finance.yahoo.com/'
    __api = 'https://query2.finance.yahoo.com/'

    def __init__(self, lang:str='es-ES', verbose:bool=False) -> None:

        self.lang: dict = {
            'lang':lang,
            'region':lang.split('-')[-1],
        }
        self.verbose: bool = verbose

    def _request(self, url:str, headers:dict=None, params:dict=None, method:Method=Method.GET) -> requests.Response:

        if headers == None:
            headers = self._random_header()
        else:
            headers = {**self._random_header(), **headers}
            
        if params != None:
            params = {**params, **self.lang}
        
        if method == self.Method.GET:
            return requests.get(url, params=params, headers=headers)
        elif method == self.Method.POST:
            return requests.post(url, data=params, headers=headers)
        else:
            raise ValueError('Not a valid request method.')

    def searchText(self, text:str) -> str: 
        
        url = f'{self.__api}v1/finance/search'
        params = {
            'q':text,
            'quotesCount':'6',
            'newsCount':'2',
            'listsCount':'2',
            'enableFuzzyQuery':'false',
            'quotesQueryId':'tss_match_phrase_query',
            'multiQuoteQueryId':'multi_quote_single_token_query',
            'newsQueryId':'news_cie_vespa',
            'enableCb':'true',
            'enableNavLinks':'true',
            'enableEnhancedTrivialQuery':'true',
            'enableResearchReports':'true',
            'enableCulturalAssets':'true',
            'enableLogoUrl':'true',
            'researchReportsCount':'2'
        }
        
        return self._request(url=url, params=params).json()

    def getCompanyInfo(self, ticker:str, info:list=['assetProfile', 'secFilings']) -> dict:

        url = f'{self.__api}v10/finance/quoteSummary/{ticker}'
        headers = {
            'host': 'query2.finance.yahoo.com',
            'origin': 'https://finance.yahoo.com',
            'cookie': 'A1=d=AQABBDP8ImQCEGphNhsXE3j7s4l9ziK1mJMFEgEBCAF70GX9Zdwr0iMA_eMBAAcILPwiZMBYI28&S=AQAAApVQ27mmHj84pi0oRFohDHI;'
        }
        params = {
            'formatted': 'true', 
            'crumb': 'IHtSUBEG..D', 
            'modules': ','.join(info),
            'corsDomain': 'finance.yahoo.com'
        }

        return self._request(url=url, headers=headers, params=params).json()
    
    def getInsights(self, ticker:str):

        url: str = f'{self.__api_delayed}ws/insights/v3/finance/insights'
        headers = {
            'host': 'query1.finance.yahoo.com',
            'origin': 'https://finance.yahoo.com',
            'cookie': 'A1=d=AQABBDP8ImQCEGphNhsXE3j7s4l9ziK1mJMFEgEBCAF70GX9Zdwr0iMA_eMBAAcILPwiZMBYI28&S=AQAAApVQ27mmHj84pi0oRFohDHI;'
        }

        params: dict = {
            'formatted': True,
            'disableRelatedReports': True,
            'getAllResearchReports': True,
            'reportsCount': 4,
            'ssl': True,
            'symbols': ticker,
        }

        return self._request(url=url, headers=headers, params=params).json()
    
    def getDataAvailable(self) -> list:
        return ['longName', 'shortName', 'regularMarketPrice', 'regularMarketChange', 'regularMarketChangePercent', 
                'messageBoardId', 'marketCap', 'underlyingSymbol', 'underlyingExchangeSymbol', 'headSymbolAsString', 
                'regularMarketVolume', 'uuid', 'regularMarketOpen', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'toCurrency', 
                'fromCurrency', 'toExchange', 'fromExchange', 'corporateActions', 'logoUrl', 'optionsType', 'regularMarketTime',
                'regularMarketSource', 'postMarketTime', 'postMarketPrice', 'postMarketChange', 'postMarketChangePercent', 
                'preMarketTime', 'preMarketPrice', 'preMarketChange', 'preMarketChangePercent', 'summaryProfile', 'financialData',
                'recommendationTrend', 'earnings', 'equityPerformance', 'summaryDetail', 'defaultKeyStatisticst', 'calendarEvents',
                'esgScores', 'price', 'pageViews', 'financialsTemplate']
    
    def getQuote(self, ticker:str, data:list=['longName', 'regularMarketPrice', 'underlyingSymbol', 'fullExchangeName']) -> dict:

        url = f'{self.__api_delayed}v7/finance/quote'
        headers = {
            'host': 'query2.finance.yahoo.com',
            'origin': 'https://finance.yahoo.com',
            'cookie': 'A1=d=AQABBDP8ImQCEGphNhsXE3j7s4l9ziK1mJMFEgEBCAF70GX9Zdwr0iMA_eMBAAcILPwiZMBYI28&S=AQAAApVQ27mmHj84pi0oRFohDHI;'
        }
        params = {
            'formatted': 'true', 
            'crumb': 'IHtSUBEG..D', 
            'symbols': ticker, 
            'fields': ','.join(data), 
            'corsDomain': 'finance.yahoo.com'
        }

        return self._request(url=url, headers=headers, params=params).json()
    
    def getSchedule(self) -> dict:
        url: str = 'https://query1.finance.yahoo.com/v6/finance/markettime?formatted=true&amp;key=finance&amp;lang=en-US&amp;region=US'

    def rcommendationBySymbol(elf, ticker:str):
        url: str = f'https://query1.finance.yahoo.com/v6/finance/recommendationsbysymbol/{ticker}?count=16&amp;fields=&amp;lang=en-US&amp;region=US'

    def getPriceRanges(self) -> list:
        return ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

    def getPrice(self, ticker:str, start:dt.datetime=None, end:dt.datetime=None, interval:str='1d'):
        url: str = 'https://query1.finance.yahoo.com/v7/finance/spark?includePrePost=false&amp;includeTimestamps=false&amp;indicators=close&amp;interval=5m&amp;range=1d&amp;symbols=AAPL&amp;lang=en-US&amp;region=US'
        url: str = f'{self.__api}v8/finance/chart/{ticker}'

        headers = {
            'host': 'query2.finance.yahoo.com',
            'origin': 'https://finance.yahoo.com',
            'cookie': 'A1=d=AQABBDP8ImQCEGphNhsXE3j7s4l9ziK1mJMFEgEBCAF70GX9Zdwr0iMA_eMBAAcILPwiZMBYI28&S=AQAAApVQ27mmHj84pi0oRFohDHI;'
        }
        params: dict = {
            'interval': interval,
            'includePrePost': True,
            'events': 'div|split|earn',
        }
        if start != None:
            params['period1'] = start.timestamp()
        if end != None:
            params['period2'] = end.timestamp()
        
        return self._request(url=url, headers=headers, params=params).json()

    def getAvailableFinancials(self) -> list:
        return ['incomeStatementHistory', 'cashflowStatementHistory', 'balanceSheetHistory', 'incomeStatementHistoryQuarterly', 'cashflowStatementHistoryQuarterly', 'balanceSheetHistoryQuarterly']
    
    def getFinancials(self, ticker:str, financials:list=['incomeStatementHistory', 'incomeStatementHistoryQuarterly']) -> dict:

        url = f'{self.__api}v10/finance/quoteSummary/{ticker}'
        headers = {
            'host': 'query2.finance.yahoo.com',
            'origin': 'https://finance.yahoo.com',
            'cookie': 'A1=d=AQABBDP8ImQCEGphNhsXE3j7s4l9ziK1mJMFEgEBCAF70GX9Zdwr0iMA_eMBAAcILPwiZMBYI28&S=AQAAApVQ27mmHj84pi0oRFohDHI;'
        }
        params = {
            'formatted': True,
            'crumb': 'IHtSUBEG..D',
            'modules': ','.join(financials),
            'corsDomain': 'finance.yahoo.com',
        }
        
        return self._request(url=url, headers=headers, params=params).json()
    
    def getAvailableFundamentals(self) -> list:

        return ['annualTreasurySharesNumber', 'trailingTreasurySharesNumber', 'annualPreferredSharesNumber', 'trailingPreferredSharesNumber', 'annualOrdinarySharesNumber', 'trailingOrdinarySharesNumber', 'annualShareIssued', 'trailingShareIssued', 'annualNetDebt', 'trailingNetDebt', 'annualTotalDebt', 'trailingTotalDebt', 'annualTangibleBookValue', 'trailingTangibleBookValue', 'annualInvestedCapital', 'trailingInvestedCapital', 'annualWorkingCapital', 'trailingWorkingCapital', 'annualNetTangibleAssets', 'trailingNetTangibleAssets', 'annualCapitalLeaseObligations', 'trailingCapitalLeaseObligations', 'annualCommonStockEquity', 'trailingCommonStockEquity', 'annualPreferredStockEquity', 'trailingPreferredStockEquity', 'annualTotalCapitalization', 'trailingTotalCapitalization', 'annualTotalEquityGrossMinorityInterest', 'trailingTotalEquityGrossMinorityInterest', 'annualMinorityInterest', 'trailingMinorityInterest', 'annualStockholdersEquity', 'trailingStockholdersEquity', 'annualOtherEquityInterest', 'trailingOtherEquityInterest', 'annualGainsLossesNotAffectingRetainedEarnings', 'trailingGainsLossesNotAffectingRetainedEarnings', 'annualOtherEquityAdjustments', 'trailingOtherEquityAdjustments', 'annualFixedAssetsRevaluationReserve', 'trailingFixedAssetsRevaluationReserve', 'annualForeignCurrencyTranslationAdjustments', 'trailingForeignCurrencyTranslationAdjustments', 'annualMinimumPensionLiabilities', 'trailingMinimumPensionLiabilities', 'annualUnrealizedGainLoss', 'trailingUnrealizedGainLoss', 'annualTreasuryStock', 'trailingTreasuryStock', 'annualRetainedEarnings', 'trailingRetainedEarnings', 'annualAdditionalPaidInCapital', 'trailingAdditionalPaidInCapital', 'annualCapitalStock', 'trailingCapitalStock', 'annualOtherCapitalStock', 'trailingOtherCapitalStock', 'annualCommonStock', 'trailingCommonStock', 'annualPreferredStock', 'trailingPreferredStock', 'annualTotalPartnershipCapital', 'trailingTotalPartnershipCapital', 'annualGeneralPartnershipCapital', 'trailingGeneralPartnershipCapital', 'annualLimitedPartnershipCapital', 'trailingLimitedPartnershipCapital', 'annualTotalLiabilitiesNetMinorityInterest', 'trailingTotalLiabilitiesNetMinorityInterest', 'annualTotalNonCurrentLiabilitiesNetMinorityInterest', 'trailingTotalNonCurrentLiabilitiesNetMinorityInterest', 'annualOtherNonCurrentLiabilities', 'trailingOtherNonCurrentLiabilities', 'annualLiabilitiesHeldforSaleNonCurrent', 'trailingLiabilitiesHeldforSaleNonCurrent', 'annualRestrictedCommonStock', 'trailingRestrictedCommonStock', 'annualPreferredSecuritiesOutsideStockEquity', 'trailingPreferredSecuritiesOutsideStockEquity', 'annualDerivativeProductLiabilities', 'trailingDerivativeProductLiabilities', 'annualEmployeeBenefits', 'trailingEmployeeBenefits', 'annualNonCurrentPensionAndOtherPostretirementBenefitPlans', 'trailingNonCurrentPensionAndOtherPostretirementBenefitPlans', 'annualNonCurrentAccruedExpenses', 'trailingNonCurrentAccruedExpenses', 'annualDuetoRelatedPartiesNonCurrent', 'trailingDuetoRelatedPartiesNonCurrent', 'annualTradeandOtherPayablesNonCurrent', 'trailingTradeandOtherPayablesNonCurrent', 'annualNonCurrentDeferredLiabilities', 'trailingNonCurrentDeferredLiabilities', 'annualNonCurrentDeferredRevenue', 'trailingNonCurrentDeferredRevenue', 'annualNonCurrentDeferredTaxesLiabilities', 'trailingNonCurrentDeferredTaxesLiabilities', 'annualLongTermDebtAndCapitalLeaseObligation', 'trailingLongTermDebtAndCapitalLeaseObligation', 'annualLongTermCapitalLeaseObligation', 'trailingLongTermCapitalLeaseObligation', 'annualLongTermDebt', 'trailingLongTermDebt', 'annualLongTermProvisions', 'trailingLongTermProvisions', 'annualCurrentLiabilities', 'trailingCurrentLiabilities', 'annualOtherCurrentLiabilities', 'trailingOtherCurrentLiabilities', 'annualCurrentDeferredLiabilities', 'trailingCurrentDeferredLiabilities', 'annualCurrentDeferredRevenue', 'trailingCurrentDeferredRevenue', 'annualCurrentDeferredTaxesLiabilities', 'trailingCurrentDeferredTaxesLiabilities', 'annualCurrentDebtAndCapitalLeaseObligation', 'trailingCurrentDebtAndCapitalLeaseObligation', 'annualCurrentCapitalLeaseObligation', 'trailingCurrentCapitalLeaseObligation', 'annualCurrentDebt', 'trailingCurrentDebt', 'annualOtherCurrentBorrowings', 'trailingOtherCurrentBorrowings', 'annualLineOfCredit', 'trailingLineOfCredit', 'annualCommercialPaper', 'trailingCommercialPaper', 'annualCurrentNotesPayable', 'trailingCurrentNotesPayable', 'annualPensionandOtherPostRetirementBenefitPlansCurrent', 'trailingPensionandOtherPostRetirementBenefitPlansCurrent', 'annualCurrentProvisions', 'trailingCurrentProvisions', 'annualPayablesAndAccruedExpenses', 'trailingPayablesAndAccruedExpenses', 'annualCurrentAccruedExpenses', 'trailingCurrentAccruedExpenses', 'annualInterestPayable', 'trailingInterestPayable', 'annualPayables', 'trailingPayables', 'annualOtherPayable', 'trailingOtherPayable', 'annualDuetoRelatedPartiesCurrent', 'trailingDuetoRelatedPartiesCurrent', 'annualDividendsPayable', 'trailingDividendsPayable', 'annualTotalTaxPayable', 'trailingTotalTaxPayable', 'annualIncomeTaxPayable', 'trailingIncomeTaxPayable', 'annualAccountsPayable', 'trailingAccountsPayable', 'annualTotalAssets', 'trailingTotalAssets', 'annualTotalNonCurrentAssets', 'trailingTotalNonCurrentAssets', 'annualOtherNonCurrentAssets', 'trailingOtherNonCurrentAssets', 'annualDefinedPensionBenefit', 'trailingDefinedPensionBenefit', 'annualNonCurrentPrepaidAssets', 'trailingNonCurrentPrepaidAssets', 'annualNonCurrentDeferredAssets', 'trailingNonCurrentDeferredAssets', 'annualNonCurrentDeferredTaxesAssets', 'trailingNonCurrentDeferredTaxesAssets', 'annualDuefromRelatedPartiesNonCurrent', 'trailingDuefromRelatedPartiesNonCurrent', 'annualNonCurrentNoteReceivables', 'trailingNonCurrentNoteReceivables', 'annualNonCurrentAccountsReceivable', 'trailingNonCurrentAccountsReceivable', 'annualFinancialAssets', 'trailingFinancialAssets', 'annualInvestmentsAndAdvances', 'trailingInvestmentsAndAdvances', 'annualOtherInvestments', 'trailingOtherInvestments', 'annualInvestmentinFinancialAssets', 'trailingInvestmentinFinancialAssets', 'annualHeldToMaturitySecurities', 'trailingHeldToMaturitySecurities', 'annualAvailableForSaleSecurities', 'trailingAvailableForSaleSecurities', 'annualFinancialAssetsDesignatedasFairValueThroughProfitorLossTotal', 'trailingFinancialAssetsDesignatedasFairValueThroughProfitorLossTotal', 'annualTradingSecurities', 'trailingTradingSecurities', 'annualLongTermEquityInvestment', 'trailingLongTermEquityInvestment', 'annualInvestmentsinJointVenturesatCost', 'trailingInvestmentsinJointVenturesatCost', 'annualInvestmentsInOtherVenturesUnderEquityMethod', 'trailingInvestmentsInOtherVenturesUnderEquityMethod', 'annualInvestmentsinAssociatesatCost', 'trailingInvestmentsinAssociatesatCost', 'annualInvestmentsinSubsidiariesatCost', 'trailingInvestmentsinSubsidiariesatCost', 'annualInvestmentProperties', 'trailingInvestmentProperties', 'annualGoodwillAndOtherIntangibleAssets', 'trailingGoodwillAndOtherIntangibleAssets', 'annualOtherIntangibleAssets', 'trailingOtherIntangibleAssets', 'annualGoodwill', 'trailingGoodwill', 'annualNetPPE', 'trailingNetPPE', 'annualAccumulatedDepreciation', 'trailingAccumulatedDepreciation', 'annualGrossPPE', 'trailingGrossPPE', 'annualLeases', 'trailingLeases', 'annualConstructionInProgress', 'trailingConstructionInProgress', 'annualOtherProperties', 'trailingOtherProperties', 'annualMachineryFurnitureEquipment', 'trailingMachineryFurnitureEquipment', 'annualBuildingsAndImprovements', 'trailingBuildingsAndImprovements', 'annualLandAndImprovements', 'trailingLandAndImprovements', 'annualProperties', 'trailingProperties', 'annualCurrentAssets', 'trailingCurrentAssets', 'annualOtherCurrentAssets', 'trailingOtherCurrentAssets', 'annualHedgingAssetsCurrent', 'trailingHedgingAssetsCurrent', 'annualAssetsHeldForSaleCurrent', 'trailingAssetsHeldForSaleCurrent', 'annualCurrentDeferredAssets', 'trailingCurrentDeferredAssets', 'annualCurrentDeferredTaxesAssets', 'trailingCurrentDeferredTaxesAssets', 'annualRestrictedCash', 'trailingRestrictedCash', 'annualPrepaidAssets', 'trailingPrepaidAssets', 'annualInventory', 'trailingInventory', 'annualInventoriesAdjustmentsAllowances', 'trailingInventoriesAdjustmentsAllowances', 'annualOtherInventories', 'trailingOtherInventories', 'annualFinishedGoods', 'trailingFinishedGoods', 'annualWorkInProcess', 'trailingWorkInProcess', 'annualRawMaterials', 'trailingRawMaterials', 'annualReceivables', 'trailingReceivables', 'annualReceivablesAdjustmentsAllowances', 'trailingReceivablesAdjustmentsAllowances', 'annualOtherReceivables', 'trailingOtherReceivables', 'annualDuefromRelatedPartiesCurrent', 'trailingDuefromRelatedPartiesCurrent', 'annualTaxesReceivable', 'trailingTaxesReceivable', 'annualAccruedInterestReceivable', 'trailingAccruedInterestReceivable', 'annualNotesReceivable', 'trailingNotesReceivable', 'annualLoansReceivable', 'trailingLoansReceivable', 'annualAccountsReceivable', 'trailingAccountsReceivable', 'annualAllowanceForDoubtfulAccountsReceivable', 'trailingAllowanceForDoubtfulAccountsReceivable', 'annualGrossAccountsReceivable', 'trailingGrossAccountsReceivable', 'annualCashCashEquivalentsAndShortTermInvestments', 'trailingCashCashEquivalentsAndShortTermInvestments', 'annualOtherShortTermInvestments', 'trailingOtherShortTermInvestments', 'annualCashAndCashEquivalents', 'trailingCashAndCashEquivalents', 'annualCashEquivalents', 'trailingCashEquivalents', 'annualCashFinancial', 'trailingCashFinancial']

    def getFundamentalTimeseries(self, ticker:str, fundamentals:list=['annualTotalAssets', 'annualTotalLiabilitiesNetMinorityInterest']) -> dict:
        
        url = f'{self.__api_delayed}ws/fundamentals-timeseries/v1/finance/timeseries/{ticker}'

        params = {
            'symbol': ticker, 
            'padTimeSeries': 'true', 
            'type': ','.join(fundamentals),
            'merge': 'false',
            'period1': '493590046',
            'period2': '1708081300',
            'corsDomain': 'finance.yahoo.com'
        }
        headers = {
            'host': 'query2.finance.yahoo.com',
            'origin': 'https://finance.yahoo.com',
            'cookie': 'A1=d=AQABBDP8ImQCEGphNhsXE3j7s4l9ziK1mJMFEgEBCAF70GX9Zdwr0iMA_eMBAAcILPwiZMBYI28&S=AQAAApVQ27mmHj84pi0oRFohDHI;'
        }
        
        return self._request(url=url, headers=headers, params=params).json()

    def getKPI(self, ticker:str) -> dict:

        url = f'https://finance.yahoo.com/quote/{ticker}?.tsrc=fin-srch'
        html = BeautifulSoup(self._request(url=url).content, 'html.parser')

        return {
            'Logotype': '',
            'BPA': html.find('td', attrs={'data-test': 'EPS_RATIO-value'}).get_text(), # EPS
            'PER': html.find('td', attrs={'data-test': 'PE_RATIO-value'}).get_text(),
            'BETA': html.find('td', attrs={'data-test': 'BETA_5Y-value'}).get_text(),
        }

    def getEconomicCalendar(self):

        url: str = 'https://query1.finance.yahoo.com/ws/screeners/v1/finance/calendar-events?countPerDay=100&economicEventsHighImportanceOnly=true&economicEventsRegionFilter=&endDate=1715184000000&modules=economicEvents&startDate=1713283200000&lang=en-US&region=US'

# checKey = lambda k, dic: (dic[k] if k in dic else None) if dic != None else None
def checKey(keys:(int | str | list[str]), dic:dict):

    if isinstance(keys, list):
        value: dict = dic
        for key in keys:
            if key in value:
                value = value[key]
            else:
                value = None
                break

        return value
    else:
        return (dic[keys] if keys in dic else None) if dic != None else None
    
if __name__ == '__main__':
    
    text: str = 'aapl'
    ys = YahooFinance(verbose=True)
    ticker: str = ys.searchText(text)['quotes'][0]['symbol']
    # result: dict = ys.getKPI(ticker=ticker)
    info: dict = ys.getCompanyInfo(ticker=ticker, info=['assetProfile'])['quoteSummary']['result'][0]['assetProfile']
    quote: dict = ys.getQuote(ticker=ticker)['quoteResponse']['result'][0]
    finance: dict = ys.getFinancials(ticker=ticker, financials=ys.getDataAvailable())['quoteSummary']['result'][0]
    balance_sheet: list = ys.getFundamentalTimeseries(ticker=ticker, 
        fundamentals=['annualTotalAssets', 'annualTotalLiabilitiesNetMinorityInterest'])['timeseries']['result']
    balance_sheet: list = {k: [i for i in v if i != None] for d in balance_sheet if len(d.keys()) > 1 \
                           for k, v in d.items() if k not in ['meta', 'timestamp']}
    insights: dict = ys.getInsights(ticker=ticker)['finance']['result'][0]
    price_raw: dict = ys.getPrice(ticker=ticker, interval='1m')['chart']['result'][0]
    trading_periods = {
        'pre': {'start': dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['pre']['start']).time(),   
                'end':dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['pre']['end']).time()},
        'regular': {'start': dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['regular']['start']).time(),   
                'end':dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['regular']['end']).time()},
        'post': {'start': dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['post']['start']).time(),   
                'end':dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['post']['end']).time()}
    }
    def checkDateSession(date:dt.datetime, trading_periods:dict):   
        for session, v in trading_periods.items():
            if v['start'] <= date.time() and date.time() < v['end']:
                return session
        return None
    data: list = [{**{'date': d}, 
                   **{k: v[i] for k, v in price_raw['indicators']['quote'][0].items()}, 
                   **{'session':checkDateSession(d, trading_periods)}} \
                  for i, d in enumerate([dt.datetime.fromtimestamp(date) for date in price_raw['timestamp']])]
    data = [{**{'date': d}, **{k: v[i] for k, v in price_raw['indicators']['quote'][0].items()}} \
    for i, d in enumerate([dt.datetime.fromtimestamp(date) for date in price_raw['timestamp']])]
    
    result: dict = {
        'Ticker': ticker,
        'Company': checKey('longName', quote),
        'Exchange': checKey('fullExchangeName', quote),
        'Type': checKey('quoteType', quote),
        'TimeZone': checKey('exchangeTimezoneName', quote),
        'Sector': checKey('sector', info),
        'Sub-Sector': checKey('industry', info),
        'Employees': checKey('fullTimeEmployees', info),
        'Description': checKey('longBusinessSummary', info),
        'Address': checKey('address1', info),
        'City': checKey('city', info),
        'ZIP': checKey('zip', info),
        'Country': checKey('country', info),
        'Phone': checKey('phone', info),
        'Website': checKey('website', info),
        'Logotype': '',
        'IPO': dt.datetime.fromtimestamp(checKey('firstTradeDate', price_raw)).strftime('%Y-%m-%d') 
                if checKey('firstTradeDate', price_raw) else None,
        'Price': checKey(['price', 'regularMarketPrice', 'raw'], finance),
        'Volume': checKey(['price', 'regularMarketVolume', 'raw'], finance),
        'EPS': checKey(['financialData', 'revenuePerShare', 'raw'], finance),
        'PER': checKey(['summaryDetail', 'forwardPE', 'raw'], finance),
        'BETA': checKey(['summaryDetail', 'beta', 'raw'], finance),
        'dividend': checKey(['summaryDetail', 'dividendYield', 'raw'], finance),
        'AvgVolume': checKey(['summaryDetail', 'averageVolume', 'raw'], finance),
        'earningsDate': checKey(['earnings','earningsChart','earningsDate'], finance)[0]['fmt'],
        'Assets': checKey('annualTotalAssets', balance_sheet)[-1]['reportedValue']['fmt'],
        'Liabilities': checKey('annualTotalLiabilitiesNetMinorityInterest', balance_sheet)[-1]['reportedValue']['fmt'],
        'SEC': checKey('secReports', insights),
        'bullishStories': checKey(['upsell', 'msBullishSummary'], insights),
        'bearishStories': checKey(['upsell', 'msBearishSummary'], insights),
        'candles': data
    }
    
    if checKey(['earnings', 'earningsChart'], finance):
        result['earnings'] = [{'date':checKey('date', e), 'actual':checKey(['actual', 'raw'], e), 'estimate':checKey(['estimate', 'raw'], e)} \
                     for e in  checKey(['earnings', 'earningsChart', 'quarterly'], finance)] + \
                    [{'date': f"{checKey(['earnings','earningsChart','currentQuarterEstimateDate'], finance)}{checKey(['earnings','earningsChart','currentQuarterEstimateYear'], finance)}",
                      'actual': None, 'estimate': checKey(['earnings','earningsChart','currentQuarterEstimate','raw'], finance)}]
    else:
        result['earnings'] = None
        
    if checKey('companyOfficers', info):
        result['officers'] = [{k: (o[k] if k in o else None) for k in ['name', 'age', 'title', 'yearBorn']} for o in checKey('companyOfficers', info)]
    else:
        result['officers'] = None

    if checKey(['incomeStatementHistoryQuarterly', 'incomeStatementHistory'],finance):
        result['Revenue'] = {'TTM': sum([checKey(['totalRevenue', 'raw'], i) for i in checKey(['incomeStatementHistoryQuarterly', 'incomeStatementHistory'],finance)]), 
                            'Last':checKey(['incomeStatementHistory','incomeStatementHistory'], finance)[0]['totalRevenue']['fmt']}
        result['Net-Earnings'] = {'TTM':sum([checKey(['netIncome','raw'], i) for i in checKey(['incomeStatementHistoryQuarterly','incomeStatementHistory'], finance)]), 
                            'Last':checKey(['incomeStatementHistory','incomeStatementHistory'], finance)[0]['netIncome']['fmt']}
    else:
        result['Revenue'] = None
        result['Net-Earnings'] = None