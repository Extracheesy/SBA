LIST_BETTING_SITE = ['unibet', 'winamax']
URL_ODDS = {
    'unibet' : 'https://www.unibet.fr/sport/football',
    'winamax' : 'https://www.winamax.fr/paris-sportifs/sports/1'
}

COLUMNS_ODDS_DF = ['date', 'site', 'odd_1', 'odd_n', 'odd_2', 'country', 'competition']

PATH_OUT = './OUT'
MATCH_BOOKMAKERS_NAMES = './DATA/matching bookmakers names.csv'
MATCH_BOOKMAKERS_NAMES_NO_DUPLICATES = './DATA/matching bookmakers no_duplicates.csv'