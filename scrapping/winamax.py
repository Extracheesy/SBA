import config
import tools

import datetime
import json
import urllib
import urllib.error
import urllib.request

import pandas as pandas
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

def parse_winamax(url):
    # url = "https://www.winamax.fr/paris-sportifs/sports/1/7/4"
    # url = 'https://www.winamax.fr/paris-sportifs/sports/1'
    ids = url.split("/sports/")[1]

    try:
        tournament_id = int(ids.split("/")[2])
    except IndexError:
        tournament_id = -1
    sport_id = int(ids.split("/")[0])
    #try:
    req = urllib.request.Request(url)
    webpage = urllib.request.urlopen(req, timeout=10).read()
    soup = BeautifulSoup(webpage, features="html.parser")

    #except urllib.error.HTTPError:
     #   raise sb.UnavailableSiteException


    match_odds_hash = {}
    for line in soup.find_all(['script']):
        if "PRELOADED_STATE" not in str(line.string):
            continue
        json_text = (line.string.split("var PRELOADED_STATE = ")[1]
                     .split(";var BETTING_CONFIGURATION")[0])
        if json_text[-1] == ";":
            json_text = json_text[:-1]
        dict_matches = json.loads(json_text)
        if "matches" not in dict_matches:
            continue
        for match in dict_matches["matches"].values():
            if (tournament_id in (match['tournamentId'], -1) and match["competitor1Id"] != 0
                    and match['sportId'] == sport_id and 'isOutright' not in match.keys()):
                try:
                    match_name = match["title"].strip().replace("  ", " ")
                    date_time = datetime.datetime.fromtimestamp(match["matchStart"])
                    if date_time < datetime.datetime.today():
                        continue
                    main_bet_id = match["mainBetId"]
                    odds_ids = dict_matches["bets"][str(main_bet_id)]["outcomes"]
                    odds = [dict_matches["odds"]
                            [str(x)] for x in odds_ids]
                    if not all(odds):
                        odds = []
                    match_odds_hash[match_name] = {
                        'odds' : {"winamax": odds},
                        'date' : date_time,
                        'id' : {"winamax": str(match["matchId"])},
                        'competition' : (
                            dict_matches["tournaments"]
                            [str(match['tournamentId'])]["tournamentName"]
                        )
                    }
                except KeyError:
                    pass
        if not match_odds_hash:
            print("Pb !!!")
            # raise sb.UnavailableCompetitionException

    df_match_odds_hash = transform_dict_to_df(match_odds_hash)

    return df_match_odds_hash

def transform_dict_to_df(dict_winamax):
    df = pd.DataFrame.from_dict(dict_winamax)
    df_transposed = df.transpose()

    df_transposed['site'] = "Winamax"
    df_odd = pd.DataFrame.from_records(df_transposed.odds.tolist())
    df_odd_splited = pd.DataFrame(df_odd['winamax'].to_list(), columns=['odd_1', 'odd_n', 'odd_2'])
    df_odd_splited.index = df_transposed.index

    df = pd.concat([df_transposed, df_odd_splited], axis=1)

    df['country'] = ''
    df.drop(['odds', 'id'], axis=1, inplace=True)

    df = tools.sort_df_columns_from_list(df, config.COLUMNS_ODDS_DF)

    return df


