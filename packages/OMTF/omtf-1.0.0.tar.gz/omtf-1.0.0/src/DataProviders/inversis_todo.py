
import requests

url = 'https://www.inversis.com/ice-deed-Vprospeed-This-his-that-were-isted-What'
headers = {
    'Accept': 'application/json; charset=utf-8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Content-Length': '546',
    'Content-Type': 'text/plain; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Cookie': 'cobranding=cbInversiones; JSESSIONID=CgDzyplH5L2weMeWkMllBAxhIRMtazoqPych_ocinKFnN3AM_4J5!-391805515!-1553665814; visid_incap_141033=CZR2XdwpRmqN5k4SDnd/Ydwz4GUAAAAAQUIPAAAAAAA9jPQolXgYWX6clyZjleal; nlbi_141033=9tQCL49hUwpeeR+D6DqBAQAAAAD664jz/P7JIvH5mTOYOf6a; incap_ses_1297_141033=brnqYvpTmQc30HtBqt//Ed0z4GUAAAAAWGg3dnYo/mAl+cFUtnJh4g==; SJID=4B42BF5BE8AA34859E9F5F6A7F6BA029; reese84=3:JzMy58FWMZsJokzJXG5A4A==:/EkzJ2PxKuQiCVUCf4NnKPlFLn6aps15BAnAN070h91g9GQ7e/1ez74yK2YM+i8rZE+MGUjWtgMfDompZyPcVdsE92xla3Vuj9EF5Mv6WUFQoDfo/8mEJQl+A67az9YVNnPlwkE7Xvr5dHxk1fBz3Y5JWYFscx0cUA+vBE085VsY+B/ibYuRUJAeSNanZRHFB4hhRN8tT5bcgzcsI9r1EpxTaokFSjNj1AZfqwgjCvHqz06Ih7ffiL7Zx21YfY6Urtevb/pn1p0bYUqb+32/DLMKMQ1rU8Sfo3GqjKtdbmHeKluUCVzofNU0VOeHaB4eMo1TmJT2tfrgXyaGq3baDl4yTbcp8/jW7l5aQ9nhYZcYx47/J2OGkDbAAfkCwhArJeXBfz/tHx6Lr/wIzHq/8zR1b4w6pBMImNP1S66FJpu3yUoA3PwZd94ehYTvs8CqQANNX1e2oe9TNRvTtWnkXA==:wUT+XFo6US8dUjcJPmCZY0Rloo0b2OTrTd16C+aM1jU=; euCookiesPolicyAcceptance=true; nlbi_141033_2147483392=L1nLH8YbrAQVYlZ86DqBAQAAAADANaogKnt7jK06JtOZrORd',
}
params = {
    'd': 'www.inversis.com'
}
r = requests.post(url=url, data=params, headers=headers)


url = 'https://www.inversis.com/mobile/'
endpoint = '/SvlForwardDelegator'
cotizaciones = '/SvlCotizaciones'

acciones = ['listaMercados', 'cotizacionesValores', 'cotizacionesEtfs', 'cotizacionesOpciones', 'consultaFondos', 'cotizacionesFuturo',
            'cotizacionesWarrants', 'listaMercados', 'comentarioMercados', 'rankingDerivados', 'rankingWarrants']

r = requests.get(url, )