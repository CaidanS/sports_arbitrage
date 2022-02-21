from flask import Flask, render_template, request
import flask_bootstrap
import findarb
import getodds
from afl_dummy_data import AFL_DUMMY_DATA
print('AFL_DUMMY_DATA',AFL_DUMMY_DATA)

app = Flask(__name__)
flask_bootstrap.Bootstrap(app)

# @app.route("/<sport_key>/<regions>/<markets>")
# def main(sport_key, regions, markets):
#     bookmakers_odds = getodds.get_upcoming_odds(sport_key, [regions], [markets])

#     arb_opps = findarb.list_arb_from_sport(bookmakers_odds, "h2h")
#     # print(arb_opps)
    
#     return render_template('index.html', arb_opps=arb_opps, bank_roll = 100)


@app.route("/")
def test():
    sport_key = request.args.get('sport_key')
    regions = request.args.get('regions')
    bankroll = request.args.get('bankroll')
    if sport_key is None and regions is None:
        return render_template('welcome.html')
    if sport_key is None:
        sport_key = "soccer_epl"
    if regions is None:
        regions = "eu"
    if bankroll is None or bankroll=='':
        bankroll = 100
    markets = "h2h"
    bookmakers_odds = getodds.get_upcoming_odds(sport_key, [regions], [markets])
    arb_opps = findarb.list_arb_from_sport(bookmakers_odds, "h2h")
    return render_template('index.html', arb_opps=arb_opps, bank_roll = int(bankroll))

# @app.errorhandler(Exception)
# def error(Exception):
#     return render_template('index.html', arb_opps=["error"], bank_roll = 100)


if __name__ == "__main__":
    app.run()