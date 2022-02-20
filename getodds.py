import requests
import json

API_KEY = 'fa61461316fcdb08b1898dc4bab3daff'
BASE_URL = 'https://api.the-odds-api.com/v4/'

def get_current_sports():
    '''Gets sports currently in season'''
    current_sports = requests.get(f"{BASE_URL}sports?apiKey={API_KEY}")
    return current_sports.json()

def get_upcoming_odds(sport_key, regions, markets):
    '''Gets odds of upcoming matches in a particular sport for the given regions and markets'''
    print(','.join(regions))
    upcoming_odds = requests.get(f"{BASE_URL}sports/{sport_key}/odds?apiKey={API_KEY}&regions={','.join(regions)}&markets={','.join(markets)}")
    print(upcoming_odds)
    match_odds = upcoming_odds.json()
    return match_odds
    
# print(get_current_sports(API_KEY))
if __name__ == "__main__":
    parsed = get_upcoming_odds("aussierules_afl", ["us"], ["h2h"])[0]
    print(json.dumps(parsed, indent=4))