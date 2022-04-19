import config
import unibet
import winamax

import pandas as pd
import numpy as np

def get_odds(list):
    df_odds = pd.DataFrame()
    for site in list:
        df = parse(site, config.URL_ODDS[site])
        df_odds = pd.concat([df_odds, df])
    return df_odds
"""
    if site == 'UNIBET':
        unibet_dict = unibet.parse(config.URL_ODDS[site])
        df_unibet = unibet.transform_dict_to_df(unibet_dict)
        df_unibet.to_csv('OUT/unibet.csv')
    elif site == 'WINAMAX':
        unibet_dict = winamax.parse(config.URL_ODDS[site])
        df_unibet = winamax.transform_dict_to_df(unibet_dict)
        df_unibet.to_csv('OUT/winamax.csv')
"""

def parse(site, url=""):
    """
    Retourne les cotes d'un site donné
    """
    parse_functions = {
        "unibet": unibet.parse_unibet,
        "winamax": winamax.parse_winamax
    }
    return parse_functions[site](url)


"""
"betclic" : betclic.parse_betclic,
"barrierebet": lambda x: pasinobet.parse_pasinobet(x, barrierebet=True),
"betfair" : betfair.parse_betfair,
"betway" : betway.parse_betway,
"pokerstars" : pokerstars.parse_pokerstars,
"bwin" : bwin.parse_bwin,
"france_pari" : france_pari.parse_france_pari,
"joa" : joa.parse_joa,
"netbet" : netbet.parse_netbet,
"parionssport" : parionssport.parse_parionssport,
"pasinobet" : pasinobet.parse_pasinobet,
"pinnacle" : pinnacle.parse_pinnacle,
"pmu" : pmu.parse_pmu,
"unibet_boost" :lambda x: unibet.parse_unibet(x, True),
"vbet": lambda x: pasinobet.parse_pasinobet(x, vbet=True),
"zebet" : zebet.parse_zebet
"""