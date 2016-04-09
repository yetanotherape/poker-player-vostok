import json

import requests


class Player:
    VERSION = "Default Python folding player"

    # {
    #     "players": [
    #         {
    #             "name": "Player 1",
    #             "stack": 1000,
    #             "status": "active",
    #             "bet": 0,
    #             "hole_cards": [],
    #             "version": "Version name 1",
    #             "id": 0
    #         },
    #         {
    #             "name": "Player 2",
    #             "stack": 1000,
    #             "status": "active",
    #             "bet": 0,
    #             "hole_cards": [],
    #             "version": "Version name 2",
    #             "id": 1
    #         }
    #     ],
    #     "tournament_id": "550d1d68cd7bd10003000003",
    #     "game_id": "550da1cb2d909006e90004b1",
    #     "round": 0,
    #     "bet_index": 0,
    #     "small_blind": 10,
    #     "orbits": 0,
    #     "dealer": 0,
    #     "community_cards": [],
    #     "current_buy_in": 0,
    #     "pot": 0
    # }

    def get_current_rank(self, game_state):
        self_player_data = self.get_self_player_data(game_state)
        my_cards = self_player_data['hole_cards']
        common_cards = game_state['community_cards']
        cards = my_cards + common_cards

        result = requests.get('http://rainman.leanpoker.org/rank', data={'cards': json.dumps(cards)})
        if result.status_code == 200:
            result = json.loads(result.content)
            rank = result['rank']

        else:
            rank = 0

        return rank

    def get_self_player_data(self, game_state):
        self_id = game_state['in_action']
        for player in game_state['players']:
            if player['id'] == self_id:
                return player

        return {}

    def is_hand_good(self, game_state):
        self_player_data = self.get_self_player_data(game_state)
        my_cards = self_player_data['hole_cards']
        is_hand_good = False
        first_card = ''
        for card in my_cards:
            if first_card and first_card == card['rank']:
                is_hand_good = True
            if first_card == '':
                first_card = card['rank']
            if card['rank'] == 'A' or card['rank'] == 'K':
                is_hand_good = True
        return is_hand_good

    def is_good_range(self, my_cards):
        is_good = False
        return is_good

    def betRequest(self, game_state):
        bet = max(game_state['small_blind'] * 8, game_state['current_buy_in'])
        bet_more = self.is_hand_good(game_state)

        if bet_more:
            bet = 1000
        else:
            if game_state['current_buy_in'] > 0:
                bet = 0

        return bet

    def showdown(self, game_state):
        pass

