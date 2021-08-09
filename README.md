# BitcoinIN - Web

[![Build Status](https://app.travis-ci.com/pablodz/bitcoinin.svg?branch=main)](https://app.travis-ci.com/pablodz/bitcoinin)

<br />
<p align="center">
  <a href="#">
    <img src="docs/img/logo.png" height="128">
  </a>

  <h3 align="center">Bitcoin in ... <br>
  (Stocks, money, ...)</h3>

  <p align="center">
    <br />
    <a href="https://bitcoinin.herokuapp.com">View Demo</a>
  </p>
</p>

<hr style="height:2px;border-width:0;color:gray;background-color:gray">

![](docs/img/screenshot.png)

<hr style="height:2px;border-width:0;color:gray;background-color:gray">

<!-- TABLE OF CONTENTS -->
<!-- ## Table of Contents -->



<!-- ABOUT THE PROJECT -->
## About The Project

Represent the growth of Bitcoin.

List of cards:

1. Bitcoin Dashboard
   1. Bitcoin Market Cap (24H)
   2. Bitcoin Volume (24H)
   3. Comparison with last year (1yo)
2. Bitcoin listed as company by market cap
3. Bitcoin listed as currrency by market cap
4. Bitcoin listed as crypto by market cap

Sources: fiatmarketcap, companiesmarketcap, coingecko, coinranking

## Install

### Local


```
sudo apt-get install python3-lxml
```

```
# Clone, install dependencies and run
git clone https://github.com/ZurMaD/bitcoinin
cd bitcoinin
pip3 install -r requirements.txt
python3 bitcoinin/manage.py runserver
```

### On Heroku

```
curl https://cli-assets.heroku.com/install.sh | sh # heroku install
heroku login
# Login here with browser
heroku buildpacks:add --index 1 heroku-community/apt -a NAME_OF_YOUR_APP
# Then connect your github repository to heroku and that's it.
```


### On Docker (comming soon)

```
...
```
