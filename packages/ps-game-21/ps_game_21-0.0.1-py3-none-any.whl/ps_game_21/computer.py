from ps_game_21.get_card import GetCard
import random


class Computer:
    # 电脑逻辑判定
    def __init__(self):
        self.get = GetCard()  # 获取牌的类

    def computer_stop(self, computer_count, computer_status):
        # 电脑叫停判断逻辑
        if computer_status == 1:
            # 只要点数大于17点，就叫停
            if computer_count >= 17:
                computer_status = 0
                print("电脑已叫停")
                print()
            else:
                computer_status = 1
        else:
            print("电脑已叫停")
            print()
        return computer_status

    def computer_get_card(
        self,
        computer_count,
        computer_cards,
        computer_status,
        cards,
        cards_data,
        num,
    ):
        # 电脑摸牌逻辑
        # 先判定是否叫停
        if computer_status == 1:
            # 摸一张牌
            computer_count, computer_cards = self.get.get_card(
                cards, cards_data, "computer", computer_count, computer_cards
            )
            num -= 1  # 牌堆剩余牌数减1
        return computer_count, computer_cards, num

    def show_card(self, computer_cards):
        # 从2张牌的牌组中随机选择一张进行展示
        computer_show = random.choice(computer_cards)
        return computer_show
