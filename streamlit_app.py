# Import the required libraries and dependencies
import os
import requests
import json
import pandas as pd
import hvplot.pandas
from defillama import DefiLlama
from requests import Request
from pycoingecko import CoinGeckoAPI
from datetime import datetime

%matplotlib inline
# initialize api client
llama = DefiLlama()
cg = CoinGeckoAPI()

# Get all protocols data
response_llama = llama.get_all_protocols()
print(json.dumps(response_llama[0], indent=4, sort_keys=True))

# Get a protocol data for uniswap
uniswap_response = llama.get_protocol(name='uniswap')

# Get all TVL from Ethereum network, not other networks
uniswap_response_df = pd.DataFrame(uniswap_response['chainTvls']['Ethereum']['tvl'], columns=['date','totalLiquidityUSD'])



uniswap_response_df['date'] = pd.to_datetime(uniswap_response_df['date'],unit='s')
uniswap_response_df.set_index('date',inplace=True)
uniswap_response_df.head()
# print(json.dumps(uniswap_response, indent=4, sort_keys=True))

uniswap_response_df.describe()

uniswap_response_df['totalLiquidityUSD'].hvplot(
    xlabel="Time",
    ylabel="Total Liquidity in USD",
    title ="Uniswap Total Liquidity (11-2018 - 02-2022)",
    rot=90, 
    height = 500,
    width = 1500 
)
llama_df = pd.DataFrame(response_llama, columns=['name','symbol','chains','mcap','tvl'])
llama_df = llama_df.rename(columns={'mcap':'Market Cap','tvl':'Total Value Locked','chains':'Network'})

llama_df['MCAP/TVL'] = llama_df['Market Cap']/llama_df['Total Value Locked']

llama_df.head()
# print(json.dumps(response_llama, indent=4, sort_keys=True))

# Get a protocol data
aave_response = llama.get_protocol(name='aave')

# Get a protocol data
compound_response = llama.get_protocol(name='compound')

# Get a protocol data
curve_response = llama.get_protocol(name='curve')

# Get a protocol data
uniswap_response = llama.get_protocol(name='uniswap')

# Get a protocol data
makerdao_response = llama.get_protocol(name='makerdao')

aave_defi_df = pd.DataFrame(
    aave_response['tvl'], 
    columns=['date', 
    'totalLiquidityUSD']).rename(columns={'totalLiquidityUSD':'AAVE TVL'}
                                                                        )

compound_defi_df = pd.DataFrame(
    compound_response['tvl'],
    columns=['date', 
    'totalLiquidityUSD']).rename(columns={'totalLiquidityUSD':'COMP TVL'}
                                )
curve_defi_df = pd.DataFrame(
    curve_response['tvl'], 
    columns=['date', 
    'totalLiquidityUSD']).rename(columns={'totalLiquidityUSD':'CURVE TVL'})

uniswap_defi_df = pd.DataFrame(uniswap_response['tvl'], 
    columns=['date', 
    'totalLiquidityUSD']).rename(columns={'totalLiquidityUSD':'UNISWAP TVL'})

makerdao_defi_df = pd.DataFrame(
    makerdao_response['tvl'], 
    columns=['date', 
    'totalLiquidityUSD']).rename(columns={'totalLiquidityUSD':'MAKER DAO TVL'})

#convert the date from UNIX format to datetime using pd.to_datetime

aave_defi_df['date'] = pd.to_datetime(aave_defi_df['date'],unit='s')
compound_defi_df['date'] = pd.to_datetime(compound_defi_df['date'],unit='s')
curve_defi_df['date'] = pd.to_datetime(curve_defi_df['date'],unit='s')
uniswap_defi_df['date'] = pd.to_datetime(uniswap_defi_df['date'],unit='s')
makerdao_defi_df['date'] = pd.to_datetime(makerdao_defi_df['date'],unit='s')

#set the index column for each dataframe to 'date'

aave_defi_df.set_index('date',inplace=True)
compound_defi_df.set_index('date', inplace=True)
curve_defi_df.set_index('date', inplace=True)
uniswap_defi_df.set_index('date', inplace=True)
makerdao_defi_df.set_index('date', inplace=True)

tvl_df = pd.concat([aave_defi_df, compound_defi_df, curve_defi_df, uniswap_defi_df, makerdao_defi_df]).groupby(['date']).sum()
tvl_df=tvl_df.mask(tvl_df==0).ffill(downcast='infer').fillna(0)

tvl_df.tail(10)
tvl_df.tail(100)

tvl_df.hvplot(
    xlabel="Time",
    ylabel="Total Liquidity in USD",
    title ="Total Value Locked (01-2019 - 02-2022)",
    rot=90, 
    height = 500,
    width = 1500 
)
# Get AAVE historical data directly from CoinGecko using CoinGeckoAPI()

aave_data_cg = cg.get_coin_market_chart_by_id(id='aave', vs_currency='usd', days='1500')


# Get COMPOUND historical data directly from CoinGecko using CoinGeckoAPI()

comp_data_cg = cg.get_coin_market_chart_by_id(id='compound-governance-token', vs_currency='usd', days='1500')


# Get Curve historical data directly from CoinGecko using CoinGeckoAPI()

curve_data_cg = cg.get_coin_market_chart_by_id(id='curve-dao-token', vs_currency='usd', days='1500')


# Get Uniswap historical data directly from CoinGecko using CoinGeckoAPI()

uni_data_cg = cg.get_coin_market_chart_by_id(id='uniswap', vs_currency='usd', days='1500')

# Get Maker Dao historical data directly from CoinGecko using CoinGeckoAPI()

maker_data_cg = cg.get_coin_market_chart_by_id(id='maker', vs_currency='usd', days='1500')

#----------------------------------------------MARKET CAP----------------------------------------------------

#create a dataframe for each coin's market cap and set format the date from unix to datetime:

aave_market_cap_cg_df= pd.DataFrame(aave_data_cg['market_caps'])
aave_market_cap_cg_df[0]= pd.to_datetime(aave_market_cap_cg_df[0], unit='ms')
aave_market_cap_cg_df.columns=['date', 'aave mcap']
aave_market_cap_cg_df.set_index('date',inplace=True)

comp_market_cap_cg_df= pd.DataFrame(comp_data_cg['market_caps'])
comp_market_cap_cg_df[0]= pd.to_datetime(comp_market_cap_cg_df[0], unit='ms')
comp_market_cap_cg_df.columns=['date', 'comp mcap']
comp_market_cap_cg_df.set_index('date',inplace=True)

curve_market_cap_cg_df= pd.DataFrame(curve_data_cg['market_caps'])
curve_market_cap_cg_df[0]= pd.to_datetime(curve_market_cap_cg_df[0], unit='ms')
curve_market_cap_cg_df.columns=['date', 'curve mcap']
curve_market_cap_cg_df.set_index('date',inplace=True)

uni_market_cap_cg_df= pd.DataFrame(uni_data_cg['market_caps'])
uni_market_cap_cg_df[0]= pd.to_datetime(uni_market_cap_cg_df[0], unit='ms')
uni_market_cap_cg_df.columns=['date', 'uni mcap']
uni_market_cap_cg_df.set_index('date',inplace=True)

maker_market_cap_cg_df= pd.DataFrame(maker_data_cg['market_caps'])
maker_market_cap_cg_df[0]= pd.to_datetime(maker_market_cap_cg_df[0], unit='ms')
maker_market_cap_cg_df.columns=['date', 'maker mcap']
maker_market_cap_cg_df.set_index('date',inplace=True)

#Combine the dataframes using pd.concat:

all_coins_mcap_df = pd.concat(
    [aave_market_cap_cg_df,
     comp_market_cap_cg_df, 
     curve_market_cap_cg_df, 
     uni_market_cap_cg_df,  
     maker_market_cap_cg_df], 
    axis=1 
)

#group the data by date and drop duplicates

all_coins_mcap_df.groupby(['date']).sum().drop_duplicates()

#Assign "NaN" values to all "0" values in the dataset, then infer the previous known values 
#for all NaN values, therefore eliminating "0" values in columns and replacing them with previous values to smooth
#out the data.
#NOTE: Some coins did not exist at the beginning of the dataset and therefore have "0" values at the beginning of
#their date ranges

all_coins_mcap_df = all_coins_mcap_df.mask(all_coins_mcap_df==0).ffill(downcast='infer').fillna(0)

#view the dataframe
all_coins_mcap_df.head(1000)


all_coins_mcap_df.hvplot(
    xlabel="Time",
    ylabel="USD",
    title ="Market Cap for 5 dApps (01-2019 - 02-2022)",
    rot=90, 
    height = 500,
    width = 1500 
)
all_coins_mcap_df['aave mcap/tvl'] = all_coins_mcap_df['aave mcap']/tvl_df['AAVE TVL']
all_coins_mcap_df['comp mcap/tvl'] = all_coins_mcap_df['comp mcap']/tvl_df['COMP TVL']
all_coins_mcap_df['curve mcap/tvl'] = all_coins_mcap_df['curve mcap']/tvl_df['CURVE TVL']
all_coins_mcap_df['uni mcap/tvl'] = all_coins_mcap_df['uni mcap']/tvl_df['UNISWAP TVL']
all_coins_mcap_df['maker mcap/tvl'] = all_coins_mcap_df['maker mcap']/tvl_df['MAKER DAO TVL']

all_coins_mcap_df = all_coins_mcap_df.mask(all_coins_mcap_df==0).ffill(downcast='infer').fillna(0)
#all_coins_mcaptvl_df = all_coins_mcap_df.drop(columns=['aave mcap/tvl', 'comp mcap/tvl', 'curve mcap/tvl', 'uni mcap/tvl', 'maker mcap/tvl'])
all_coins_mcap_df.tail()

all_coins_mcaptvl_df = all_coins_mcap_df.drop(columns=['aave mcap', 'comp mcap', 'curve mcap', 'uni mcap', 'maker mcap'])

all_coins_mcaptvl_df.tail()
                                              

all_coins_mcaptvl_df.hvplot(
    xlabel="Time",
    ylabel="MCAP/TVL Ratios in USD",
    title ="MCAP/TVL Ratio for 5 dApps",
    rot=90, 
    height = 500,
    width = 1500 
)
#--------------------------------------------HISTORICAL PRICES-------------------------------------------------------


#create a dataframe for each coin's price and set format the date from unix to datetime:
#set the columns to 'date' and 'price'

aave_prices_cg_df= pd.DataFrame(aave_data_cg['prices'])
aave_prices_cg_df[0]= pd.to_datetime(aave_prices_cg_df[0], unit='ms')
aave_prices_cg_df.columns=['date', 'aave price']
aave_prices_cg_df.set_index('date',inplace=True)

comp_prices_cg_df= pd.DataFrame(comp_data_cg['prices'])
comp_prices_cg_df[0]= pd.to_datetime(comp_prices_cg_df[0], unit='ms')
comp_prices_cg_df.columns=['date', 'comp price']
comp_prices_cg_df.set_index('date',inplace=True)

curve_prices_cg_df= pd.DataFrame(curve_data_cg['prices'])
curve_prices_cg_df[0]= pd.to_datetime(curve_prices_cg_df[0], unit='ms')
curve_prices_cg_df.columns=['date', 'curve price']
curve_prices_cg_df.set_index('date',inplace=True)

uni_prices_cg_df= pd.DataFrame(uni_data_cg['prices'])
uni_prices_cg_df[0]= pd.to_datetime(uni_prices_cg_df[0], unit='ms')
uni_prices_cg_df.columns=['date', 'uni price']
uni_prices_cg_df.set_index('date',inplace=True)

maker_prices_cg_df= pd.DataFrame(maker_data_cg['prices'])
maker_prices_cg_df[0]= pd.to_datetime(maker_prices_cg_df[0], unit='ms')
maker_prices_cg_df.columns=['date', 'maker price']
maker_prices_cg_df.set_index('date',inplace=True)

#Combine the dataframes using pd.concat:

all_coins_prices_df = pd.concat(
    [aave_prices_cg_df,
     comp_prices_cg_df, 
     curve_prices_cg_df, 
     uni_prices_cg_df,  
     maker_prices_cg_df], 
    axis=1 
)
#group the data by date and drop duplicates
all_coins_prices_df.groupby(['date']).sum().drop_duplicates()

#Assign "NaN" values to all "0" values in the dataset, then infer the previous known values 
#for all NaN values, therefore eliminating "0" values in columns and replacing them with previous values to smooth
#out the data.
#NOTE: Some coins did not exist at the beginning of the dataset and therefore have "0" values at the beginning of
#their date ranges

all_coins_prices_df = all_coins_prices_df.mask(all_coins_prices_df==0).ffill(downcast='infer').fillna(0)

#view the dataframe
all_coins_prices_df.head(1000)


#--------------------------------------------HISTORICAL PRICES-------------------------------------------------------


#create a dataframe for each coin's price and set format the date from unix to datetime:
#set the columns to 'date' and 'price'

aave_prices_cg_df= pd.DataFrame(aave_data_cg['prices'])
aave_prices_cg_df[0]= pd.to_datetime(aave_prices_cg_df[0], unit='ms')
aave_prices_cg_df.columns=['date', 'aave price']
aave_prices_cg_df.set_index('date',inplace=True)

comp_prices_cg_df= pd.DataFrame(comp_data_cg['prices'])
comp_prices_cg_df[0]= pd.to_datetime(comp_prices_cg_df[0], unit='ms')
comp_prices_cg_df.columns=['date', 'comp price']
comp_prices_cg_df.set_index('date',inplace=True)

curve_prices_cg_df= pd.DataFrame(curve_data_cg['prices'])
curve_prices_cg_df[0]= pd.to_datetime(curve_prices_cg_df[0], unit='ms')
curve_prices_cg_df.columns=['date', 'curve price']
curve_prices_cg_df.set_index('date',inplace=True)

uni_prices_cg_df= pd.DataFrame(uni_data_cg['prices'])
uni_prices_cg_df[0]= pd.to_datetime(uni_prices_cg_df[0], unit='ms')
uni_prices_cg_df.columns=['date', 'uni price']
uni_prices_cg_df.set_index('date',inplace=True)

maker_prices_cg_df= pd.DataFrame(maker_data_cg['prices'])
maker_prices_cg_df[0]= pd.to_datetime(maker_prices_cg_df[0], unit='ms')
maker_prices_cg_df.columns=['date', 'maker price']
maker_prices_cg_df.set_index('date',inplace=True)

#Combine the dataframes using pd.concat:

all_coins_prices_df = pd.concat(
    [aave_prices_cg_df,
     comp_prices_cg_df, 
     curve_prices_cg_df, 
     uni_prices_cg_df,  
     maker_prices_cg_df], 
    axis=1 
)
#group the data by date and drop duplicates
all_coins_prices_df.groupby(['date']).sum().drop_duplicates()

#Assign "NaN" values to all "0" values in the dataset, then infer the previous known values 
#for all NaN values, therefore eliminating "0" values in columns and replacing them with previous values to smooth
#out the data.
#NOTE: Some coins did not exist at the beginning of the dataset and therefore have "0" values at the beginning of
#their date ranges

all_coins_prices_df = all_coins_prices_df.mask(all_coins_prices_df==0).ffill(downcast='infer').fillna(0)

#view the dataframe
all_coins_prices_df.head(1000)


all_coins_prices_df.hvplot(
    xlabel="Time",
    ylabel="USD",
    title ="Historical Prices for 5 dApps",
    rot=90, 
    height = 500,
    width = 1500 
)
