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
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.status import (
#     HTTP_400_BAD_REQUEST,
#     HTTP_404_NOT_FOUND,
#     HTTP_200_OK
# )
# from rest_framework.response import Response
from .forms import SignUpForm
from django.contrib import messages

# ------------------------  INICIO LOGIN ------------------


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

# ------------------------  FIN LOGIN ------------------

# ------------------------ INICIO INDEX ------------------

from pycoingecko import CoinGeckoAPI
import time
#import yfinance as yf

def index_view(request):

    # Variables de reporte mensual
    text1 = "-"
    text2 = "- "
    text3 = "BitcoinIn"

    current_time = time.localtime()
    now1=time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    cg = CoinGeckoAPI()
    json_response=cg.get_coin_market_chart_by_id('bitcoin','usd','1')

    one_billion=1000000000
    thousand=1000
    myindex=0

    last_price_bitcoin=round(json_response['prices'][myindex][1],2)
    last_marketcap_bitcoin=round(json_response['market_caps'][myindex][1]/one_billion,2)
    last_volume_bitcoin=round(json_response['total_volumes'][myindex][1]/one_billion,2)

    # print(json_response)
    
    return render(request, 'index/index.html', locals())

# -------------------------- FIN INDEX -------------------
