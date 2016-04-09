import json

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

    def betRequest(self, game_state):
        bet = max(game_state['small_blind'] * 8, game_state['current_buy_in'])
        bet_more = self.is_hand_good(game_state)

        if bet_more:
            bet = 1000

        return bet

    def is_hand_good(self, game_state):
        self_player_data = self.getSelfPlayerData(game_state)
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


    # def getCurrentRank(self, game_state):
    #     self_player_data = self.getSelfPlayerData(game_state)
    #     my_cards = self_player_data['hole_cards']
    #     common_cards = game_state['community_cards']
    #     cards = my_cards + common_cards
    #     cards = json.dumps(cards)
    #
    #
    #     return rank

    def getSelfPlayerData(self, game_state):
        selfIndex = game_state['in_action']
        for player in game_state['players']:
            if player['id'] == selfIndex:
                return player
        return {}


    def showdown(self, game_state):
        pass

