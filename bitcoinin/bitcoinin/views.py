from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
###########################################################
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
###########################################################
from django.utils.timezone import get_current_timezone
##########################################################
from django.db.models import Count
from django.db.models import Sum
from django.db.models import F
##########################################################
# ALLOW REST_FRAMEWORK LOGIN
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm
from django.contrib import messages

# BitcoinIn
from pycoingecko import CoinGeckoAPI
import time
import datetime
import pandas as pd

# ------------------------  START LOGIN ------------------


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(
                request, 'Nueva cuenta registrada satisfactoriamente.')
            return redirect('signup')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

# ------------------------  END LOGIN ------------------

# ------------------------ START INDEX ------------------


#import yfinance as yf

one_cuatrillion = 1000000000000000
one_trillion = 1000000000000
one_billion = 1000000000
one_million = 1000000
one_thousand = 1000


def index_view(request):

    index_html = '1'

    current_time = time.localtime()
    now1 = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    year_ago = datetime.datetime.utcnow() - datetime.timedelta(days=365)

    # Client api crypto
    cg = CoinGeckoAPI()
    json_response = cg.get_coin_market_chart_by_id('bitcoin', 'USD', '1')

    myindex_last = -1
    myindex_first = 0

    # Prices of BTC
    first_price_bitcoin = round(json_response['prices'][myindex_first][1], 2)
    last_price_bitcoin = round(json_response['prices'][myindex_last][1], 2)

    # Symbol +/-
    var_price_bitcoin = last_price_bitcoin-first_price_bitcoin
    if var_price_bitcoin > 0:
        symbol_price_bitcoin = "+"
    else:
        symbol_price_bitcoin = "-"

    # Percentajes of variation
    var_price_bitcoin_abs = round(abs(var_price_bitcoin), 2)
    var_price_bitcoin_percentage = abs(
        round(var_price_bitcoin_abs/first_price_bitcoin*100, 2))

    # Data price of the last 24h
    print("len prices: {}".format(len(json_response['prices'])))

    # Generate json to send to the frontend also Get max and min
    data_chart_price_bitcoin, max_btc, min_btc = generate_chart_data(
        json_response['prices'])
    print("MAX: ", max_btc, " MIN: ", min_btc)

    # Market cap of the last 24h

    first_marketcap_bitcoin = round(
        json_response['market_caps'][myindex_first][1]/one_billion, 2)
    last_marketcap_bitcoin = round(
        json_response['market_caps'][myindex_last][1]/one_billion, 2)

    # Symbol +/-
    var_marketcap_bitcoin = last_marketcap_bitcoin-first_marketcap_bitcoin
    if var_marketcap_bitcoin > 0:
        symbol_var_marketcap_bitcoin = "+"
    else:
        symbol_var_marketcap_bitcoin = "-"

    # Percentajes of variation
    var_marketcap_bitcoin_abs = round(abs(var_marketcap_bitcoin), 2)
    var_marketcap_bitcoin_percentage = abs(
        round(var_marketcap_bitcoin_abs/first_marketcap_bitcoin*100, 2))
    var_marketcap_bitcoin_percentage_with_symbol = round(
        var_marketcap_bitcoin_abs/first_marketcap_bitcoin*100, 2)

    data_chart_marketcap_bitcoin, max_btc_marketcap, min_btc_marketcap = generate_chart_data(
        json_response['market_caps'])
    max_btc_marketcap = max_btc_marketcap/one_billion
    min_btc_marketcap = min_btc_marketcap/one_billion

    # Volume of the last 24h

    first_volume_bitcoin = round(
        json_response['total_volumes'][myindex_first][1]/one_billion, 2)
    last_volume_bitcoin = round(
        json_response['total_volumes'][myindex_last][1]/one_billion, 2)

    # Symbol +/-
    var_volume_bitcoin = last_volume_bitcoin-first_volume_bitcoin
    if var_volume_bitcoin > 0:
        symbol_var_volume_bitcoin = "+"
    else:
        symbol_var_volume_bitcoin = "-"

    # Percentajes of variation
    var_volume_bitcoin_abs = round(abs(var_volume_bitcoin), 2)
    var_volume_bitcoin_percentage = abs(
        round(var_volume_bitcoin_abs/first_volume_bitcoin*100, 2))

    data_chart_volume_bitcoin, max_btc_volume, min_btc_volume = generate_chart_data(
        json_response['total_volumes'])
    max_btc_volume = max_btc_volume/one_billion
    min_btc_volume = min_btc_volume/one_billion

    # Year comparison
    d = year_ago.strftime('%d-%m-%Y')
    json_year_response = cg.get_coin_history_by_id('bitcoin', d)
    year_price = round(
        json_year_response['market_data']['current_price']['usd'], 2)
    year_marketcap = round(
        json_year_response['market_data']['market_cap']['usd']/one_billion, 2)
    year_volume = round(
        json_year_response['market_data']['total_volume']['usd']/one_billion, 2)

    print(year_price, year_marketcap, year_volume)

    # price
    var_year_ago = (last_price_bitcoin-year_price)/year_price*100
    var_year_ago_abs = abs(round(var_year_ago, 2))
    if var_year_ago > 0:
        symbol_var_price_year_ago = True
    else:
        symbol_var_price_year_ago = False

    # marketcap
    var_year_ago_marketcap = (
        last_marketcap_bitcoin-year_marketcap)/year_marketcap*100
    var_year_ago_marketcap_abs = abs(round(var_year_ago_marketcap, 2))
    if var_year_ago_marketcap > 0:
        symbol_var_markecap_year_ago = True
    else:
        symbol_var_marketcap_year_ago = False

    # volume
    var_year_ago_volume = (last_volume_bitcoin-year_volume)/year_volume*100
    var_year_ago_volume_abs = abs(round(var_year_ago_volume, 2))
    if var_year_ago_volume > 0:
        symbol_var_volume_year_ago = True
    else:
        symbol_var_volume_year_ago = False

    print("vars:", var_year_ago_marketcap_abs, " ", var_year_ago_volume_abs)

    return render(request, 'index/index.html', locals())


def bitcoinasacompany_view(request):

    index_html = '2'

    current_time = time.localtime()
    now1 = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    year_ago = datetime.datetime.utcnow() - datetime.timedelta(days=365)

    # Client api crypto
    cg = CoinGeckoAPI()
    json_response = cg.get_coin_market_chart_by_id('bitcoin', 'USD', '1')

    myindex_last = -1
    myindex_first = 0

    # Prices of BTC
    first_price_bitcoin = round(json_response['prices'][myindex_first][1], 2)
    last_price_bitcoin = round(json_response['prices'][myindex_last][1], 2)

    # Symbol +/-
    var_price_bitcoin = last_price_bitcoin-first_price_bitcoin

    # Data price of the last 24h
    print("len prices: {}".format(len(json_response['prices'])))

    # Market cap of the last 24h

    first_marketcap_bitcoin = round(
        json_response['market_caps'][myindex_first][1]/one_billion, 2)
    last_marketcap_bitcoin = round(
        json_response['market_caps'][myindex_last][1]/one_billion, 2)

    # Symbol +/-
    var_marketcap_bitcoin = last_marketcap_bitcoin-first_marketcap_bitcoin

    # Percentajes of variation
    var_marketcap_bitcoin_abs = round(abs(var_marketcap_bitcoin), 2)
    var_marketcap_bitcoin_percentage = abs(
        round(var_marketcap_bitcoin_abs/first_marketcap_bitcoin*100, 2))
    var_marketcap_bitcoin_percentage_with_symbol = round(
        var_marketcap_bitcoin_abs/first_marketcap_bitcoin*100, 2)

    # BITCOIN AS A COMPANY
    print("BTC AS COMPANY: ", last_price_bitcoin,
          last_marketcap_bitcoin, var_price_bitcoin)
    table_company = get_largest_companies_by_market_cap_and_include_bitcoin(
        last_price_bitcoin, last_marketcap_bitcoin, var_marketcap_bitcoin_percentage_with_symbol)
    table_company = table_company

    return render(request, 'index/bitcoinasacompany.html', locals())


def bitcoinasfiat_view(request):

    index_html = '3'

    current_time = time.localtime()
    now1 = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    year_ago = datetime.datetime.utcnow() - datetime.timedelta(days=365)

    # Client api crypto
    cg = CoinGeckoAPI()
    json_response = cg.get_coin_market_chart_by_id('bitcoin', 'USD', '1')

    myindex_last = -1
    myindex_first = 0

    # Prices of BTC
    first_price_bitcoin = round(json_response['prices'][myindex_first][1], 2)
    last_price_bitcoin = round(json_response['prices'][myindex_last][1], 2)

    # Symbol +/-
    var_price_bitcoin = last_price_bitcoin-first_price_bitcoin

    # Data price of the last 24h
    print("len prices: {}".format(len(json_response['prices'])))

    # Market cap of the last 24h

    first_marketcap_bitcoin = round(
        json_response['market_caps'][myindex_first][1]/one_billion, 2)
    last_marketcap_bitcoin = round(
        json_response['market_caps'][myindex_last][1]/one_billion, 2)

    # BITCOIN AS A FIAT
    print("BTC AS FIAT: ", last_price_bitcoin,
          last_marketcap_bitcoin, var_price_bitcoin)
    table_company = get_fiat_currencies_by_market_cap_and_include_bitcoin(
        last_price_bitcoin, last_marketcap_bitcoin)
    table_company = table_company

    return render(request, 'index/bitcoinasfiat.html', locals())


def bitcoinascrypto_view(request):


    index_html = '4'

    current_time = time.localtime()
    now1 = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    year_ago = datetime.datetime.utcnow() - datetime.timedelta(days=365)

    data=pd.read_html('https://coinranking.com/')

    table_company =data[0].dropna()

    # data[['C','Cryptocurrency']]=data['Cryptocurrency'].str.split(" ",expand=True) 


    return render(request, 'index/bitcoinascrypto.html', locals())


def bitcoinascommodity_view(request):

    index_html = '5'

    current_time = time.localtime()
    now1 = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    year_ago = datetime.datetime.utcnow() - datetime.timedelta(days=365)


    return render(request, 'index/bitcoinascommodity.html', locals())

# -------------------------- END INDEX -------------------


def generate_chart_data(json_response_sub):

    data_chart_price_bitcoin = ""
    max_btc = 0
    min_btc = 10000000

    for data in json_response_sub:
        temp = {"meta": "0", "value": "0"}
        temp["meta"] = str(datetime.datetime.fromtimestamp(
            data[0] / 1e3))[:-7]  # delete miliseconds https://stackoverflow.com/questions/9744775/how-to-convert-integer-timestamp-to-python-datetime
        temp["value"] = str(int(float(data[1])))

        data_chart_price_bitcoin += '{temp},'.format(temp=temp)

        temp = int(float(data[1]))
        if max_btc < temp:
            max_btc = temp
        if min_btc > temp:
            min_btc = temp

    data_chart_price_bitcoin = data_chart_price_bitcoin.replace("'", '"')[
        :-1]  # delete final comma

    return data_chart_price_bitcoin, max_btc, min_btc


def get_largest_companies_by_market_cap_and_include_bitcoin(last_price_bitcoin, last_marketcap_bitcoin, var_price_bitcoin):
    data = pd.read_html('https://companiesmarketcap.com/', encoding='utf-8')
    bitcoin_allocated = 0
    data = data[0]  # wrapped
    for i, row in data.iterrows():
        # Clean the data
        mc = float(row['Market Cap'][1:-1])  # delete $ and B or T
        if row['Market Cap'].__contains__("B"):
            total_mc = mc*one_billion
        elif row['Market Cap'].__contains__("T"):
            total_mc = mc*one_trillion
        # print(total_mc)

        # Compare to BTC and include
        if last_marketcap_bitcoin*one_billion > total_mc and bitcoin_allocated == 0:
            bitcoin_allocated = 1
            print("BTC! HERE")
            data_up = data[:i]
            row_btc = pd.DataFrame([['¡BTC!',
                                     "BITCOIN",
                                     '${} B'.format(last_marketcap_bitcoin),
                                     '${}'.format(last_price_bitcoin),
                                     '{}%'.format(var_price_bitcoin),
                                     '-',
                                     'Free World']], columns=['Rank',
                                                              'Name',
                                                              'Market Cap',
                                                              'Price',
                                                              'Today',
                                                              'Price (30 days)',
                                                              'Country'])
            data_down = data[i:]
            frames = [data_up, row_btc, data_down]
            df = pd.concat(frames, sort=False)
            df2 = df[['Rank', 'Name', 'Market Cap', 'Price', 'Today', 'Country']]

    return df2


def get_fiat_currencies_by_market_cap_and_include_bitcoin(last_price_bitcoin, last_marketcap_bitcoin):

    data = pd.read_html('https://fiatmarketcap.com/', encoding='utf-8')
    bitcoin_allocated = 0
    data2 = data[0]  # wrapped
    # print(data2)

    # for idx, row in data2.iterrows():

    #     mc = float(row['Market Cap'][:-4].replace(',', ''))

    #     mc = mc*last_price_bitcoin

    #     if mc in range(one_million, one_billion-1):
    #         mc = mc/one_million
    #         units = " M"
    #     elif mc in range(one_billion, one_trillion-1):
    #         mc = mc/one_billion
    #         units = " B"
    #     elif mc in range(one_trillion, one_cuatrillion-1):
    #         mc = mc/one_trillion
    #         units = " T"
    #     mc_string = str(round(mc, 2))+units

    #     data2.loc[idx, 'Market Cap 2'] = mc_string

    #     # Compare to BTC and include
    #     if last_marketcap_bitcoin*one_billion > mc and bitcoin_allocated == 0:
    #         bitcoin_allocated = 1
    #         print("BTC!")

            # ALREADY LISTED

            # data_up = data[:i]
            # row_btc = pd.DataFrame([['¡BTC!',
            #                          "Free World",
            #                          '${} B'.format(last_marketcap_bitcoin),
            #                          '${}'.format(last_price_bitcoin),
            #                          '{}%'.format(var_price_bitcoin),
            #                          '-']], columns=['#',
            #                                                   'Currency',
            #                                                   'Market Cap',
            #                                                   'Price',
            #                                                   'Circulating Supply',
            #                                                   'Max Supply'])
            # data_down = data[i:]
            # frames = [data_up, row_btc, data_down]
            # df = pd.concat(frames, sort=False)
            # df2 = df[['Rank', 'Name', 'Market Cap', 'Price', 'Today', 'Country']]

    return data2


# -------------------------- EXTRAS -------------------

import urllib.request

def get_techcrunch_techcrunch_rss(request):

    url='https://techcrunch.com/feed/'
    data=urllib.request.urlopen(url)
    string_data=str(data.read().decode('utf-8'))

    print(string_data)
    
    return render(request, 'rss/techcrunch/techcrunch.xml', locals(), content_type="application/xhtml+xml")


def get_techcrunch_startups_rss(request):

    url='https://techcrunch.com/startups/feed/'
    data=urllib.request.urlopen(url)
    string_data=str(data.read().decode('utf-8'))

    string_data=string_data.replace('<atom:link href="https://techcrunch.com/startups/feed/" rel="self" type="application/rss+xml" />','')
    # string_data=string_data.replace('<script data-dapp-detection="">!function(){let e=!1;function n(){if(!e){const n=document.createElement("meta");n.name="dapp-detected",document.head.appendChild(n),e=!0}}if(window.hasOwnProperty("ethereum")){if(window.__disableDappDetectionInsertion=!0,void 0===window.ethereum)return;n()}else{var t=window.ethereum;Object.defineProperty(window,"ethereum",{configurable:!0,enumerable:!1,set:function(e){window.__disableDappDetectionInsertion||n(),t=e},get:function(){if(!window.__disableDappDetectionInsertion){const e=arguments.callee;e&&e.caller&&e.caller.toString&&-1!==e.caller.toString().indexOf("getOwnPropertyNames")||n()}return t}})}}();</script>',"")
    # string_data=string_data.replace('<rss xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/" xmlns:slash="http://purl.org/rss/1.0/modules/slash/" version="2.0">','<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/" version="2.0">')
    print(string_data)

    return render(request, 'rss/techcrunch/startups.xml', locals(), content_type="application/xhtml+xml")
