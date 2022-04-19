"""
Unibet odds scraper
"""

from collections import defaultdict
import config
import tools

import datetime
import json

import requests

import sportsbetting as sb

import pandas as pd
import numpy as np

def get_id_league(url):
    """
    Get league id from url
    """
    if "https://www.unibet.fr" not in url:
        return None, None
    public_url = url.split("https://www.unibet.fr")[1]
    request_url = "https://www.unibet.fr/zones/navigation.json?publicUrl="+public_url
    content = requests.get(request_url).content
    if "Nos services ne sont pas accessibles pour le moment et seront de retour au plus vite." in str(content):
        raise sb.UnavailableSiteException
    parsed = json.loads(content)
    sport = public_url.split("/")[2]
    if sport == "cotes-boostees":
        sport = public_url.split("-cotes-boostees")[0].split("/")[-1]
    if parsed["requestData"]:
        return parsed["requestData"].get("nodeId"), sport
    return None, None


def parse_unibet_api(id_league, sport, boost):
    """
    Get Unibet odds from league id and sport
    """
    parameter = ""
    if sport == "tennis":
        parameter = "Vainqueur%2520du%2520match"
    elif "basket" in sport:
        parameter = "Vainqueur%2520du%2520match%2520%2528prolong.%2520incluses%2529"
    else:
        parameter = "R%25C3%25A9sultat%2520du%2520match"
    url = ("https://www.unibet.fr/zones/sportnode/markets.json?nodeId={}&filter=R%25C3%25A9sultat&marketname={}"
           .format(id_league, parameter))
    content = requests.get(url).content
    parsed = json.loads(content)
    markets_by_type = parsed.get("marketsByType", [])
    odds_match = {}
    site_name = "unibet" + ("_boost" if boost else "")
    for market_by_type in markets_by_type:
        days = market_by_type["days"]
        for day in days:
            events = day["events"]
            for event in events:
                markets = event["markets"]
                for market in markets:
                    name = (market["eventHomeTeamName"].replace(" - ", "-")
                            + " - " + market["eventAwayTeamName"].replace(" - ", "-"))
                    date = datetime.datetime.fromtimestamp(market["eventStartDate"]/1000)
                    odds = []
                    selections = market["selections"]
                    for selection in selections:
                        price_up = int(selection["currentPriceUp"])
                        price_down = int(selection["currentPriceDown"])
                        odds.append(round(price_up / price_down + 1, 2))
                    odds_match[name] = {
                        "date":date,
                        "odds":{site_name:odds},
                        "id":{"unibet":event["eventId"]},
                        "competition":event["competitionName"]
                    }

    df_odds_match = transform_dict_to_df(odds_match)

    return df_odds_match

def parse_unibet(url, boost=False):
    """
    Get Unibet odds from url
    """
    id_league, sport = get_id_league(url)
    if id_league:
        return parse_unibet_api(id_league, sport, boost)
    print("Wrong unibet url")
    return {}


def transform_dict_to_df(dict_unibet):
    df = pd.DataFrame.from_dict(dict_unibet)
    df_transposed = df.transpose()

    df_transposed['site'] = "Unibet"
    df_odd = pd.DataFrame.from_records(df_transposed.odds.tolist())
    df_odd_splited = pd.DataFrame(df_odd['unibet'].to_list(), columns=['odd_1', 'odd_n', 'odd_2'])
    df_odd_splited.index = df_transposed.index

    df = pd.concat([df_transposed, df_odd_splited], axis=1)

    df['country'] = df['competition'].str.split(', ').str[0]
    df['comp'] = df['competition'].str.split(', ').str[1]
    df = df.replace(np.nan, 0)
    df['comp'] = np.where(df['comp'] == 0, df['country'], df['comp'])
    df['country'] = np.where(df['country'] == df['comp'], 'International', df['country'])

    df.drop(['odds', 'id', 'competition'], axis=1, inplace=True)
    df.rename(columns={'comp': 'competition'}, inplace=True)

    df = tools.sort_df_columns_from_list(df, config.COLUMNS_ODDS_DF)

    return df