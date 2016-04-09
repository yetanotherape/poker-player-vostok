import json

import requests


class Player:
    VERSION = "Default Python folding player"
    game_state = {}
    M = 100
    my_pos = 0

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
        in_spectre = self.is_hand_in_spectre("22 A2 K7 Q9 JT", first_card, second_card)

        return in_spectre

    def is_hand_good_push_fold(self, first_card, second_card):
        if self.M >= 8:
            if self.my_pos == 1:
                spectre = "22+ Kx+ Q2s+ Q8o+ J3s+ J8o+ T4s+ T8o+ 95s+ 97o+ 85s+ 87o 74s+ 76o 64s+ 53s+"
            elif self.my_pos == 0:
                spectre = "22+ A8s+ A5s ATo+ K9s+ KQo Q9s+ J9s+ T9s"
            elif self.my_pos == 6:
                spectre = "22+ A8s+ A5s ATo+ K9s+ KQo Q9s+ J9s+ T9s"
            elif self.my_pos == 5:
                spectre = "22+ A8s+ A5s ATo+ K9s+ KQo Q9s+ J9s+ T9s"
            elif self.my_pos == 4:
                spectre = "22+ A7s+ A5s-A3s ATo+ K8s+ KJo+ Q8s+ QJo J8s+ T8s+ 98s"
            elif self.my_pos == 3:
                spectre = "22+ A2s+ A7o+ A5o K7s+ KTo+ Q8s+ QTo+ J8s+ JTo T8s+ 98s 87s"
            elif self.my_pos == 2:
                spectre = "22+ Ax+ K5s+ KTo+ Q8s+ QTo+ J8s+ JTo T8s+ 97s+ 87s 76s"
        elif self.M >= 7:
            if self.my_pos == 1:
                spectre = "22+ Kx+ Q2s+ Q5o+ J2s+ J7o+ T4s+ T8o+ 95s+ 97o+ 85s+ 87o 74s+ 76o 64s+ 53s+"
            elif self.my_pos == 0:
                spectre = "22+ A7s+ A5s-A3s ATo+ K8s+ KJo+ Q9s+ QJo J9s+ T9s 98s"
            elif self.my_pos == 6:
                spectre = "22+ A7s+ A5s-A3s ATo+ K8s+ KJo+ Q9s+ QJo J9s+ T9s 98s"
            elif self.my_pos == 5:
                spectre = "22+ A7s+ A5s-A3s ATo+ K8s+ KJo+ Q9s+ QJo J9s+ T9s 98s"
            elif self.my_pos == 4:
                spectre = "22+ A2s+ A8o+ K8s+ KTo+ Q9s+ QJo J8s+ JTo T8s+ 98s"
            elif self.my_pos == 3:
                spectre = "22+ Ax+ K7s+ KTo+ Q9s+ QJo J8s+ JTo T8s+ 98s 87s"
            elif self.my_pos == 2:
                spectre = "22+ Ax+ K4s+ K9o+ Q8s+ QTo+ J8s+ JTo T7s+ 97s+ 86s+ 76s 65s"
        elif self.M >= 6:
            if self.my_pos == 1:
                spectre = "22+ Qx+ J2s+ J4o+ T2s+ T6o+ 93s+ 96o+ 84s+ 86o+ 74s+ 76o 63s+ 53s+ 43s"
            elif self.my_pos == 0:
                spectre = "22+ A2s+ A8o+ K8s+ KTo+ Q9s+ QJo J9s+ T8s+ 98s"
            elif self.my_pos == 6:
                spectre = "22+ A2s+ A8o+ K8s+ KTo+ Q9s+ QJo J9s+ T8s+ 98s"
            elif self.my_pos == 5:
                spectre = "22+ A2s+ A8o+ K8s+ KTo+ Q9s+ QJo J9s+ T8s+ 98s"
            elif self.my_pos == 4:
                spectre = "22+ A2s+ A4o+ K8s+ KTo+ Q9s+ QJo J8s+ JTo T8s+ 98s 87s"
            elif self.my_pos == 3:
                spectre = "22+ Ax+ K6s+ KTo+ Q9s+ QTo+ J8s+ JTo T8s+ 97s+ 87s"
            elif self.my_pos == 2:
                spectre = "22+ Ax+ K2s+ K7o+ Q8s+ QTo+ J8s+ JTo T7s+ 97s+ 86s+ 76s 65s"
        else:
            spectre = "77 A9 KJ QJ"

        in_spectre = self.is_hand_in_spectre(spectre, first_card, second_card)

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
            bet = 0
            # if game_state['current_buy_in'] > 0:
            #     bet = 0
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

        players = self.game_state['players'] + self.game_state['players']

        is_dealer_found = False
        pos = 0
        my_pos = 0
        for player in players:
            if player['id'] > self.game_state['dealer']:
                if player['status'] != 'out':
                    pos += 1
                if player['id'] == self_player_data['id']:
                    my_pos = pos
            elif player['id'] == self.game_state['dealer'] and is_dealer_found:
                break
            elif player['id'] == self.game_state['dealer']:
                is_dealer_found = True

        total_active = pos
        if my_pos >= 2:
            my_pos = total_active + 2 - my_pos
        elif my_pos == 2:
            my_pos = 0

        self.my_pos = my_pos

        if game_state['bet_index'] == 0:
            M = self_player_data['stack'] / (game_state['small_blind'] * 3)
        else:
            M = 100

        self.M = M

        if M > 8:
            bet = self.get_bet_for_calm_game()
        else:
            bet = self.get_bet_for_push_fold()

        return bet

    def showdown(self, game_state):
        pass

