from typing import Mapping
from duneanalytics import DuneAnalytics
from datetime import datetime
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

load_dotenv()

# initialize client
dune = DuneAnalytics(os.environ['USER'], os.environ['PASS'])

# try to login
dune.login()

# fetch token
dune.fetch_auth_token()

# amount of daily feed requests made to chainlink


def chainlink_dailyFeedRequests():
    # https://dune.xyz/queries/566527
    result_id = dune.query_result_id(query_id=392745)

    # fetch query result
    data = dune.query_result(result_id)
    data2 = data['data']['get_result_by_result_id']

    times = []
    values = []
    results = []

    for datum in data2:
        time = datetime.fromisoformat(
            datum['data']['date']).strftime('%b-%d-%Y')

        txnsCount = datum['data']['txns']

        # print(str(time) + ": " +
        #       str(txnsCount) + " chainlink feed requests")

        if txnsCount > 200:
            times.append(time)
            values.append(txnsCount)

            results.append((time, txnsCount))

    fig, ax = plt.subplots(figsize=(8, 6))

    half_year_locator = mdates.MonthLocator(interval=3)
    # Locator for major axis only.
    ax.xaxis.set_major_locator(half_year_locator)

    plt.plot(times, values)
    plt.xticks(rotation=15)

    plt.xlabel('Date')
    plt.ylabel('Chainlink Feed Requests')
    plt.title('Daily Chainlink Feed Requests')
    plt.show()


# total number of feed requests per consumer
def chainlink_consumerFeedRequests():
    # https://dune.xyz/queries/505151/955038
    result_id = dune.query_result_id(query_id=505151)

    # fetch query result
    data = dune.query_result(result_id)
    data2 = data['data']['get_result_by_result_id']

    consumers = []
    reads = []
    results = []

    for datum in data2:
        consumer = datum['data']['consumer']
        read = datum['data']['reads']

        # print(str(consumer) + ": " + str(read))

        if read > 5000:
            consumers.append(consumer)
            reads.append(read)

            results.append((consumer, read))

    plt.pie(reads, labels=consumers, autopct='%1.1f%%')
    # plt.legend(consumers, loc='upper left')
    plt.title('Total Chainlink Feed Requests per Consumer')
    plt.show()


def chainlink_consumerFeedRequestsNoChainlink():
    # https://dune.xyz/queries/505151/955038
    result_id = dune.query_result_id(query_id=505151)

    # fetch query result
    data = dune.query_result(result_id)
    data2 = data['data']['get_result_by_result_id']

    consumers = []
    reads = []
    results = []

    for datum in data2:
        consumer = datum['data']['consumer']
        read = datum['data']['reads']

        # print(str(consumer) + ": " + str(read))

        if read < 30000 and read > 600:
            consumers.append(consumer)
            reads.append(read)

            results.append((consumer, read))

    plt.pie(reads, labels=consumers, autopct='%1.1f%%')
    # plt.legend(consumers, loc='upper left')
    plt.title('Total Chainlink Feed Requests per Consumer, < 30 000 reads')
    plt.show()


def chainlink_consumerFeedRequestsNoChainlinkBAR():
    # https://dune.xyz/queries/505151/955038
    result_id = dune.query_result_id(query_id=505151)

    # fetch query result
    data = dune.query_result(result_id)
    data2 = data['data']['get_result_by_result_id']

    consumers = []
    reads = []
    results = []

    for datum in data2:
        consumer = datum['data']['consumer']
        read = datum['data']['reads']

        # print(str(consumer) + ": " + str(read))

        if read < 30000 and read > 100:
            consumers.append(consumer)
            reads.append(read)

            results.append((consumer, read))

    plt.bar(consumers, reads)
    plt.xticks(rotation=30)
    plt.title('Total Chainlink Feed Requests per Consumer, < 30 000 reads')
    plt.show()


def chainlink_priceFeedsMostRequested2():
    # https://dune.xyz/queries/509884/963063
    result_id = dune.query_result_id(query_id=509884)

    # fetch query result
    data = dune.query_result(result_id)
    data2 = data['data']['get_result_by_result_id']

    feeds = []
    payouts = []
    sorted_dict = {}

    diction = {}

    for datum in data2:

        feedName = str(datum['data']['feed_name'])
        payout = datum['data']['payouts_link']

        if feedName in diction:
            diction[feedName] += payout
        else:
            diction[feedName] = payout

    sorted_values = sorted(diction.values())

    # sort the dictionary by value
    for i in sorted_values:
        for k in diction.keys():
            if diction[k] == i:
                sorted_dict[k] = diction[k]
                break

    for key, value in reversed(sorted_dict.items()):
        if value > 30000:       # change this value to see the top x reads
            feeds.append(key)
            payouts.append(value)

    # fig = plt.figure()
    # ax = fig.add_axes([0,0,1,1])
    plt.bar(feeds, payouts)
    plt.xticks(rotation=30)
    plt.title('Most requested Chainlink feeds, Past year')
    plt.show()


def chainlink_dailyUniqueConsumersNoChainlink():
    # https://dune.xyz/queries/578702
    result_id = dune.query_result_id(query_id=578702)

    # fetch query result
    data = dune.query_result(result_id)
    data2 = data['data']['get_result_by_result_id']

    counts = []
    times = []

    for datum in data2:
        count = datum['data']['count']
        time = datetime.fromisoformat(
            datum['data']['day']).strftime('%b-%d-%Y')

        times.append(time)
        counts.append(count)

    fig, ax = plt.subplots(figsize=(8, 6))

    half_year_locator = mdates.MonthLocator(interval=3)
    # Locator for major axis only.
    ax.xaxis.set_major_locator(half_year_locator)

    plt.bar(times, counts)
    plt.xticks(rotation=30)
    plt.title('Daily Unique Chainlink Consumers, Chainlink excluded')
    plt.show()


def chainlink_dailyUniqueConsumersNoChainlink2():
   # https://dune.xyz/queries/578702    
    # https://dune.xyz/queries/579473 this is for the unnamed contracts

    result_id = dune.query_result_id(query_id=578702)
    result_id2 = dune.query_result_id(query_id=579473)

    # fetch query result
    data = dune.query_result(result_id)
    data2 = data['data']['get_result_by_result_id']

    data3 = dune.query_result(result_id2)
    data4 = data3['data']['get_result_by_result_id']

    counts = []
    counts2 = []
    times = []

    for datum in data2:
        count = datum['data']['count']
        time = datetime.fromisoformat(
            datum['data']['day']).strftime('%b-%d-%Y')

        times.append(time)
        counts.append(count)
    
    for datum in data4:
        count = datum['data']['count']
        time = datetime.fromisoformat(
            datum['data']['day']).strftime('%b-%d-%Y')
        counts2.append(count)

    final_counts=np.add(counts, counts2)

    fig, ax = plt.subplots(figsize=(8, 6))

    half_year_locator = mdates.MonthLocator(interval=3)
    # Locator for major axis only.
    ax.xaxis.set_major_locator(half_year_locator)

    plt.bar(times, final_counts)
    plt.xticks(rotation=30)
    plt.title('Daily Unique Chainlink Consumers, Chainlink excluded')
    plt.show()


# chainlink_dailyFeedRequests()
# chainlink_consumerFeedRequests()
# chainlink_consumerFeedRequestsNoChainlink()
# chainlink_priceFeedsMostRequested2()
chainlink_consumerFeedRequestsNoChainlinkBAR()
chainlink_dailyUniqueConsumersNoChainlink()
# chainlink_dailyUniqueConsumersNoChainlink2()
# https://dune.xyz/queries/509884/963063
