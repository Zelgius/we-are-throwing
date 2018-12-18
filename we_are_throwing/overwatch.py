from flask import Blueprint, request, jsonify
from random import shuffle
from we_are_throwing.constants import OW_HEROES
from collections import deque
import random

overwatch = Blueprint('overwatch', __name__)


@overwatch.route('/overwatch/random-team')
def random_team():

    # Gather data from web request
    players = request.args.get('players', None).split(',')
    num_tanks = request.args.get('tanks', 0, type=int)
    num_healers = request.args.get('healers', 0, type=int)
    num_dps = request.args.get('dps', 0, type=int)

    # calculate the total number or requested heroes
    total_heroes = num_tanks + num_healers + num_dps

    # If you didn't send players, nope.
    if players is None:
        return "No players specified", 200

    # if the number of heroes is greater than 6, the max size of an overwatch
    # team, nope.
    if total_heroes > 6:
        return "Can't have more than 6 heroes. Tanks: {0} + Healers: {1} + DPS: {2} = {3} > 6".format(num_tanks, num_healers, num_dps, total_heroes), 200

    # if you sent to many players, nope
    if len(players) > 6:
        return "Team cannot contain more than 6 players, nerd"

    # create a shuffled pool of all heroes to choose from if number of
    # requested heroes does not match party size
    all_hero_pool = list(OW_HEROES.keys())
    shuffle(all_hero_pool)

    # generate a random healer pool
    healer_pool = [hero for hero, attributes in OW_HEROES.items() if attributes['classification'] == 'healer']
    shuffle(healer_pool)

    # generate a random tank pool
    tank_pool = [hero for hero, attributes in OW_HEROES.items() if attributes['classification'] == 'tank']
    shuffle(tank_pool)

    # generate a random dps pool
    dps_pool = [hero for hero, attributes in OW_HEROES.items() if attributes['classification'] == 'dps']
    shuffle(dps_pool)

    # create a list with the correct number of random tanks
    selected_tanks = [tank_pool[i] for i in range(0, num_tanks)]

    # create a list with the correct number of random healers
    selected_healers = [healer_pool[i] for i in range(0, num_healers)]

    # create a list with the correct number of random dps
    selected_dps = [dps_pool[i] for i in range(0, num_dps)]

    # combine the above selected lists and randomize them
    selected_heroes = selected_tanks + selected_healers + selected_dps
    shuffle(selected_heroes)

    # if the number of heroes requested is less than the amount of players
    # remove already selected heroes from OW_HEREOS and then append to already
    # selected_heroes
    if total_heroes < len(players):
        selected_heroes += [hero for hero in all_hero_pool if hero not in selected_heroes]

    # put stuff in a queue so we can just pull off the front
    selected_heroes = deque(selected_heroes)

    # iterate over players and assign hero
    results = {}
    for player in players:
        results[player] = selected_heroes.popleft()

    # return results
    return jsonify(results)


@overwatch.route('/overwatch/individual')
def random_hero():
    results = {}
    heroes = list(OW_HEROES.keys())
    results['individual'] = random.choice(heroes)
    return jsonify(results)


@overwatch.route('/overwatch/fuck')
def fuck():
    pass
