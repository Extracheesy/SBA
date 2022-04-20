# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import config
import parse
import tools
import matching
import fuzzy

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tools.mk_dir()
    df = parse.get_odds(config.LIST_BETTING_SITE)

    df = matching.match_team_names(df)

    df.to_csv('OUT/odds.csv')

    fuzzy.get_match_ration(df.copy())

    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
