import pandas as pd
import config

def match_team_names(df):
    df_temp = df.copy()
    df['games'] = df.index.tolist()
    df['games'] = df['games'].str.upper()
    df.index = df['games']

    df['team_1'] = df['games'].str.split(' - ').str[0]
    df['team_1'] = df['team_1'].str.upper()
    df['team_2'] = df['games'].str.split(' - ').str[1]
    df['team_2'] = df['team_2'].str.upper()

    df.to_csv('OUT/odds_0.csv')

    df = match_bookmakers_team_names(df)
    df.set_index('games', inplace=True, drop=False)

    df_result = pd.DataFrame(df.games.value_counts())
    df_result.rename(columns={'games': 'cpt_matching'}, inplace=True)

    df['cpt_bookmakers'] = df_result['cpt_matching']

    df.sort_values(by=['date'], inplace=True)
    df.drop(['games'], axis=1, inplace=True)

    return df


def match_bookmakers_team_names(df):
    df_teams = pd.read_csv(config.MATCH_BOOKMAKERS_NAMES)
    df_teams = df_teams.drop_duplicates()
    df_teams.to_csv(config.MATCH_BOOKMAKERS_NAMES_NO_DUPLICATES)

    lst_bookmakers = df_teams.columns.tolist()
    lst_bookmakers.remove('sub')

    for bookmaker in lst_bookmakers:
        df_teams.set_index(bookmaker, inplace=True, drop=False)
        for replaced in df_teams.index.tolist():
            df.replace(replaced, df_teams['sub'][replaced], inplace=True, regex=True)

    return df