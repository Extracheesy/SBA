import os
import config

def sort_df_columns_from_list(df, columns):
    df = df.reindex(columns=columns)
    return df

def mk_dir():
    path = config.PATH_OUT
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")