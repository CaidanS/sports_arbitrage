from datetime import datetime
import getodds
import json
from dateutil import parser
import riskmodels


bookmakers_odds = [
        {
            "key": "unibet",
            "title": "Unibet",
            "last_update": "2022-02-20T00:37:17Z",
            "markets": [
                {
                    "key": "h2h",
                    "outcomes": [
                        {
                            "name": "Melbourne Demons",
                            "price": 1.61
                        },
                        {
                            "name": "Western Bulldogs",
                            "price": 2.3
                        }
                    ]
                }
            ]
        },
        {
            "key": "draftkings",
            "title": "DraftKings",
            "last_update": "2022-02-20T00:36:35Z",
            "markets": [
                {
                    "key": "h2h",
                    "outcomes": [
                        {
                            "name": "Melbourne Demons",
                            "price": 1.61
                        },
                        {
                            "name": "Western Bulldogs",
                            "price": 2.2
                        }
                    ]
                }
            ]
        },
        {
            "key": "fanduel",
            "title": "FanDuel",
            "last_update": "2022-02-20T00:31:26Z",
            "markets": [
                {
                    "key": "h2h",
                    "outcomes": [
                        {
                            "name": "Melbourne Demons",
                            "price": 1.59
                        },
                        {
                            "name": "Western Bulldogs",
                            "price": 2.38
                        }
                    ]
                }
            ]
        },
        {
            "key": "betfair",
            "title": "Betfair",
            "last_update": "2022-02-20T00:40:36Z",
            "markets": [
                {
                    "key": "h2h",
                    "outcomes": [
                        {
                            "name": "Melbourne Demons",
                            "price": 1.64
                        },
                        {
                            "name": "Western Bulldogs",
                            "price": 2.34
                        }
                    ]
                },
                {
                    "key": "h2h_lay",
                    "outcomes": [
                        {
                            "name": "Melbourne Demons",
                            "price": 1.75
                        },
                        {
                            "name": "Western Bulldogs",
                            "price": 2.56
                        }
                    ]
                }
            ]
        },
        {
            "key": "williamhill_us",
            "title": "William Hill (US)",
            "last_update": "2022-02-20T00:36:37Z",
            "markets": [
                {
                    "key": "h2h",
                    "outcomes": [
                        {
                            "name": "Melbourne Demons",
                            "price": 1.62
                        },
                        {
                            "name": "Western Bulldogs",
                            "price": 2.38
                        }
                    ]
                }
            ]
        }
    ]

def find_arb_from_match_odds(bookmakers_odds, match_data):
    arb_opps = []
    def rec_arb_finder(bookmakers_odds, num_legs=None, current_leg=0, arbtrace={}):
        if num_legs == None:
            num_legs = len(bookmakers_odds[0]["markets"][0]["outcomes"])
        if current_leg == num_legs:
            temp_sum = 0
            for leg in range(num_legs):
                temp_sum += 1/arbtrace[leg]["price"]
            if temp_sum < 1 and (parser.parse(match_data['commence_time']) - datetime.utcnow()).days  > 1:
                ad_return = (1/temp_sum -1) * (1-riskmodels.calc_likelihood_of_cancellation('test', 100, temp_sum, match_data['commence_time']))
                data = {
                    "match_data": match_data,
                    "odds": temp_sum, 
                    "bookies": dict(arbtrace),
                    "returns":{
                        'return': 1/temp_sum -1,
                        'adjusted_return': ad_return,
                        'annualized_return': ((1/temp_sum)**(365/((parser.parse(match_data['commence_time']) - datetime.utcnow()).days + 1))-1),
                        'adjusted_annualized_return': ((ad_return + 1)**(365/((parser.parse(match_data['commence_time']) - datetime.utcnow()).days + 1))-1)
                    }
                }
                arb_opps.append(data)
                # print(data)
        else:
            for bookmaker in bookmakers_odds:
                if bookmaker["key"] not in str(arbtrace.values()):
                    price = bookmaker["markets"][0]["outcomes"][current_leg]["price"]
                    arbtrace[current_leg] = {
                        "bookmaker_key" : bookmaker["key"],
                        "bookmaker_name" : bookmaker["title"],
                        "price" : price,
                    }
                    # print(arbtrace[current_leg])
                    rec_arb_finder(bookmakers_odds, num_legs, current_leg + 1, arbtrace)
    rec_arb_finder(bookmakers_odds)
    return arb_opps

def list_arb_from_sport(upcoming_matches, market):
    arb_opps = []
    if len(upcoming_matches) > 1:
        for match in upcoming_matches:
            match_data = {
                'sport_title' : match['sport_title'],
                'commence_time' : parser.parse(match['commence_time']).strftime('%m/%d/%Y, %H:%M'),
                'home_team' : match['home_team'],
                'away_team' : match['away_team'],
                'outcomes': match['bookmakers'][0]['markets'][0]['outcomes']
            }
            arb_opps = arb_opps + find_arb_from_match_odds(match['bookmakers'], match_data)
        print(json.dumps(arb_opps, indent=4))
    return arb_opps

