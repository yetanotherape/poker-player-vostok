import json

import requests


class Player:
    VERSION = "Default Python folding player"
    game_state = {}
    M = 100

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
        self_player_data = self.get_self_player_data()
        my_cards = self_player_data['hole_cards']
        common_cards = game_state['community_cards']
        cards = my_cards + common_cards

        result = requests.get('http://rainman.leanpoker.org/rank', data={'cards': json.dumps(cards)})
        if result.status_code == 200:
            result = json.loads(result.content)
            rank = result

        else:
            rank = {}

        return rank

    def get_self_player_data(self):
        self_id = self.game_state['in_action']
        for player in self.game_state['players']:
            if player['id'] == self_id:
                return player

        return {}

    def is_hand_good(self, spectre='default'):
        self_player_data = self.get_self_player_data()
        my_cards = self_player_data['hole_cards']
        first_card = my_cards[0]
        second_card = my_cards[1]

        if spectre == 'wide':
            func = self.is_hand_good_wide
        elif spectre == 'push_fold':
            func = self.is_hand_good_push_fold
        else:
            func = self.is_hand_good_narrow

        is_hand_good = self.rotate_cards(func, first_card, second_card)

        return is_hand_good

    def rotate_cards(self, func, first_card, second_card):
        is_hand_good = func(first_card, second_card)
        is_hand_good = is_hand_good or func(second_card, first_card)

        return is_hand_good

    def is_hand_good_narrow(self, first_card, second_card):
        in_spectre = self.is_hand_in_spectre("TT AJ KQ", first_card, second_card)

        return in_spectre

    def is_hand_good_wide(self, first_card, second_card):
        in_spectre = self.is_hand_in_spectre("66 A6 K9 QT JT", first_card, second_card)

        return in_spectre

    def is_hand_good_push_fold(self, first_card, second_card):
        in_spectre = self.is_hand_in_spectre("77 A9 KJ QJ", first_card, second_card)

        return in_spectre

    def is_hand_in_spectre(self, spectre, first_card, second_card):
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        first_card_index = cards.index(first_card['rank'])
        second_card_index = cards.index(second_card['rank'])

        hands = spectre.split(" ")
        in_spectre = False
        cards_spectre = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        for hand in hands:
            first_card_in_hand = hand[0]
            second_card_in_hand = hand[1]
            first_cards_in_hand_index = cards_spectre.index(first_card_in_hand)
            second_cards_in_hand_index = cards_spectre.index(second_card_in_hand)

            if first_cards_in_hand_index == second_cards_in_hand_index:
                if first_card_index == second_card_index and first_card_index >= first_cards_in_hand_index:
                    in_spectre = True
            elif first_card_index >= first_cards_in_hand_index and second_card_index >= second_cards_in_hand_index:
                in_spectre = True
                break

        return in_spectre



    def is_good_rank(self):
        is_good = False

        rank = self.get_current_rank(self.game_state)
        if rank >= 2:
            is_good = True

        return is_good

    def get_active_players_count(self):
        active_count = 0
        for player in self.game_state['players']:
            if player['status'] != 'out':
                active_count += 1
        return active_count

    def get_bet_for_calm_game(self):
        game_state = self.game_state
        bet = max(game_state['small_blind'] * 8, game_state['current_buy_in'])
        active_players_count = self.get_active_players_count()
        if active_players_count >= 3:
            is_hand_good = self.is_hand_good()
        else:
            is_hand_good = self.is_hand_good(spectre='wide')

        common_cards_count = len(self.game_state['community_cards'])

        if common_cards_count >= 3:
            rank_data = self.get_current_rank(self.game_state)
            rank = rank_data['rank']
            if rank >= 1:
                is_hand_good = True
            elif rank == 0:
                is_hand_good = False

        if not is_hand_good:
            if game_state['current_buy_in'] > 0:
                bet = 0
        return bet

    def get_bet_for_push_fold(self):
        bet = 0

        is_hand_good = self.is_hand_good(spectre="push_fold")

        if is_hand_good:
            bet = 1000000

        return bet

    def bet_request(self, game_state):
        self.game_state = game_state

        self_player_data = self.get_self_player_data()

        if game_state['bet_index'] == 0:
            M = self_player_data['stack'] / (game_state['small_blind'] * 3)
        else:
            M = 100

        self.M = M

        if M > 10:
            bet = self.get_bet_for_calm_game()
        else:
            bet = self.get_bet_for_push_fold()

        return bet

    def showdown(self, game_state):
        pass

