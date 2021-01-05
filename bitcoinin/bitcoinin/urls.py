"""bitcoinin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

# Heroku
from django.conf import settings
from django.conf.urls.static import static

# Login
from .views import signup

# Pages
from .views import index_view
from .views import bitcoinasacompany_view
from .views import bitcoinasfiat_view
from .views import bitcoinascrypto_view

urlpatterns = [

    path('admin/', admin.site.urls),
    # -----------------INICIO LOGIN----------------
    path('accounts/', include('django.contrib.auth.urls')), # No register auth builded
    url(r'^accounts/register/$',signup,name='signup'),
    # -----------------FIN LOGIN----------------

    # -----------------INICIO INDEX----------------
    path('', index_view, name='main-view'),
    path('bitcoinasacompany/', bitcoinasacompany_view, name='bitcoinasacompany-view'),
    path('bitcoinasfiat/', bitcoinasfiat_view, name='bitcoinasfiat-view'),
    path('bitcoinascrypto/', bitcoinascrypto_view, name='bitcoinascrypto-view'),
    # ------------------FIN INDEX------------------

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
