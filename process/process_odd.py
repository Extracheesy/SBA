import pandas as pd

def get_optimized_odd(df):
    df.reset_index(inplace=True)
    list_bookmakers = list(set(df['site'].tolist()))
    df = df[df['cpt_bookmakers'] == len(list_bookmakers)]
    list_games = list(set(df['games'].tolist()))
    df_odd = pd.DataFrame()
    for game in list_games:
        df_sub = df[df['games'] == game]
        list_dates = list(set(df_sub['date'].tolist()))
        for date in list_dates:
            df_sub = df_sub[df_sub['date'] == date]
            list_odd_1 = df_sub['odd_1'].tolist()
            list_odd_n = df_sub['odd_n'].tolist()
            list_odd_2 = df_sub['odd_2'].tolist()
            min_odd = 1000
            max_odd = 0
            for odd_1 in list_odd_1:
                for odd_n in list_odd_n:
                    for odd_2 in list_odd_2:
                        odd = 1 / odd_1 + 1 / odd_n + 1 / odd_2
                        if min_odd > odd:
                            min_odd = odd
                        if max_odd < odd:
                            max_odd = odd
            df_new_row_odd = pd.DataFrame()
            df_new_row_odd.loc[0, 'date'] = date
            df_new_row_odd.loc[0, 'games'] = game
            df_new_row_odd.loc[0, 'odd_min'] = min_odd
            df_new_row_odd.loc[0, 'odd_max'] = max_odd
            df_odd = pd.concat([df_odd, df_new_row_odd], axis=0)

    df_odd.sort_values(by=['odd_min'], inplace=True)
    df_odd.reset_index(drop=True, inplace=True)
    return df_odd
