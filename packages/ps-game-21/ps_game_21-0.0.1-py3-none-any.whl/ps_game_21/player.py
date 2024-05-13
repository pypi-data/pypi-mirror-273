from ps_game_21.get_card import GetCard


class Player:
    # 玩家的操作
    def __init__(self):
        self.get = GetCard()

    def player_stop(self, player_count, player_status):
        # 玩家叫停判断逻辑
        if player_status == 1:
            if player_count > 21:
                # 达到“引爆”条件后自动叫停
                player_status = 0
            else:
                while True:
                    # 玩家选择是否叫停
                    stop = input("是否叫停？(y/n)：")
                    if stop == "y":
                        player_status = 0
                        print("你已叫停")
                        print()
                        break
                    elif stop == "n":
                        player_status = 1
                        break
                    else:
                        print("输入有误，请重新输入")
        else:
            print("你已叫停")
            print()
        return player_status

    def player_get_card(
        self, player_count, player_cards, player_status, cards, cards_data, num
    ):
        # 玩家摸牌逻辑
        # 先判定是否叫停
        if player_status == 1:
            # 摸一张牌
            player_count, player_cards = self.get.get_card(
                cards, cards_data, "player", player_count, player_cards
            )
            num -= 1  # 牌组剩余牌数减1
        return player_count, player_cards, num

    def show_card(self, player_cards):
        # 从2张牌的牌组中选择一张进行展示
        print("你手上的牌是：", player_cards)
        while True:
            # 玩家选择展示的牌
            show_card_num = int(input("请选择展示的牌（1/2）："))
            if show_card_num == 1:
                show_card = player_cards[0]
                break
            elif show_card_num == 2:
                show_card = player_cards[1]
                break
            else:
                print("输入有误，请重新输入")
        return show_card
