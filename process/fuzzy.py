from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

def get_match_ration(df):
    print(len(df))
    df = df.drop(df[df.cpt_bookmakers == 2].index)

    df_winamax = df.copy()
    df_winamax = df_winamax.drop(df_winamax[df_winamax['site'] != 'Winamax'].index)

    df_unibet = df.copy()
    df_unibet = df_unibet.drop(df_unibet[df_unibet['site'] != 'Unibet'].index)

    list_matching_winamax = []
    list_matching_unibet = []
    list_winamax = df_winamax['team_1'].tolist() + df_winamax['team_2'].tolist()
    list_winamax = list(dict.fromkeys(list_winamax))
    list_unibet = df_unibet['team_1'].tolist() + df_unibet['team_2'].tolist()
    list_unibet = list(dict.fromkeys(list_unibet))

    for winamax in list_winamax:
        for unibet in list_unibet:
            if winamax != unibet:
                if fuzz.partial_ratio(winamax, unibet) == 100:
                    print(winamax, "       " ,unibet)
                    list_matching_winamax.append(winamax)
                    list_matching_unibet.append(unibet)

    df_match_teams = pd.DataFrame()
    df_match_teams['wianamax_team'] = list_matching_winamax
    df_match_teams['unibet_team'] = list_matching_unibet

    df_match_teams.to_csv('OUT/match.csv')

    print(len(df))