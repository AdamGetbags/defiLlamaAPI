# -*- coding: utf-8 -*-
"""
DeFi Llama API - Python Tutorial

@author: AdamGetbags
"""

import pandas as pd
import requests
import json
from datetime import datetime
import time
import math

baseUrl = 'https://api.llama.fi'

# protocols endpoint
protocols = requests.get(baseUrl + '/protocols')

# explore the data
dir(protocols)
print(protocols.json())
print(protocols.json()[0])
print(protocols.json()[0].keys())
print(protocols.json()[0]['chainTvls'])
print(protocols.json()[0]['chainTvls']['Bitcoin'])

# to dataframe
protocolData = pd.DataFrame.from_dict(protocols.json())
len(protocolData.columns)
print(protocolData.columns)

# review data
print(protocolData.slug.sort_values()[:50])
# get protocol slug
slug = protocols.json()[20]['slug']

# protocol data by slug endpoint
oneProtocol = requests.get(baseUrl + '/protocol/' + slug)

# explore the data
print(oneProtocol.json().keys())
print(oneProtocol.json()['chainTvls'])
print(oneProtocol.json()['chainTvls'].keys())
oneProtocol.json()['chainTvls']['Ethereum']
print(oneProtocol.json()['chainTvls']['Ethereum'].keys())
oneProtocol.json()['chainTvls']['Ethereum']['tvl']
print(oneProtocol.json()['chainTvls']['Ethereum']['tvl'][0])
print(oneProtocol.json()['chainTvls']['Ethereum']['tvl'][-1]['date'])
testTimestamp = oneProtocol.json()['chainTvls']['Ethereum']['tvl'][-1]['date']
print(datetime.fromtimestamp(testTimestamp))

# historical chain tvl endpoint // all chains
historicTVL = requests.get(baseUrl + '/v2/historicalChainTvl')
# historicTVL.json()

# get chain name
chain = protocolData.chain[5]
# historical chain tvl endpoint by chain
historicChainTVL = requests.get(baseUrl + '/v2/historicalChainTvl/' + chain)
# to dataframe
historicChainTVLData  = pd.DataFrame.from_dict(historicChainTVL.json())

# simple tvl endpoint
simpleTVL = requests.get(baseUrl + '/tvl/' + slug)
# simpleTVL.json()

# all chains tvl
allTVL = requests.get(baseUrl + '/v2/chains')
# allTVL.json()
allTVLData = pd.DataFrame.from_dict(allTVL.json())

# set coins base url
coinsUrl = 'https://coins.llama.fi'
# input data
# set(protocolData.chain)
chainName = 'arbitrum'
contractAddress = '0x6C2C06790b3E3E3c38e12Ee22F8183b37a13EE55'
coins = chainName + ':' + contractAddress
# sample address from docs
coins2 = 'ethereum:0x69b4B4390Bd1f0aE84E090Fe8af7AbAd2d95Cc8E'
# get current price data
coinPrice = requests.get(coinsUrl + '/prices/current/' + coins)
# coinPrice.json()

# timestamp data
# ts = str(historicChainTVLData.date[len(historicChainTVLData)-1])
ts = str(1676000000)
# get cross-sectional historical price data
historicPrice = requests.get(
                    coinsUrl + '/prices/historical/' + ts + '/' + coins)
# historicPrice.json()

# sample date 
print(datetime.fromtimestamp(1672560000))

# stringDate = "02/01/2023"
# sampleDatetime = datetime.strptime(stringDate,"%m/%d/%Y")
# sampleTimestamp = datetime.timestamp(sampleDatetime)
# print(sampleTimestamp)

# price chart data // start + span 
chartData = requests.get(coinsUrl + '/chart/' + coins +
                         '?start=1672560000' +
                         '&span=10' + 
                         '&period=1d' + 
                         '&searchWidth=600')

# data may truncate with span // increase searchWidth if data is truncated
chartData = requests.get(coinsUrl + '/chart/' + coins + 
                         '?start=1672560000' + 
                         '&span=100' +
                         '&period=1d' +
                         '&searchWidth=600')

# get to the price data
# chartData.json()['coins'][
#     list(chartData.json()['coins'].keys())[0]]['prices']

priceData = pd.DataFrame.from_dict(
                chartData.json()['coins'][
                list(chartData.json()['coins'].keys())[0]]['prices'])

# priceData.price.plot()

# pct chg data // verify your data!
pctChgData = requests.get(coinsUrl + '/percentage/' + coins +
                         '?timestamp=1672560000' +
                         '&lookForward=false' + 
                         '&period=4w')

tsNow = str(math.floor(time.time()))
# closest block to timestamp
closestBlock = requests.get(coinsUrl + '/block/' + chainName + '/' + tsNow)

# closestBlock.json()

# bridges base url
bridgesBaseUrl = 'https://bridges.llama.fi'

# list all bridges
bridges = requests.get(bridgesBaseUrl + '/bridges/' + '?includeChains=true')

# bridges.json()
# bridges.json()['bridges']
# bridges.json()['chains']

# bridge ID 
bridgeID = str(bridges.json()['bridges'][1]['id'])

# bridge summary 
bridgeSummary = requests.get(bridgesBaseUrl + '/bridge/' + bridgeID)

# bridgeSummary.json()

# bridge / chain volume
bridgeVolume = requests.get(bridgesBaseUrl + '/bridgevolume/' + 
                            chainName + 
                            '?id=2')
# bridgeVolume.json()

# 24hr bridge stats
dailyBridgeStats = requests.get(bridgesBaseUrl + '/bridgedaystats/' + 
                                ts + '/' +
                                'ethereum' +
                                '?id=5')
# dailyBridgeStats.json()

# transactions by bridge, address
bridgeTransactions = requests.get(bridgesBaseUrl + '/transactions/' + 
                                  '1' + '?' +
                                  'starttimestamp=1667260800' +
                                  '&endtimestamp=1667347200' +
                                  '&sourcechain=Polygon'
                                  '&address=' + coins2 +
                                  '&limit=200')

# dex overview
dexOverview = requests.get(baseUrl + '/overview/dexs' + 
                           '?excludeTotalDataChart=false' +
                           '&excludeTotalDataChartBreakdown=false' +
                           '&dataType=dailyVolume')

# dexOverview.json()
print(dexOverview.json().keys())
print(dexOverview.json()['totalDataChartBreakdown'])
print(dexOverview.json()['protocols'][0])
print(dexOverview.json()['allChains'])
print(dexOverview.json()['total24h'])
print(dexOverview.json()['total60dto30d'])


dexOverviewByChain = requests.get(baseUrl + '/overview/dexs/' + chainName +
                                  '?excludeTotalDataChart=false' +
                                  '&excludeTotalDataChartBreakdown=false' +
                                  '&dataType=dailyVolume')

# dexOverviewByChain.json()
print(dexOverviewByChain.json().keys())

# options dex overview
optionsDexData = requests.get(baseUrl + '/overview/options/' +
                                  '?excludeTotalDataChart=false' +
                                  '&excludeTotalDataChartBreakdown=false' +
                                  '&dataType=dailyPremiumVolume')

# optionsDexData.json()
# optionsDexData.json().keys()
# optionsDexData.json()['protocols']
print(len(optionsDexData.json()['protocols']))
# optionsDexData.json()['totalDataChartBreakdown']

# options dex by chain // similar data as above
optionsDexByChain = requests.get(baseUrl + '/overview/options/' + chainName +
                                  '/?excludeTotalDataChart=false' +
                                  '&excludeTotalDataChartBreakdown=false' +
                                  '&dataType=dailyPremiumVolume')

# optionsDexByChain.json()

optionsProtocol = optionsDexByChain.json()['protocols'][0]['module']

# options summary by option dex
optionSummary = requests.get(baseUrl + '/summary/options/' + optionsProtocol +
                                  '/?dataType=dailyPremiumVolume')

# optionSummary.json()
# optionSummary.json().keys()

# stablecoins endpoints url
stablecoinsUrl = 'https://stablecoins.llama.fi'

# get stablecoins data
stablecoins = requests.get(stablecoinsUrl + '/stablecoins/' +
                           '?includePrices=true')

# stablecoins.json()
# stablecoins.json().keys()
# len(stablecoins.json()['peggedAssets'])
# stablecoins.json()['peggedAssets'][0]
# stablecoins.json()['peggedAssets'][0].keys()
# stablecoins.json()['peggedAssets'][0]
# stablecoins.json()['peggedAssets'][0]['name']
# stablecoins.json()['peggedAssets'][0]['chainCirculating']

stblCoinID = stablecoins.json()['peggedAssets'][0]['id']

# get stablecoin chart data
stblCoinChart = requests.get(stablecoinsUrl + '/stablecoincharts/all' +
                           '?stablecoin=' + stblCoinID)

# stblCoinChart.json()
# stblCoinChart.json()[0]

# get stablecoin chart data by chain
stblCoinChartByChain = requests.get(stablecoinsUrl + '/stablecoincharts/' + 
                             chainName +
                             '?stablecoin=' + stblCoinID)

# stblCoinChartByChain.json()
# stblCoinChartByChain.json()[0]

# get historic mktcap chain distribution of stablecoin
stblCoinHistory = requests.get(stablecoinsUrl + '/stablecoin/' + 
                                    stblCoinID)

# stblCoinHistory.json()
# stblCoinHistory.json().keys()
# stblCoinHistory.json()['chainBalances']
# stblCoinHistory.json()['chainBalances'].keys()
# stblCoinHistory.json()['chainBalances']['Ethereum']['tokens'][0]

# stablecoin chain data
stblCoinChains = requests.get(stablecoinsUrl + '/stablecoinchains')

# stblCoinChains.json()
# stblCoinChains.json()[0]

# historical stablecoin price data
stblCoinPrices = requests.get(stablecoinsUrl + '/stablecoinprices')

# stblCoinPrices.json()
# stblCoinPrices.json()[0]
# stblCoinPrices.json()[0]['prices']
# stblCoinPrices.json()[0]['prices']['tether']

# yields url
yieldsUrl = 'https://yields.llama.fi'

# pool data
poolData = requests.get(yieldsUrl + '/pools')

# poolData.json()
# poolData.json().keys()
# poolData.json()['data']
# len(poolData.json()['data'])
# poolData.json()['data'][0]

poolID = poolData.json()['data'][1]['pool']

# apy and tvl data for pool

# pool data
poolData = requests.get(yieldsUrl + '/chart/' + poolID)

# poolData.json()
# poolData.json().keys()
# poolData.json()['data']
# poolData.json()['data'][0]

decoderUrl = 'https://abi-decoder.llama.fi'

# fetch signature endpoint
fetchSig = requests.get(decoderUrl + '/fetch/signature/' + '?functions='
                        '0x23b872dd,0x18fccc76,0xb6b55f25,0xf5d07b60' +
                        '&events=' + '0xddf252ad1be2c89b69c2b068fc378daa952' +
                        'ba7f163c4a11628f55a4df523b3ef')

# fetchSig.json()
# fetchSig.json().keys()
# fetchSig.json()['functions']
# fetchSig.json()['functions'].keys()
# fetchSig.json()['functions'][list(fetchSig.json()['functions'].keys())[0]]
# fetchSig.json()['events']
# fetchSig.json()['events'][list(fetchSig.json()['events'].keys())[0]]

# fetch contract endpoint
fetchContract = requests.get(decoderUrl + '/fetch/contract/' + 
    'ethereum' + '/'
    '0x02f7bd798e765369a9d204e9095b2a526ef01667' + '/'
    '?functions=' + '0xf43f523a,0x95d89b41,0x95d89b41,0x70a08231,0x70a08231' +
    '&events=' + '0xddf252ad1be2c89b69c2b068fc378daa952ba' +
    '7f163c4a11628f55a4df523b3ef')

# fetchContract.json()

# fee overview // similar structure to dexOverview
feeOverview = requests.get(baseUrl + '/overview/fees/' +
                           '?excludeTotalDataChart=false' +
                           '&excludeTotalDataChartBreakdown=false' + 
                           '&datatype=dataType=dailyFees')

# feeOverview.json()
# feeOverview.json().keys()
# feeOverview.json()['totalDataChartBreakdown']
# feeOverview.json()['totalDataChartBreakdown'][0]

# fee overview by chain // similar structure to dexOverview
chainFeeOverview = requests.get(baseUrl + '/overview/fees/' + chainName + '/'
                           '?excludeTotalDataChart=false' +
                           '&excludeTotalDataChartBreakdown=false' + 
                           '&datatype=dataType=dailyFees')

# chainFeeOverview.json()
# chainFeeOverview.json().keys()
# chainFeeOverview.json()['totalDataChartBreakdown']
# chainFeeOverview.json()['totalDataChartBreakdown'][0]


protocolFeeOverview = requests.get(baseUrl + '/summary/fees/' + 'lyra/' + 
                           '?datatype=dataType=dailyFees')

# protocolFeeOverview.json()
# protocolFeeOverview.json().keys()
# protocolFeeOverview.json()['totalDataChartBreakdown']