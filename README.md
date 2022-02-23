# Defi-DApps-Investment-Analyzer

DeFi, or Decentralized Finance  is a relatively new area of the crypto-currency world that aims to sustainably transform the financial services industry, primarily by eliminating financial intermediaries. 
This area involves two important terms which are DeFi centralized applications  which are applications related to borrowing lending, exchanges, payments) and which are based on the blockchain technology (the most popular is ethereum). This brings us to the second element which are the Defi Tokens, with a market capitalization of more than 2 billion, they are the ones who give this panoply of possible services, we can mention Maker, Uniswap, Aave...The principle is mainly based on Purchasing a DeFi coin transfers value to the related dApp.

Our DeFi projects aims to buil application to help the investors find the best project. 
Indeed, this project will try to provide an analysis by using Jupiter Notebook. 
The value of a coin is directly related to its control over liquidity. This can be measured by the following ratio: Market Cap/ Total Value Locked (TVL). Therefore, the investor will be able to use this tool to visualize TVL for all coins, Market Cap for all coins, and the comparison of the ratio between all the coins in order to see what is the best investment for him.

  ## Technologies

This project uses Anaconda and Jupyterlab with **Python 3.9** 

It incorporates the following 9 required dependencies. These dependencies include the folowing imports :

```
 import os
 import requests
 import json
 import pandas as pd
 from dotenv import load_dotenv
 from pycoingecko import CoinGeckoAPI
 from datetime import datetime
 from defillama import DefiLlama
 %matplotlib inline

```
 ## Installation Guide
 
 
 ### Install the Request and Json Library 
 We will use the following Python modules and libraries to facilitate API requests:

   1.OS: The OS module comes under Python's standard utility models and provides functions for interacting with the computer's operating system. The OS module does          not require a separate download.
   2.Requests: The Python Requests library helps you access data via APIs.
   3.JSON: This library puts the response (that is, the data) from an API into a human-readable format.

 To install the Requests library, check that your development environment is active, and then run the following command:
  
  ```conda install -c anaconda requests```

 To install the JSON library, check that your development environment is active, and then run the following command:
   
   ```conda install -c jmcmurray json```



### Install the python-dotenv Library
To install this library, run the following command in your terminal:

```pip install python-dotenv```

### Install the Alpaca SDK
To install this SDK, run the following command in your terminal:

```pip install alpaca-trade-api```


