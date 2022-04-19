import pandas as pd

def match_team_names(df):
    df_temp = df.copy()
    df['games'] = df.index.tolist()
    df['games'] = df['games'].str.upper()
    df.index = df['games']

    df['team_1'] = df['games'].str.split(' - ').str[0]
    df['team_1'] = df['team_1'].str.upper()
    df['team_2'] = df['games'].str.split(' - ').str[1]
    df['team_2'] = df['team_2'].str.upper()

    df_result = pd.DataFrame(df.games.value_counts())
    df_result.rename(columns={'games': 'cpt_matching'}, inplace=True)

    df['cpt_bookmakers'] = df_result['cpt_matching']

    # df.sort_values(by=['team_1'], inplace=True)
    # df.sort_values(by=['team_2'], inplace=True)
    df.sort_values(by=['date'], inplace=True)
    df.drop(['games'], axis=1, inplace=True)

    return df