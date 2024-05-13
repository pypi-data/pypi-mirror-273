import random


class GetCard:
    # 摸牌的类

    def __init__(self):
        pass

    def get_card(self, cards, cards_data, user, count, user_cards):
        # user摸一张牌
        card = cards.pop(
            random.randint(0, len(cards) - 1)
        )  # 随机从牌组中摸一张牌
        card_data = cards_data[card]  # 获取该牌的点数
        if user == 'player':
            print('你摸到了 ' + card)
            count += card_data  # 玩家点数增加
            user_cards.append(card)  # 玩家牌组增加
            print('你现在的点数是 ' + str(count))
            print('你的牌是 ' + str(user_cards))
            print()
        elif user == 'computer':
            count += card_data  # 电脑点数增加
            user_cards.append(card)  # 电脑牌组增加
        # 返回点数和玩家牌组
        return count, user_cards
