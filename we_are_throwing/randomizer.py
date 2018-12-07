from flask import Blueprint, request, jsonify
from random import shuffle
from we_are_throwing.constants import OW_HEROES
import copy
import random

randomizer = Blueprint('randomizer', __name__)


@randomizer.route('/overwatch/random-team')
def random_team():
    heroes = copy.deepcopy(OW_HEROES)
    shuffle(heroes)
    players = request.args.get('players', None)
    if players is None:
        return "No players specified", 200
    players = players.split(',')
    if len(players) > 6:
        return "Team cannot contain more than 6 players, nerd"
    results = {}
    for player in players:
        results[player] = heroes.pop()

    return jsonify(results)


@randomizer.route('/overwatch/individual')
def random_hero():
    results = {}
    heroes = copy.deepcopy(OW_HEROES)
    results['individual'] = random.choice(heroes)
    return jsonify(results)
